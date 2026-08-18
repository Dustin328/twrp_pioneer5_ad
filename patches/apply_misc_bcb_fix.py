#!/usr/bin/env python3
"""
Unisoc misc/BCB fix for PBRP's tw_reboot().

Root cause: PitchBlackRecoveryProject/android_bootable_recovery's
TWFunc::tw_reboot() (twrp-functions.cpp) never calls
TWFunc::Clear_Bootloader_Message() for any RebootCommand target. Most SoCs
tolerate this because their bootloader looks at the reboot *reason* string,
not just "is misc non-empty". Unisoc's splloader does not: it unconditionally
boots into recovery whenever misc still holds a leftover BCB command, no
matter what target was actually requested (confirmed via dmesg:
bootcause="Detect the recovery message in the misc partition" after using
recovery once, regardless of which menu item was pressed). Because misc is
never cleared, every subsequent reboot - system, bootloader, fastbootd alike -
gets redirected back into recovery, and recovery never reaches a clean exit
to persist its own settings either.

This script inserts an unconditional Clear_Bootloader_Message() call as the
first statement inside tw_reboot(), before any step that could fail partway
through and leave misc dirty (DataManager::Flush, Update_Log_File). It skips
rb_recovery, since that path legitimately needs the BCB kept intact for the
next boot (fastbootd menu detection reads it).

Usage: python3 apply_misc_bcb_fix.py <path-to-twrp-functions.cpp>
Idempotent: safe to run more than once; a second run is a no-op.
"""
import sys

MARKER = "Unisoc misc/BCB fix"
SIGNATURE = "int TWFunc::tw_reboot(RebootCommand command)"

INSERTION = f'''
\t// [{MARKER} - fortuneship ums91581h10]
\t// See apply_misc_bcb_fix.py for the full root-cause writeup. Short
\t// version: upstream tw_reboot() never clears misc for any target, and
\t// Unisoc's splloader boots into recovery whenever misc has a leftover
\t// BCB command regardless of the actually-requested target. Clear it
\t// unconditionally, up front, except when re-entering recovery on
\t// purpose (rb_recovery), where the BCB needs to stay intact.
\tif (command != rb_recovery) {{
\t\tTWFunc::Clear_Bootloader_Message();
\t}}
'''


def main():
    if len(sys.argv) != 2:
        print("usage: apply_misc_bcb_fix.py <path-to-twrp-functions.cpp>", file=sys.stderr)
        sys.exit(2)

    path = sys.argv[1]
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if MARKER in content:
        print("info: patch already applied, skipping (idempotent)")
        return

    sig_idx = content.find(SIGNATURE)
    if sig_idx == -1:
        print(
            f"error: could not find '{SIGNATURE}' in {path}. "
            "This branch's twrp-functions.cpp may have a different "
            "tw_reboot() signature - needs manual review before patching.",
            file=sys.stderr,
        )
        sys.exit(1)

    brace_idx = content.find("{", sig_idx)
    if brace_idx == -1:
        print(
            "error: found tw_reboot() signature but no opening brace after it",
            file=sys.stderr,
        )
        sys.exit(1)

    new_content = content[: brace_idx + 1] + INSERTION + content[brace_idx + 1 :]
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"success: misc/BCB fix inserted into tw_reboot() in {path}")


if __name__ == "__main__":
    main()
