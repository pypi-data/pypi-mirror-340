import re
import os
from yamcs.pymdb import IntegerArgument, FloatArgument, BooleanArgument, EnumeratedArgument, StringArgument


def to_upper_camel_case(s):
    if s[0].islower():
        s = s[0].upper() + s[1:]
    if ' ' in s or '_' in s:
        words = re.split(r'[^a-zA-Z0-9]', s)
        return ''.join(word.capitalize() for word in words if word)
    return s

def to_snake_case(s):
    s = re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()
    s = re.sub(r'[^a-zA-Z0-9_]', '_', s)
    s = re.sub(r'__', '_', s)
    return s

def replace_with_indentation(text, keyword, replacement):
    lines = text.split('\n')
    indent = 0
    for line in lines:
        if keyword in line:
            indent = len(line) - len(line.lstrip())
    
    return text.replace(keyword, replacement.replace('\n', ('\n'+(indent*' '))))

def insert_before_with_indentation(text, keyword, replacement):
    lines = text.split('\n')
    indent = 0
    for line in lines:
        if keyword in line:
            indent = len(line) - len(line.lstrip())
    return text.replace(keyword, (replacement.replace('\n', ('\n'+(indent*' ')))+keyword))

def get_keywords(text):
    pattern = r'<<.*?>>'
    return re.findall(pattern, text)

def get_var_keywords(text):
    pattern = r'<<VAR_.*?>>'
    return re.findall(pattern, text)

def get_service_module_keywords(text):
    pattern = r'<<SERVICE_MODULE_.*?>>'
    return re.findall(pattern, text)

def get_command_module_keywords(text):
    pattern = r'<<COMMAND_MODULE_.*?>>'
    return re.findall(pattern, text)

def delete_all_keywords(text):
        keywords = get_keywords(text)
        for keyword in keywords:
            text = text.replace(keyword, '')
        return text

def delete_all_command_module_keywords(text):
        keywords = get_command_module_keywords(text)
        for keyword in keywords:
            text = text.replace(keyword, '')
        return text

def arg_type_to_rust(arg, bit_number_str='32'):
    if isinstance(arg, IntegerArgument):
        if arg.signed:
            return 'i'+bit_number_str
        else:
            return 'u'+bit_number_str
    elif isinstance(arg, FloatArgument):
        return 'f'+bit_number_str
    elif isinstance(arg, BooleanArgument):
        return 'bool'
    elif isinstance(arg, EnumeratedArgument):
        return arg.name
    elif isinstance(arg, StringArgument):
        return 'String'
    else:
        print('Argument type is not supported: '+str(type(arg)))
        return None
    
def arg_enum_rust_definition(arg):
    if not isinstance(arg, EnumeratedArgument):
        raise ValueError('Provided Argument is not of type EnumeratedArgument.')
    definition_text = 'pub enum '+arg.name+' {\n'
    for choice in arg.choices:
        definition_text += ('\t'+str(choice[1])+' = '+str(choice[0])+',\n')
    definition_text += '}\n'
    return definition_text

def engineering_bit_number(raw_bit_number):
    if raw_bit_number < 1 or raw_bit_number > 128:
        raise ValueError("raw_bit_number must be between 1 and 128")
    power = 1
    while 2**power < raw_bit_number:
        power += 1
    bit_number = 2**power
    return (bit_number)

def get_data_type(parent_classes):
    """Extract the data type from a list of parent class names.
    Returns the class name that ends with 'DataType' or None if not found."""
    for class_name in parent_classes:
        if class_name.endswith('DataType'):
            return class_name
    return None

def rust_type_definition(pymdb_data_instance):
    sc_instance_name = to_snake_case(pymdb_data_instance.name)
    parent_classes = list(map(lambda type: type.__name__, type(pymdb_data_instance).mro()))
    data_type = get_data_type(parent_classes)
    base_type = pymdb_data_instance.__class__.__name__
    if data_type is None:
        raise ValueError("Data type not found in parent classes.")

    if data_type == 'IntegerDataType':
        if pymdb_data_instance.encoding is None or pymdb_data_instance.encoding.bits is None:
            raw_bit_number = 8
            print("Warning: No encoding for "+base_type+" "+pymdb_data_instance.name+" found. Using 8 as default for raw bit number.")
        else:
            raw_bit_number = pymdb_data_instance.encoding.bits
        raw_bit_number_str = str(raw_bit_number)
        eng_bit_number = engineering_bit_number(raw_bit_number)
        eng_bit_number_str = str(eng_bit_number)
        definition_text = ["\t#[bits("+raw_bit_number_str+")]\n"]
        if pymdb_data_instance.signed:
            definition_text[0] += ("\tpub "+sc_instance_name+": i"+eng_bit_number_str+",\n")
        else:
            definition_text += ("\tpub "+sc_instance_name+": u"+eng_bit_number_str+",\n")
        definition_text.append("")
    
    elif data_type == 'BooleanDataType':
        definition_text = ["\t#[bits(1)]\n\tpub "+sc_instance_name+": bool,\n"]
        definition_text.append("")
    
    elif data_type == 'StringDataType':
        definition_text = ["\t#[null_terminated]\n\tpub "+sc_instance_name+": String,\n", ""]
    
    elif data_type == 'ArrayDataType':
        struct_name = to_upper_camel_case(pymdb_data_instance.name)
        definition_text = ["\tpub "+sc_instance_name+": Vec<"+struct_name+">,\n"]
        definition_text.append("pub struct "+struct_name+" {\n")
        for member in pymdb_data_instance.data_type.members:
            definition_text[1] += rust_type_definition(member)[0]
        definition_text[1] += "}\n"
        for member in pymdb_data_instance.data_type.members:
            definition_text[1] += rust_type_definition(member)[1]
    
    elif data_type == 'EnumeratedDataType':
        definition_text = ["\tpub "+pymdb_data_instance.name+": "+to_upper_camel_case(pymdb_data_instance.name)+",\n"]
        definition_text.append("pub enum "+to_upper_camel_case(pymdb_data_instance.name)+" {\n")
        for choice in pymdb_data_instance.choices:
            definition_text[1] += "\t"+str(choice[1])+" = "+str(choice[0])+",\n"
        definition_text[1] += "}\n"
    
    else:
        definition_text = ["\t// Please implement datatype "+data_type+" here.\n", ""]
    return definition_text