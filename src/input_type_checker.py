def is_array_type(type_text: str) -> bool:
    return type_text.startswith('struct java::array')

def is_class_type(type_text: str) -> bool:
    return type_text.startswith('struct') and not is_array_type(type_text)

def is_primitive_type(type_text: str) -> bool:
    PRIMITIVE_TYPES = set(['int', 'char', 'short', 'byte', 'double', 'float'])
    return type_text in PRIMITIVE_TYPES

def is_string_type(type_text: str) -> bool:
    return type_text.startswith("struct java.lang.String")

