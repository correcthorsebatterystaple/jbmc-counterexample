import csv
def generate_java_source(test_class_name: str, out_class_name: str, counterexample_inputs, reason: str) -> str:
    """Generate java souce code from counter example inputs"""
    source_builder = []
    source_builder.append(f'// Counterexample for: {reason}')
    source_builder.append(f'class {out_class_name} {{')
    source_builder.append('\tpublic static void main(String[] args) {')
    var_name = "classVar"
    var_index = 0
    for input_var in counterexample_inputs:
        input_type = counterexample_inputs[input_var]['type']
        input_value = counterexample_inputs[input_var]['value']
        if isinstance(input_value, dict):
            source_builder.extend(generate_obj_init(input_var, input_value, indent=2))
            continue

        if isinstance(input_value, list):
            array_type = input_value[0]
            array_value = input_value[1]
            print("arr:", array_value)
            for index, el in enumerate(array_value):
                if isinstance(el, dict):
                    var_name_to_generate = var_name + str(var_index)
                    var_index += 1
                    source_builder.extend(generate_obj_init(var_name_to_generate, el, indent=2))
                    array_value[index] = var_name_to_generate

            array_value = '{' + ', '.join([str(x) for x in array_value]) + '}'

            input_value = "new " + array_type + array_value

        if input_type == "reference[]":
            # array = input_value[input_value.find("{"):]
            # actual_array_value = list(csv.reader([array[1:-1]], delimiter=',', quotechar='"'))[0]
            # print(actual_array_value)
            # for el in actual_array_value:
            #     if isinstance(el, dict):
            #         source_builder.extend(generate_obj_init(input_var, input_value, indent=2))
            #         continue
            input_type = input_value.split("new ")[1].split("{")[0]
        lhs = f"{input_type} {input_var}"
        rhs = f"{input_value}"
        expr = f"{lhs} = {rhs}"
        source_builder.append(f"\t\t{expr};")

    arg_list = ", ".join(counterexample_inputs.keys())
    source_builder.append(f'\t\t{test_class_name}.test({arg_list});')
    source_builder.append('\t}')
    source_builder.append('}')

    return '\n'.join(source_builder)

def generate_obj_init(input_name, value: dict, indent = 0) -> list:
    source = []
    indent_str = "\t" * indent
    source.append(f'{indent_str}{value["__class"]} {input_name} = new {value["__class"]}();')

    for k, v in value.items():
        if k == '__class':
            continue

        if isinstance(v, str):
            source.append(f'{indent_str}{input_name}.{k} = {v};')

        if isinstance(v, dict):
            source.extend(generate_obj_init(f'{k}_{input_name}', v, indent))
            source.append(f'{indent_str}{input_name}.{k} = {k}_{input_name};')

    return source

