import xml.etree.ElementTree as ET

PRIMITIVE_TYPES = set(['int'])

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

    if assignment_type_text in PRIMITIVE_TYPES:
        return assignment_type_text

    if assignment_type_text.startswith('struct java::array'):
        return get_array_input_type(assignment_type_text)

    if assignment_type_text.startswith('struct'):
        return get_class_input_type(assignment_type_text)
    
    raise NotImplementedError(f'\'{assignment_type_text}\' input type not implemented')
    
def get_array_input_type(type_text: str) -> str:
    """Returns the java type string for array types"""
    pass

def get_class_input_type(type_text: str) -> str:
    """Returns the java type string for class types"""
    assert type_text.startswith('struct')
    class_name = type_text.split(' ')[1]
    return class_name

def get_input_value(assignment: ET.Element, trace: ET.Element) -> str:
    assert assignment.tag == 'assignment'
    assignment_value_text = assignment.findtext('full_lhs_value')
    assignment_type_text = assignment.findtext('type')

    if assignment_value_text == 'null':
        return 'null'

    if assignment_type_text in PRIMITIVE_TYPES:
        return assignment_value_text
    
    if assignment_type_text.startswith('struct java::array'):
        return get_array_input_value()

    if assignment_type_text.startswith('struct'):
        return get_class_input_value(assignment_value_text, trace)

    raise NotImplementedError(f'\'{assignment_type_text}\' input type not implemented')

def get_array_input_value() -> str:
    pass

def get_class_input_value(assignment_value_text: str, trace: ET.Element) -> str:
    pass


