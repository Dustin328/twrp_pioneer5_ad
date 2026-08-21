import sys
import os
import re

def patch_file(path, pattern, replacement):
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return
    with open(path, 'r') as f:
        content = f.read()
    new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)
    with open(path, 'w') as f:
        f.write(new_content)
    print(f"Patched {path}")

def patch_twrp_functions(path):
    if not os.path.exists(path):
        return
    with open(path, 'r') as f:
        content = f.read()

    # Use a robust regex to find the entire Try_Decrypting_File function and replace it with a stub
    # This handles cases where the opening brace is on a different line and nested braces
    pattern = r'bool\s+TWFunc::Try_Decrypting_File\s*\([^)]*\)\s*\{.*?\}\n'
    # Actually, matching nested braces with regex is hard. Let's use a simpler marker-based approach
    # since we know the structure.

    start_marker = "bool TWFunc::Try_Decrypting_File"
    start_idx = content.find(start_marker)
    if start_idx != -1:
        # Find the first { after the marker
        brace_idx = content.find("{", start_idx)
        if brace_idx != -1:
            # Find the matching }
            # For simplicity in this specific file, we look for the next } at the start of a line
            end_idx = content.find("\n}", brace_idx)
            if end_idx != -1:
                end_idx += 2 # include the brace
                stub = "bool TWFunc::Try_Decrypting_File(const string& fn, const string& password) {\n\treturn false; // AES Support Removed\n}\n"
                new_content = content[:start_idx] + stub + content[end_idx:]
                with open(path, 'w') as f:
                    f.write(new_content)
                print(f"Successfully stubbed Try_Decrypting_File in {path}")
                return

    print(f"Warning: Could not find Try_Decrypting_File in {path}")

if __name__ == "__main__":
    twrp_dir = sys.argv[1] # Path to ~/twrp/bootable/recovery

    # 1. Patch the C++ code
    patch_twrp_functions(os.path.join(twrp_dir, "twrp-functions.cpp"))

    # 2. Patch the Build System to remove libopenaes dependency
    android_mk = os.path.join(twrp_dir, "Android.mk")
    if os.path.exists(android_mk):
        with open(android_mk, 'r') as f:
            lines = f.readlines()
        with open(android_mk, 'w') as f:
            for line in lines:
                if "libopenaes" in line:
                    f.write("# Removed libopenaes\n")
                else:
                    f.write(line)
        print(f"Removed libopenaes from {android_mk}")
