import xml.etree.ElementTree as ET
from lxml import etree
import subprocess
import sys
from java_generator import generate_java_source

# Code to generate a java file with inputs for the test function of the supplied class
def generate_java(filename, counterexample_inputs):
    code = generate_java_source(filename, counterexample_inputs)

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

    with open(filename + ".xml", "w") as f:
        f.write(xml_text.stdout)


def get_inputs(filename):
    file = open(filename + ".xml", "rb")
    tree = ET.parse(file)
    root = tree.getroot()

    failed_results = filter(lambda r: r.get('status') == 'FAILURE', root.findall('result'))
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

        return inputs_list

jbmc_path = sys.argv[1]
filepath = sys.argv[2]

compile_and_run_java(jbmc_path, filepath)
filename = filepath.split(".")[0]
counterexample_inputs = get_inputs(filename)

generate_java(filename, counterexample_inputs)



