import sys
import os
import re

def patch_file(path, pattern, replacement):
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return
    with open(path, 'r') as f:
        content = f.read()
    new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    with open(path, 'w') as f:
        f.write(new_content)
    print(f"Patched {path}")

def patch_twrp_functions(path):
    if not os.path.exists(path): return
    with open(path, 'r') as f:
        lines = f.readlines()
    new_lines = []
    skip = False
    for line in lines:
        if "TWFunc::Try_Decrypting_File" in line:
            new_lines.append(line)
            new_lines.append("{\n\treturn false; // AES Support Removed\n}\n/*\n")
            skip = True
            continue
        if skip and line.strip() == "}":
            new_lines.append("*/\n")
            skip = False
            continue
        if not skip:
            new_lines.append(line)
    with open(path, 'w') as f:
        f.writelines(new_lines)
    print(f"Patched C++ in {path}")

if __name__ == "__main__":
    twrp_dir = sys.argv[1] # Path to ~/twrp/bootable/recovery

    # 1. Patch the C++ code
    patch_twrp_functions(os.path.join(twrp_dir, "twrp-functions.cpp"))

    # 2. Patch the Build System to remove libopenaes dependency
    # Remove from Android.mk
    patch_file(os.path.join(twrp_dir, "Android.mk"), r'libopenaes', '')

    # Some branches use variables, let's be thorough
    patch_file(os.path.join(twrp_dir, "Android.mk"), r'LOCAL_SHARED_LIBRARIES \+= libopenaes', '# Removed libopenaes')
    patch_file(os.path.join(twrp_dir, "Android.mk"), r'LOCAL_STATIC_LIBRARIES \+= libopenaes', '# Removed libopenaes')
