import xml.etree.ElementTree as ET

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
                value_type = trace.find('type').text
                actual_value = trace.find('full_lhs_value').text

                base_name = trace.get('base_name')

                inputs_list.setdefault(base_name, {})
                inputs_list[base_name] = {'type': value_type, 'value': actual_value}

        reason = goto_trace.find('failure').get('reason')
        inputs.append({'inputs': inputs_list, 'reason': reason})
    return inputs