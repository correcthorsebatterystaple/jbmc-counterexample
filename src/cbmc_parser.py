import xml.etree.ElementTree as ET
from lxml import etree
import subprocess
import sys

# Code to generate a java file with inputs for the test function of the supplied class
def generate_java(filename, counterexample_inputs):
    code = "class Counterexample { \n \tpublic static void main(String[] args) { \n \t"
    for input_var in counterexample_inputs:
        code += f'\t{counterexample_inputs[input_var]["type"]} {input_var} = ' \
                f'{counterexample_inputs[input_var]["value"]}; \n \t'

    code += f'\t{filename}.test({", ".join(counterexample_inputs.keys())}); \n \t'
    code += "} \n }"

    with open("Counterexample.java", "w") as f:
        f.write(code)
    return


# Code to compile the Java file and run JBMC with a specified path until running from outside Java file folder works correctly
def compile_and_run_java(jbmc_path, filepath):
    subprocess.run(["javac", filepath])
    filename = filepath.split(".")[0]
    print(filename)
    xml_text = subprocess.run([jbmc_path, filename, "--function", filename + ".test", "--unwind", "5",
                    "--trace", "--xml-ui"], capture_output=True, text=True)

    with open(filename + ".txt", "w") as f:
        f.write(xml_text.stdout)


def get_inputs(filename):
    file = open(filename + ".txt", "rb")
    tree = etree.parse(file)
    print(tree.getroot().tag)
    root = tree.getroot()
    # print(root.tag)
    for child in root:
        # print(child.tag, child.attrib)
        if child.tag == 'result' and child.attrib['status'] == 'FAILURE':

            function_name = child.attrib['property'].split('::')[1].split(':')[0]
            print(child.tag, child.attrib)
            # Get goto_trace
            goto_trace = None
            for child1 in child:
                if child1.tag == "goto_trace":
                    goto_trace = child1
                    break

            inputs_list = {}
            for goto_trace_child in goto_trace:
                if goto_trace_child.tag == 'assignment' \
                        and goto_trace_child.attrib['base_name'].startswith('arg'):
                    # print(goto_trace_child.attrib['base_name'])
                    value_type = None
                    actual_value = None
                    for attribute in goto_trace_child:
                        if attribute.tag == 'type':
                            value_type = attribute.text

                        if attribute.tag == 'full_lhs_value':
                            actual_value = attribute.text

                    # print(goto_trace_child.attrib['base_name'], value_type, actual_value)
                    if goto_trace_child.attrib['base_name'] not in inputs_list:
                        inputs_list[goto_trace_child.attrib['base_name']] = {}

                    inputs_list[goto_trace_child.attrib['base_name']]['type'] = value_type
                    inputs_list[goto_trace_child.attrib['base_name']]['value'] = actual_value

            print(function_name)
            print(inputs_list)
            return inputs_list

jbmc_path = sys.argv[1]
filepath = sys.argv[2]

compile_and_run_java(jbmc_path, filepath)
filename = filepath.split(".")[0]
counterexample_inputs = get_inputs(filename)

generate_java(filename, counterexample_inputs)



