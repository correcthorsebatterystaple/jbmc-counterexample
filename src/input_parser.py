import xml.etree.ElementTree as ET
from helpers import nested_set
from input_type_checker import is_array_type, is_class_type, is_primitive_type, is_string_type
import csv

def get_inputs(xml_source: str):
    """
    Given an XML trace as string from JBMC, it produces a dictionary of input types and values

    Returns:
        A list where the first element is the input variables dictionary 
        and second is the reason for failure.

        The input variables dict has keys which correspond to the name of the varibale
        and has values that correspond to a dict with the `type` and `value` of the variable
    """
    root = ET.fromstring(xml_source)
    inputs = []

    failed_results = [r for r in root.findall('result') if r.get('status') == 'FAILURE']
    for result in failed_results:
        goto_trace = result.find('goto_trace')

        inputs_list = {}
        for trace in goto_trace:
            if (
                trace.tag == 'assignment' and 
                trace.attrib['base_name'].startswith('arg')
            ):
                value_type = get_input_type(trace)
                actual_value = get_input_value(trace, goto_trace)

                base_name = trace.get('base_name')

                inputs_list.setdefault(base_name, {})
                inputs_list[base_name] = {'type': value_type, 'value': actual_value}

        reason = goto_trace.find('failure').get('reason')
        inputs.append({'inputs': inputs_list, 'reason': reason})
    return inputs

def get_input_type(assignment: ET.Element) -> str:
    """Return the java type string"""
    assert assignment.tag == 'assignment'
    assignment_type_text = assignment.findtext('type')

    if is_string_type(assignment_type_text):
        return "String"

    if is_primitive_type(assignment_type_text):
        return assignment_type_text

    if is_array_type(assignment_type_text):
        return get_array_input_type(assignment_type_text)

    if is_class_type(assignment_type_text):
        return get_class_input_type(assignment_type_text)
    
    raise NotImplementedError(f'\'{assignment_type_text}\' input type not implemented')
    
def get_array_input_type(type_text: str) -> str:
    """Returns the java type string for array types"""
    array_type = None
    if type_text.startswith('struct'):
        array_type = type_text.split(' ')[1]
        if array_type.startswith('java::array['):
            array_type = array_type.split('java::array[')[1]
            array_type = array_type.split(']')[0]
        else:
            array_type = get_class_input_type(type_text)
    else:
        array_type = type_text.split(" ")[0]
    return array_type + "[]"

def get_class_input_type(type_text: str) -> str:
    """Returns the java type string for class types"""
    assert type_text.startswith('struct')
    class_name = type_text.split(' ')[1]
    return class_name

def get_input_value(assignment: ET.Element, trace: ET.Element) -> str:
    """Gets java values for assignments"""
    assert assignment.tag == 'assignment'
    assignment_value_text = assignment.findtext('full_lhs_value')
    assignment_type_text = assignment.findtext('type')

    if assignment_value_text == 'null':
        return 'null'

    if is_primitive_type(assignment_type_text):
        return assignment_value_text

    if is_string_type(assignment_type_text):
        return get_string_input_value(assignment_type_text, assignment_value_text, trace)
    
    if is_array_type(assignment_type_text):
        return get_array_input_value(assignment_type_text, assignment_value_text, trace)

    if is_class_type(assignment_type_text):
        return get_class_input_value(assignment_value_text, trace)

    raise NotImplementedError(f'\'{assignment_type_text}\' input type not implemented')

def get_string_input_value(assignment_type_text, assignment_value_text, trace):
    assignments = [a for a in trace.findall('assignment') if a.get('base_name') == assignment_value_text[1:]]
    val = {}
    for assignment in assignments:
        full_lhs_text = assignment.findtext('full_lhs')
        full_lhs_value_text = assignment.findtext('full_lhs_value')

        if full_lhs_value_text.startswith('{'):
            continue

        if full_lhs_text == f'{assignment_value_text[1:]}.length':
            val['length'] = full_lhs_value_text

        if full_lhs_text == f'{assignment_value_text[1:]}.data':
            if full_lhs_value_text.startswith('&'):
                full_lhs_value_text = remove_dynamic_object_pointer_cast(full_lhs_value_text[1:])
                val['value'], _ = get_string_value(full_lhs_value_text, trace)
            elif full_lhs_value_text.startswith('dynamic_object'):
                val['value'], _ = get_string_value(full_lhs_value_text, trace)
            else: 
                val['value'] = full_lhs_value_text

    actual_array_value = list(csv.reader([val['value'][1:-1].strip()], skipinitialspace=True, delimiter=',', quotechar='\''))[0]
    actual_array_value = ''.join(actual_array_value)
    
    return "\"" + actual_array_value + "\""


def get_string_value(dynamic_obj_name, trace):
    assignments = [a for a in trace.findall('assignment') if a.get('base_name') == dynamic_obj_name]
    array_value = None
    assignment_type = None
    for assignment in assignments:
        full_lhs_text = assignment.findtext('full_lhs')
        full_lhs_value_text = assignment.findtext('full_lhs_value')
        assignment_type = assignment.findtext('type')
        if full_lhs_text == dynamic_obj_name:
            if full_lhs_value_text.startswith('{'):
                array_value = full_lhs_value_text
            elif full_lhs_value_text.startswith('&'):
                full_lhs_value_text = remove_dynamic_object_pointer_cast(full_lhs_value_text[1:])
                array_value, assignment_type =  get_string_value(full_lhs_value_text, trace)
            elif full_lhs_value_text.startswith('dynamic_object'):
                array_value, assignment_type = get_string_value(full_lhs_value_text, trace)
    
    return array_value, assignment_type

def get_array_input_value(assignment_type_text, assignment_value_text, trace) -> str:
    assignments = [a for a in trace.findall('assignment') if a.get('base_name') == assignment_value_text[1:]]
    val = {}
    for assignment in assignments:
        full_lhs_text = assignment.findtext('full_lhs')
        full_lhs_value_text = assignment.findtext('full_lhs_value')

        if full_lhs_value_text.startswith('{'):
            continue

        if full_lhs_text == f'{assignment_value_text[1:]}.length':
            val['length'] = full_lhs_value_text

        if full_lhs_text == f'{assignment_value_text[1:]}.data':
            if full_lhs_value_text.startswith('&'):
                full_lhs_value_text = remove_dynamic_object_pointer_cast(full_lhs_value_text[1:])
                val['value'], val["type"] = get_array_value(full_lhs_value_text, trace)
            elif full_lhs_value_text.startswith('dynamic_object'):
                val['value'], val["type"] = get_array_value(full_lhs_value_text, trace)
            else: 
                val['value'] = full_lhs_value_text
    
    # Convert the {} array into a list of elements
    # This method will not split on delimeter when delimeter is within the quotechar
    # e.g. '{ "abc", "def", "ghi,jkl"}' should come out as ["abc", "def", "ghi,jkl"]
    actual_array_value = val['value']

    # Get only the first "length" elements (Currently works only for 1-d arrays)
    actual_array_value = actual_array_value[0: int(val["length"])]
    
    # Join the array back in {} for Java initialisation
    val["value"] = actual_array_value
    return [get_array_input_type(val["type"]), val["value"]]

def remove_dynamic_object_pointer_cast(dynamic_obj_name):
    if dynamic_obj_name.startswith("((void *)"):
        dynamic_obj_name = dynamic_obj_name.split("((void *)")[1]
    dynamic_obj_name = dynamic_obj_name.split("[")[0]
    return dynamic_obj_name

# Method to get the value of a 1-d array
def get_array_value(dynamic_obj_name, trace):
    assignments = [a for a in trace.findall('assignment') if a.get('base_name') == dynamic_obj_name]
    array_value = None
    assignment_type = None
    for assignment in assignments:
        full_lhs_text = assignment.findtext('full_lhs')
        full_lhs_value_text = assignment.findtext('full_lhs_value')
        assignment_type = assignment.findtext('type')
        if full_lhs_text == dynamic_obj_name:
            if full_lhs_value_text.startswith('{'):
                array_value = full_lhs_value_text
            elif full_lhs_value_text.startswith('&'):
                full_lhs_value_text = remove_dynamic_object_pointer_cast(full_lhs_value_text[1:])
                array_value, assignment_type =  get_array_value(full_lhs_value_text, trace)
            elif full_lhs_value_text.startswith('dynamic_object'):
                array_value, assignment_type = get_array_value(full_lhs_value_text, trace)

    
    actual_array_value = list(csv.reader([array_value[1:-1]], delimiter=',', quotechar='"'))[0]
    for assignment in assignments:
        full_lhs_text = assignment.findtext('full_lhs')
        full_lhs_value_text = assignment.findtext('full_lhs_value')
        assignment_type = assignment.findtext('type')

        if full_lhs_text.startswith(dynamic_obj_name + "["):
            index = int(full_lhs_text.split(dynamic_obj_name + "[")[1].split("L")[0])

            index_array_value = actual_array_value[index]
            index_array_value = full_lhs_value_text
            actual_array_value[index] = index_array_value
            array_value = '{' + ','.join([str(x) for x in actual_array_value]) + '}'

    for index,value in enumerate(actual_array_value):
        if value.startswith("&"):
            actual_array_value[index] = get_dynamic_obj_value(value[1:], trace)

    return actual_array_value, assignment_type

def get_class_input_value(assignment_value_text: str, trace: ET.Element) -> dict:
    return get_dynamic_obj_value(assignment_value_text[1:], trace)

def get_dynamic_obj_value(dynamic_obj_name: str, trace: ET.Element) -> dict:
    assignments = [a for a in trace.findall('assignment') if a.get('base_name') == dynamic_obj_name]
    val = {}
    for assignment in assignments:
        full_lhs_text = assignment.findtext('full_lhs')
        full_lhs_value_text = assignment.findtext('full_lhs_value')

        # Filter out grouped assignments to dynamic objs
        if full_lhs_value_text.startswith('{'):
            continue

        # Assign class type to the dynamic object
        if full_lhs_text == f'{dynamic_obj_name}.@java.lang.Object.@class_identifier':
            val['__class'] = full_lhs_value_text.strip('"').split('::')[-1]
            continue

        # if value is another dynamic object then make recursive call
        if full_lhs_value_text.startswith('&'):
            value = get_dynamic_obj_value(full_lhs_value_text[1:], trace)
        else:
            value = full_lhs_value_text

        key_path = full_lhs_text.split('.')[1:]
        nested_set(val, key_path, value)
        
    return val



