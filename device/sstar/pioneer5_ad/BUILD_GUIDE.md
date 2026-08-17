# Build Guide for TWRP (SigmaStar Pioneer5 AD)

Since this device tree is generated for a specific SigmaStar board, you can use a GitHub Actions compiler to build your recovery image without needing a Linux machine.

## Prerequisites
1. A GitHub account.
2. The `recovery_backup.img` you already have.

## Steps

### 1. Fork a TWRP Compiler Repository
Fork one of the following reputable repositories:
* [ColdWindScholar/TWRP-Compiler](https://github.com/ColdWindScholar/TWRP-Compiler) (Recommended for Android 11/12)
* [NoahDomingues/Auto-TWRP-Builder](https://github.com/NoahDomingues/Auto-TWRP-Builder)

### 2. Prepare your Device Tree
You need to upload the files I generated to a new repository or within the forked one.
The structure should be:
`device/sstar/pioneer5_ad/` containing all the `.mk` files and `recovery.fstab`.

### 3. Configure the Workflow
In the `.github/workflows/main.yml` (or similar) of your forked repo, set these variables:
* **MANIFEST_URL**: `https://github.com/minimal-twrp/platform_manifest_twrp_omni`
* **MANIFEST_BRANCH**: `twrp-12.1` (since your SDK is 32/Android 12L)
* **DEVICE_PATH**: `device/sstar/pioneer5_ad`
* **DEVICE_NAME**: `pioneer5_ad`
* **MAKEFILE_NAME**: `omni_pioneer5_ad`
* **BUILD_TARGET**: `recovery`

### 4. Run the Action
1. Go to the **Actions** tab.
2. Select the "Build TWRP" workflow.
3. Click "Run workflow".
4. Once finished, download the `recovery.img` from the **Artifacts** or **Releases** section.

### 5. Flashing (CAUTION)
Flash it using fastboot:
```bash
fastboot flash recovery recovery.img
fastboot reboot recovery
```

> [!WARNING]
> Always keep your stock `recovery_backup.img` safe. If the new TWRP doesn't boot, you can flash the stock one back using:
> `fastboot flash recovery recovery_backup.img`
