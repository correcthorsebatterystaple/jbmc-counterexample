from subprocess import run

def get_trace_xml(jbmc_path: str, class_name: str) -> str:
    return run([jbmc_path, f'{class_name}.test', '--xml-ui'], capture_output=True, text=True).stdout