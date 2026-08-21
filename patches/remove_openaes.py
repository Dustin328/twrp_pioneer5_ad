import sys
import os

def patch_twrp_functions(path):
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return

    with open(path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    skip = False
    for line in lines:
        if "TWFunc::Try_Decrypting_File" in line:
            new_lines.append(line)
            new_lines.append("{\n")
            new_lines.append("\treturn false; // AES Support Removed\n")
            new_lines.append("}\n")
            new_lines.append("/* Removed legacy AES code\n")
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
    print(f"Successfully patched {path}")

if __name__ == "__main__":
    patch_twrp_functions(sys.argv[1])
