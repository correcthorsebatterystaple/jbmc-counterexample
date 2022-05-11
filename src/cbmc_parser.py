import sys
from java_generator import generate_java_source
from java_compiler import compile_java_class
from jbmc_runner import get_trace_xml
from input_parser import get_inputs

def main(argv):
    jbmc_path = argv[1]
    file_path = argv[2]
    filename = file_path.split('.')[0]

    compile_java_class(file_path)
    trace_xml_source = get_trace_xml(jbmc_path, filename)

    counterexample_inputs = get_inputs(trace_xml_source)

    for i, counterexample_input in enumerate(counterexample_inputs):
        reason = counterexample_input['reason']
        inputs = counterexample_input['inputs']
        print(reason)
        out_class_name = f'CounterExample{i}'
        source = generate_java_source(
            test_class_name=filename, 
            out_class_name=out_class_name, 
            counterexample_inputs=inputs, reason=reason
        )
        with open(out_class_name + '.java', 'w') as file:
            file.write(source)

if __name__ == '__main__':
    main(sys.argv)



