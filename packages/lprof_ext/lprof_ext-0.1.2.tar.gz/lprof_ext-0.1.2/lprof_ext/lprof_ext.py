#!/usr/bin/env python3
# built-in libraries
import sys
import builtins
import os
from pathlib import Path

# third party libraries
from line_profiler import LineProfiler
import libcst as cst
import libcst.matchers as m

# custom library
from .lib_prof import load_stats, show_text, find_script, update_json_file

profiler = LineProfiler()
builtins.profile = profiler  # load profile when builtin

def check_source_code(content: str) -> bool:
    """Check for existing @profile decorator in the source code"""
    content = [line.strip() for line in content.splitlines()]
    if "@profile" in content:
        print("@profile decorator found in the script.")
        return False
    return True

class AddProfileDecorator(cst.CSTTransformer):
    def leave_FunctionDef(self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef) -> cst.FunctionDef:
        # Check for existing @profile decorator
        has_profile = any(
            m.matches(deco, m.Decorator(decorator=m.Name("profile")))
            for deco in updated_node.decorators
        )
        if not has_profile:
            # Add @profile
            new_decorators = [cst.Decorator(decorator=cst.Name("profile"))] + list(updated_node.decorators)
            return updated_node.with_changes(decorators=new_decorators)
        return updated_node

def process_script(script_path, entry_script=False):
    script_file = find_script(script_path)
    with open(script_path, "r") as f:
        source = f.read()
    if not check_source_code(source):
        print(f"Skipping {script_path} due to existing @profile decorator.")
        return False
    # Parse CST
    tree = cst.parse_module(source)

    # Apply decorator
    transformer = AddProfileDecorator()
    modified_tree = tree.visit(transformer)

    # Turn CST to Python code (w/ comments)
    modified_code = modified_tree.code
    update_json_file(script_path, modified_code)

    # Add __name__, __file__ to locals()
    if entry_script:
        __file__ = script_file
        __name__ = '__main__'
    # local_vars = {"__file__": script_file, "__name__": "__main__"}
    exec(compile(modified_code, script_path, "exec"), locals(), locals())
    return True

def find_python_scripts(project_dir):
    """Find all .py files in the project directory, excluding .venv/"""
    project_path = Path(project_dir).resolve()
    python_files = []
    for py_file in project_path.rglob("*.py"):
        # Skip files in .venv/
        if ".venv" not in str(py_file.relative_to(project_path)).split(os.sep):
            python_files.append(str(py_file))
    return python_files

def remove_caches(project_dir):
    """Remove all *.lprof, snapshot.temp.json  files in the project directory."""
    # from glob import glob
    import os
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            if file.endswith(".lprof") or file.endswith("snapshot.temp.json"):
                os.remove(os.path.join(root, file))

if __name__ == "__main__":
    input_path = Path(sys.argv[1]).resolve()
    if not input_path.exists():
        print(f"Error: {input_path} does not exist.")
        sys.exit(1)

    # If it's a file, treat its parent as project dir
    if input_path.is_file():
        main_script = str(input_path)
        project_dir = input_path.parent
    else:
        print("Please pass the entry script (like test.py) as argument.")
        sys.exit(1)

    # Find all Python scripts
    scripts = find_python_scripts(project_dir)
    if not scripts:
        print(f"No Python scripts found in {project_dir}.")
        sys.exit(1)

    # Process each script except the entry script
    for script_path in scripts:
        if script_path == str(input_path):
            continue
        print(f"Processing {script_path}...")
        process_script(script_path)

    # Process entry script
    print("Processing the entry script...")
    process_script(str(input_path), True)

    # dump profile stats
    print("Dumping profile stats...")
    profiler.dump_stats(f"{script_path}.lprof")
    lstats = load_stats(f"{script_path}.lprof")
    show_text(lstats.timings)

    remove_caches(project_dir)