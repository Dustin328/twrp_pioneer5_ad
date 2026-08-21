import sys
import os
import re

def patch_twrp_functions(path):
    print(f"Opening {path} for patching...")
    if not os.path.exists(path):
        print(f"ERROR: {path} not found!")
        return

    with open(path, 'r') as f:
        content = f.read()

    # Search for the function name regardless of return type or argument style
    func_name = "TWFunc::Try_Decrypting_File"
    start_idx = content.find(func_name)

    if start_idx == -1:
        print(f"ERROR: Could not find '{func_name}' in {path}")
        # Let's list some lines around where it should be
        return

    print(f"Found '{func_name}' at index {start_idx}")

    # Find the opening brace of the function
    brace_idx = content.find("{", start_idx)
    if brace_idx == -1:
        print("ERROR: Could not find opening brace after function name")
        return

    # Match nested braces to find the end of the function
    brace_count = 0
    end_idx = -1
    for i in range(brace_idx, len(content)):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                end_idx = i + 1
                break

    if end_idx == -1:
        print("ERROR: Could not find matching closing brace")
        return

    print(f"Found end of function at index {end_idx}")

    # Replace the entire function block with a clean stub
    # We keep the original start (everything before the function name)
    # but we need to find where the return type starts.
    # A safe bet is to find the previous newline.
    bol_idx = content.rfind("\n", 0, start_idx) + 1

    stub = "bool TWFunc::Try_Decrypting_File(const std::string& fn, const std::string& password) {\n    return false;\n}\n"

    new_content = content[:bol_idx] + stub + content[end_idx:]

    with open(path, 'w') as f:
        f.write(new_content)
    print("Successfully stubbed the function. No more oaes_* calls should exist.")

def clean_android_mk(path):
    if not os.path.exists(path):
        return
    print(f"Cleaning {path}...")
    with open(path, 'r') as f:
        lines = f.readlines()

    with open(path, 'w') as f:
        for line in lines:
            if "libopenaes" in line:
                print(f"Removing line: {line.strip()}")
                f.write("# Removed libopenaes\n")
            else:
                f.write(line)

if __name__ == "__main__":
    base_dir = sys.argv[1] # Path to ~/twrp/bootable/recovery
    patch_twrp_functions(os.path.join(base_dir, "twrp-functions.cpp"))
    clean_android_mk(os.path.join(base_dir, "Android.mk"))
