# lprof_ext/cli.py
import os
import sys
import argparse
from pathlib import Path

# custom lib
from . import __version__
from .profiler import find_python_scripts, process_script, remove_caches, profiler
from .lib_prof import load_stats, dump_stats

def main():
    parser = argparse.ArgumentParser(
        description="Profile Python scripts by adding @profile decorators and collecting performance stats",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"{__version__}",
    )
    
    parser.add_argument(
        "entry_script",
        type=str,
        help="Path to the main Python script to profile"
    )

    parser.add_argument(
        "--keep-cache",
        action="store_true",
        help="Keep profiling cache files (.lprof and snapshot.temp.json)"
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="Directory to store profiling output files"
    )

    args = parser.parse_args()

    # Validate input
    input_path = Path(args.entry_script).resolve()
    if not input_path.exists():
        print(f"Error: {input_path} does not exist.")
        sys.exit(1)

    if not input_path.is_file() or input_path.suffix != '.py':
        print("Error: Please provide a valid .py file.")
        sys.exit(1)

    project_dir = os.getcwd()
    sys.path.append(project_dir)
    main_script = str(input_path)

    try:
        # Find scripts
        scripts = find_python_scripts(project_dir)
        if not scripts:
            print(f"[ERROR] - No Python scripts found in {project_dir}.")
            sys.exit(1)

        # Process non-entry scripts
        for script_path in scripts:
            if script_path != main_script:
                print(f"[INFO] - Processing {script_path}...")
                process_script(script_path)

        # Process entry script
        print("[INFO] - Processing the entry script...")
        process_script(main_script, entry_script=True)

        # Save and display stats
        output_path = Path(args.output_dir) / f"{input_path.name}.lprof"
        print(f"[INFO] - Dumping profile stats...  {str(output_path)}")
        profiler.dump_stats(str(output_path))
        lstats = load_stats(str(output_path))

        print(f"[INFO] - Dumping profile stats to JSON")
        dump_stats(lstats.timings, str(main_script))
        print("[INFO] - JSON stats saved to `./profile.json`")
        print("""
-------------------- [FINISH] --------------------
Run the following command to view the profile stats in GUI:

> docker run --rm -d --name prof_gui -v ./profile.json:/profile.json -p 8080:8080 ruprof/prof_gui:rust
> http://0.0.0.0:8080/
""")


        # Clean up
        if not args.keep_cache:
            remove_caches(project_dir)

    except Exception as e:
        print(f"Error during profiling: {e}")
        raise e
        sys.exit(1)

if __name__ == "__main__":
    main()