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

    # Search for the function name
    func_name = "TWFunc::Try_Decrypting_File"
    start_idx = content.find(func_name)

    if start_idx == -1:
        print(f"ERROR: Could not find '{func_name}' in {path}")
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

    # Find the beginning of the line containing the function definition
    bol_idx = content.rfind("\n", 0, start_idx) + 1

    # The signature must match twrp-functions.hpp exactly:
    # static int Try_Decrypting_File(string fn, string password);
    # Note: TWRP source uses 'using namespace std;' so 'string' is used instead of 'std::string'
    stub = "int TWFunc::Try_Decrypting_File(string fn, string password) {\n    return 0; // AES Support Removed\n}\n"

    new_content = content[:bol_idx] + stub + content[end_idx:]

    with open(path, 'w') as f:
        f.write(new_content)
    print("Successfully stubbed the function with correct signature.")

def clean_android_mk(path):
    if not os.path.exists(path):
        return
    print(f"Cleaning {path}...")
    with open(path, 'r') as f:
        lines = f.readlines()

    with open(path, 'w') as f:
        for line in lines:
            if "libopenaes" in line:
                f.write("# Removed libopenaes\n")
            else:
                f.write(line)

if __name__ == "__main__":
    base_dir = sys.argv[1] # Path to ~/twrp/bootable/recovery
    patch_twrp_functions(os.path.join(base_dir, "twrp-functions.cpp"))
    clean_android_mk(os.path.join(base_dir, "Android.mk"))
