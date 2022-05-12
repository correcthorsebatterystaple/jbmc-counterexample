from subprocess import run

def get_trace_xml(jbmc_path: str, class_name: str, options = None) -> str:
    assert options == None or len(options) > 0

    cmd = [jbmc_path, f'{class_name}.test', '--xml-ui']
    if not options == None:
        cmd.extend(options)
    
    return run(cmd, capture_output=True, text=True).stdout