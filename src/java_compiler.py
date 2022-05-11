import subprocess

def compile_java_class(file_path: str) -> None:
    """Compiles java source at `file_path` and generates `.class` file"""
    subprocess.run(['javac', file_path])