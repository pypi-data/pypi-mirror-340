from yamcs.pymdb import Container, ParameterEntry, AggregateParameter, ArrayParameter, BinaryParameter, StringParameter, BooleanParameter, FloatParameter, IntegerParameter, StringMember, EnumeratedMember
from .utils import *
    

def generate_rccn_parameter_telemetry(parameter):
    sc_parameter_name = to_snake_case(parameter.name)

    if isinstance(parameter, ArrayParameter):
        struct_name = to_upper_camel_case(parameter.name)
        telemetry = ["\tpub "+sc_parameter_name+": Vec<"+struct_name+">,\n"]
        telemetry.append("pub struct "+struct_name+" {\n")
        for member in parameter.data_type.members:
            telemetry[1] += generate_rccn_member_telementry(member)[0]
        telemetry[1] += "}\n"
        for member in parameter.data_type.members:
            telemetry[1] += generate_rccn_member_telementry(member)[1]

    elif isinstance(parameter, BooleanParameter):
        telemetry = ["\t#[bits(1)]\n\tpub "+sc_parameter_name+": bool,\n"]
        telemetry.append("")

    elif isinstance(parameter, IntegerParameter):
        if parameter.encoding is None or parameter.encoding.bits is None:
            raw_bit_number_str = '8'
            print("Warning: No encoding for parameter "+parameter.name+" found. Using 8 as default for raw bit number.")
        else:
            raw_bit_number = parameter.encoding.bits
            raw_bit_number_str = str(raw_bit_number)
            eng_bit_number = engineering_bit_number(raw_bit_number)
            eng_bit_number_str = str(eng_bit_number)
        telemetry = ["\t#[bits("+raw_bit_number_str+")]\n"]
        if parameter.signed:
            telemetry[0] += ("\tpub "+sc_parameter_name+": i"+eng_bit_number_str+",\n")
        else:
            telemetry += ("\tpub "+sc_parameter_name+": u"+eng_bit_number_str+",\n")
        telemetry.append("")

    elif isinstance(parameter, StringParameter):
        telemetry = ["#[null_terminated]\npub "+sc_parameter_name+": String,\n"]
        telemetry.append("")

    else:
        telemetry = ["\t// Please implement datatype "+type(parameter).__name__+" here.\n", ""]
    return telemetry

def generate_rccn_member_telementry(member):
    sc_member_name = to_snake_case(member.name)

    if isinstance(member, StringMember):
        member_telemetry = ["#[null_terminated]\n\tpub "+member.name+": String,\n"]
        member_telemetry.append("")

    elif isinstance(member, EnumeratedMember):
        member_telemetry = ["\tpub "+member.name+": "+to_upper_camel_case(member.name)+",\n"]
        member_telemetry.append("pub enum "+to_upper_camel_case(member.name)+" {\n")
        for choice in member.choices:
            member_telemetry[1] += "\t"+str(choice[1])+" = "+str(choice[0])+",\n"
        member_telemetry[1] += "}\n"

    elif isinstance(member, BooleanParameter):
        telemetry = ["pub "+sc_member_name+": bool,\n"]
        telemetry.append("")

    elif isinstance(member, IntegerParameter):
        if member.encoding is None or member.encoding.bits is None:
            raw_bit_number = 8
            print("Warning: No encoding for member "+member.name+" found. Using 8 as default for raw bit number.")
        else:
            raw_bit_number = member.encoding.bits
        raw_bit_number_str = str(raw_bit_number)
        eng_bit_number = engineering_bit_number(raw_bit_number)
        eng_bit_number_str = str(eng_bit_number)
        telemetry = ["\t#[bits("+raw_bit_number_str+")]\n"]
        if member.signed:
            telemetry[0] += ("\tpub "+sc_member_name+": i"+eng_bit_number_str+",\n")
        else:
            telemetry += ("\tpub "+sc_member_name+": u"+eng_bit_number_str+",\n")
        telemetry.append("")
    
    else:
        member_telemetry[0] += "\t// Please implement datatype "+type(member).__name__+" here.\n"
        member_telemetry.append("")
    return member_telemetry