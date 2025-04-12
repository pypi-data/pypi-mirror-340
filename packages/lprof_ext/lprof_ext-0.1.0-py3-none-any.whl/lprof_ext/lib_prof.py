import os
import sys
import pickle
from collections import defaultdict
import inspect
# from line_profiler.line_profiler import show_func

import json

def update_json_file(script_path, modified_code, json_file='snapshot.temp.json'):
    # Step 1: Read the existing JSON data
    try:
        with open(json_file, 'r') as infile:
            data = json.load(infile)
    except FileNotFoundError:
        # If the file doesn't exist, start with an empty dictionary
        data = {}
    except json.JSONDecodeError:
        # If the file is empty or invalid, start with an empty dictionary
        data = {}

    # Step 2: Modify the data
    data[script_path] = modified_code

    # Step 3: Write the updated data back to the file
    with open(json_file, 'w') as outfile:
        json.dump(data, outfile, indent=4)  # indent for readability

def load_json(json_file='snapshot.temp.json'):
    with open(json_file, 'r') as infile:
        data = json.load(infile)
    return data

# def update_lineno(stats_order: list, stats:dict):
#     """
#     count the number of functions before the line
#     and add n to the line number.
#     """
#     scripts = load_json()
#     counter = defaultdict(int)
#     stats_order_new = []

#     for (file_name, first_line, func_name), line_stats in stats_order:
#         if line_stats:
#             # with open(file_name, "r") as f:
#             #     source = f.read()
#             source = scripts[file_name]
    
#             correct_lineno = source.split(f"def {func_name}")[0]
#             correct_lineno = len(correct_lineno.split('\n'))

#             # print((file_name, correct_lineno , func_name),line_stats)
#             key = tuple((file_name, correct_lineno , func_name))
#             line_stats_new = [(correct_lineno + lineno - first_line-1, count, totaltime) for (lineno, count, totaltime) in line_stats]
#             stats_order_new.append((key, line_stats_new))

#             line_stats = stats.pop(tuple((file_name, first_line, func_name)))
#             stats[key] = line_stats_new.copy()
#             counter[file_name] += 1
#         else:
#             stats.pop(tuple((file_name, first_line, func_name)))

#     stats_order.clear()
#     stats_order += stats_order_new
stat_dict_template = defaultdict(lambda: #file_name : 
                    defaultdict(lambda:  { # func_name
                        "line": defaultdict(
                            lambda: {}
                        ),
                        # "total_hit": 0,
                        "total_time": 0
                    }))

def transform(stats:dict):
    """
    count the number of functions before the line
    and add n to the line number.

    stats_dict
    {
        <file_name> : 
            <func_name> :
                "line":{
                    <line_no> : dict w/o type
                },
                # "total_hit": int,
                "total_time": int,
    }
    """
    stats_dict = stat_dict_template.copy()
    
    for (file_name, first_line, func_name), line_stats in stats.items():
        if line_stats:
            for line in line_stats:
                line_no, count, totaltime = line
                stats_dict[file_name][func_name]["line"][line_no]['count'] = count
                stats_dict[file_name][func_name]["line"][line_no]['time'] = totaltime
    return stats_dict

def load_stats(filename):
    """ Utility function to load a pickled LineStats object from a given
    filename.
    """
    with open(filename, 'rb') as f:
        return pickle.load(f)

def get_func_sublines(script, index):
    """
    return: distance from `first_line` to `def `
    """
    func_sublines = []
    # Collect lines starting from @deco
    for dist in range(20):
        # print(script[index + i].rstrip())
        line = script[index + dist].strip()
        if not line:  # Skip empty lines
            continue
        if line.startswith("def "):
            # Use inspect.getblock to get the function body
            block = inspect.getblock(script[index + dist:])
            # print(dist, block)
            func_sublines.extend(block)  # Skip the def line since we already added it
            break
    return dist, func_sublines

def number_of_profiles(script, index):
    """ 
    Get the number of profiles from a given script before line `index`.
    """
    line_strip = [line.strip() for line in script[:index]]
    return line_strip.count("@profile")


def show_text(stats):
    """ Show text for the given timings.
    """
    # if stream is None:
        # stream = sys.stdout
    
    stats_order = sorted(stats.items())
    stats_dict = transform(stats)
    scripts = load_json()
    # print(stats_dict)
    clean_dict = stat_dict_template.copy()
     
    for (file_name, start_lineno, func_name), v in stats_order:
        if v:
            all_lines = [ x + "\n" for x in scripts[file_name].split("\n")]
            dist, func_sublines = get_func_sublines(all_lines, start_lineno)
            # print(func_sublines)
            # print()
            # func_time = 0
            
            numprof = number_of_profiles(all_lines, start_lineno)

            # total func hit and time
            # total_hit = sum([x['count']for x in stats_dict[file_name][func_name]["line"].values()])
            total_time = sum([x['time']for x in stats_dict[file_name][func_name]["line"].values()])
            # stats_dict[file_name][func_name]['total_hit'] = total_hit
            stats_dict[file_name][func_name]['total_time'] = total_time
            
            for n, line in enumerate(func_sublines):
                run_line_no = start_lineno + dist + n + 1


                # print(start_lineno, dist, n, run_line_no, line, sep="   \t")
                # print(line_no, stats_dict[file_name][line_no], line, sep="   \t")
                # line_dict = stats_dict[file_name][func_name][run_line_no]
                # if line_dict:
                #     count = line_dict['count']
                #     time = line_dict['time']
                #     func_time += time
                # else:
                #     count = ""
                #     time = ""
                show_line_no = run_line_no - numprof
                # print(show_line_no, count, time, line, sep="\t" )
                for k,v in stats_dict[file_name][func_name]["line"][run_line_no].items():
                    clean_dict[file_name][func_name]["line"][show_line_no][k] = v
                clean_dict[file_name][func_name]["line"][show_line_no]["code"] = line.split("\n")[0]
                # clean_dict[file_name][func_name]['total_hit'] = stats_dict[file_name][func_name]['total_hit']
                clean_dict[file_name][func_name]['total_time'] = stats_dict[file_name][func_name]['total_time']
                # clean_dict[file_name][func_name]["func_time"] = func_time
            # print(stats_dict)
            # print()
    # print(json.dumps(clean_dict))
    for file_name, func_profile in clean_dict.items():
        for func_name, func_dict in func_profile.items():
            # func_time = line_stats
            # print(line_stats.values())
            line_stats = func_dict["line"]
            # print(line_stats)
            # print(file_name, func_name)
            for line_no, stats_dict_ in sorted(line_stats.items()):
                count = stats_dict_.get('count', "")
                time = stats_dict_.get('time', "")
                code = stats_dict_.get('code', "")
                if count:
                    # print(count, time, clean_dict[file_name][func_name]["total_hit"], clean_dict[file_name][func_name]["total_time"])
                    # pct_hit = round(count/clean_dict[file_name][func_name]["total_hit"]*100,1)
                    pct_time =  round(time/clean_dict[file_name][func_name]["total_time"]*100,1)
                else:
                    # pct_hit = ""
                    pct_time = ""
                # clean_dict[file_name][func_name]["line"][line_no]["pct_hit"] = pct_hit
                clean_dict[file_name][func_name]["line"][line_no]["pct_time"] = pct_time
                # print(line_no, count,  time, pct_hit, pct_time, code, sep="\t")
                # print(line_no, count,  time, pct_time, code, sep="\t")
            # print("\n\n\n")

    # rename filename
    # print(clean_dict)
    rename_dict = {old_file_path: old_file_path.replace(f"{os.getcwd()}", ".")  \
                    for old_file_path in clean_dict.keys()}
    
    for old_file_path, new_file_path in rename_dict.items():
        clean_dict[new_file_path] = clean_dict.pop(old_file_path)
    
    # clean_dict[]
    # exit()
    with open("profile.json", "w") as f:
        json.dump(clean_dict, f, indent=4)

    # exit()
    # # update_lineno(stats_order, stats)
    # if details:
    #     scripts = load_json()
    #     for (fn, start_lineno, name), timings in stats_order:
    #         print(fn, start_lineno, name, timings)
    #         all_lines = scripts[fn].split("\n")
            
    #         # extract subline 
    #         print(name , start_lineno, all_lines[start_lineno-1])
    #         sublines = inspect.getblock(all_lines[start_lineno - 1:])
    #         # print(sublines)
    #         for line in sublines:
    #             print(line)
    #         exit()
    #         # show_func(fn, lineno, name, stats[fn, lineno, name], unit,
    #         #           output_unit=output_unit, stream=stream,
    #         #           stripzeros=stripzeros, rich=rich)


def find_script(script_name):
    """ Find the script.

    If the input is not a file, then $PATH will be searched.
    """
    if os.path.isfile(script_name):
        return script_name
    path = os.getenv('PATH', os.defpath).split(os.pathsep)
    for dir in path:
        if dir == '':
            continue
        fn = os.path.join(dir, script_name)
        if os.path.isfile(fn):
            return fn

    sys.stderr.write('Could not find script %s\n' % script_name)
    raise SystemExit(1)
