# lprof_ext/profiler.py
# built-in libraries
import os
from pathlib import Path
import builtins

# third party libraries
import libcst as cst
import libcst.matchers as m
from line_profiler import LineProfiler

# custom libraries
from .lib_prof import find_script, update_json_file

# Initialize profiler
profiler = LineProfiler()
builtins.profile = profiler

class AddProfileDecorator(cst.CSTTransformer):
    """CST Transformer to add @profile decorator to function definitions."""
    def leave_FunctionDef(self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef) -> cst.FunctionDef:
        has_profile = any(
            m.matches(deco, m.Decorator(decorator=m.Name("profile")))
            for deco in updated_node.decorators
        )
        if not has_profile:
            new_decorators = [cst.Decorator(decorator=cst.Name("profile"))] + list(updated_node.decorators)
            return updated_node.with_changes(decorators=new_decorators)
        return updated_node

def check_source_code(content: str) -> bool:
    """Check if source code already contains @profile decorator."""
    content = [line.strip() for line in content.splitlines()]
    if "@profile" in content:
        return False
    return True

def process_script(script_path: str, entry_script: bool = False) -> bool:
    """Process a Python script by adding @profile decorators and executing it."""
    script_file = find_script(script_path)
    try:
        with open(script_path, "r") as f:
            source = f.read()

        if not check_source_code(source):
            print(f"Skipping {script_path} due to existing @profile decorator.")
            return False

        # Parse and modify CST
        tree = cst.parse_module(source)
        transformer = AddProfileDecorator()
        modified_tree = tree.visit(transformer)
        modified_code = modified_tree.code

        update_json_file(script_path, modified_code)

        # Execute with proper context
        if entry_script:
            local_vars = {"__file__": script_file, "__name__": "__main__"}
        else:
            local_vars = {}

        exec(compile(modified_code, script_path, "exec"), local_vars, local_vars)
        return True

    except Exception as e:
        print(f"Error processing {script_path}: {str(e)}")
        raise e
        return False

def find_python_scripts(project_dir: str): # -> list[str]:
    """Find all .py files in project directory, excluding .venv/."""
    project_path = Path(project_dir).resolve()
    python_files = []
    for py_file in project_path.rglob("*.py"):
        if ".venv" not in str(py_file.relative_to(project_path)).split(os.sep):
            python_files.append(str(py_file))
    return python_files

def remove_caches(project_dir: str):
    """Remove profiling cache files (.lprof, snapshot.temp.json)."""
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith((".lprof", "snapshot.temp.json")):
                os.remove(os.path.join(root, file))