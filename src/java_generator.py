def generate_java_source(test_class_name: str, out_class_name: str, counterexample_inputs, reason: str) -> str:
    """Generate java souce code from counter example inputs"""
    source_builder = []
    source_builder.append(f'// Counterexample for: {reason}')
    source_builder.append(f'class {out_class_name} {{')
    source_builder.append('\tpublic static void main(String[] args) {')

    for input_var in counterexample_inputs:
        input_type = counterexample_inputs[input_var]['type']
        input_value = counterexample_inputs[input_var]['value']
        lhs = f"{input_type} {input_var}"
        rhs = f"{input_value}"
        expr = f"{lhs} = {rhs}"
        source_builder.append(f"\t\t{expr};")

    arg_list = ", ".join(counterexample_inputs.keys())
    source_builder.append(f'\t\t{test_class_name}.test({arg_list});')
    source_builder.append('\t}')
    source_builder.append('}')

    return '\n'.join(source_builder)