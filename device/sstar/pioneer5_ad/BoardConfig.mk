#
# Copyright (C) 2026 The TWRP Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

DEVICE_PATH := device/sstar/pioneer5_ad

# Architecture
TARGET_ARCH := arm
TARGET_ARCH_VARIANT := armv7-a-neon
TARGET_CPU_ABI := armeabi-v7a
TARGET_CPU_ABI2 := armeabi
TARGET_CPU_VARIANT := generic
TARGET_USES_64_BIT_BINDER := true

# Assert
TARGET_OTA_ASSERT_DEVICE := pioneer5_ad

# Kernel
# Match stock cmdline exactly
BOARD_KERNEL_CMDLINE := androidboot.boot_devices=soc/soc:emmc,soc0/soc/soc:emmc init=/init console=ttyS0,115200 androidboot.console=ttyS0 printk.devkmsg=on 8250.nr_uarts=0 androidboot.hardware=sstar
BOARD_KERNEL_BASE := 0x20000000
BOARD_KERNEL_PAGESIZE := 2048
BOARD_KERNEL_OFFSET := 0x02000000
BOARD_RAMDISK_OFFSET := 0x05000000
BOARD_TAGS_OFFSET := 0x00000100
BOARD_BOOTIMG_HEADER_VERSION := 2
TARGET_PREBUILT_KERNEL := $(DEVICE_PATH)/kernel
# Full DTB extracted from stock recovery_backup.img with magiskboot:
#     magiskboot unpack recovery_backup.img
#     cat stock_unpacked/dtb_* > device/sstar/pioneer5_ad/dtb_full
TARGET_PREBUILT_DTB := $(DEVICE_PATH)/dtb_full
BOARD_MKBOOTIMG_ARGS := --ramdisk_offset $(BOARD_RAMDISK_OFFSET) --tags_offset $(BOARD_TAGS_OFFSET) --header_version $(BOARD_BOOTIMG_HEADER_VERSION) --dtb $(TARGET_PREBUILT_DTB)

# AVB
BOARD_AVB_ENABLE := false # Disabled to match stock headers which have no AVB footer

# Platform
TARGET_BOARD_PLATFORM := ums512
TARGET_BOOTLOADER_BOARD_NAME := ums512_1h10
TARGET_COPY_OUT_VENDOR := vendor

# Metadata
BOARD_USES_METADATA_PARTITION := true

# Partitions
BOARD_FLASH_BLOCK_SIZE := 131072 # (Page Size * 64)
BOARD_RECOVERYIMAGE_PARTITION_SIZE := 41943040 # 40MB based on recovery_backup.img size

# Dynamic Partitions
BOARD_USES_DYNAMIC_PARTITIONS := true
BOARD_SUPER_PARTITION_GROUPS := sstar_dynamic_partitions
BOARD_SSTAR_DYNAMIC_PARTITIONS_SIZE := 5359720512
BOARD_SSTAR_DYNAMIC_PARTITIONS_PARTITION_LIST := system vendor odm elable

# Root Symlinks
BOARD_ROOT_EXTRA_SYMLINKS := \
    /vendor/bin/adbd:/system/bin/adbd \
    /mnt/vendor/persist:/persist

# System as root
BOARD_SUPPORTS_VBOOT := true

# Compression - Aggressive LZMA to fit 40MB
BOARD_RECOVERYIMAGE_COMPRESSION := lzma
TARGET_RECOVERY_COMPRESSION := lzma
BOARD_RAMDISK_COMPRESSION := lzma

# TWRP Configuration
TW_THEME := portrait_hdpi
TW_EXTRA_LANGUAGES := false
TW_SCREEN_BLANK_ON_BOOT := true
TW_INPUT_BLACKLIST := "hbtp_vm"
TW_BRIGHTNESS_PATH := "/sys/class/backlight/backlight/brightness"
TW_MAX_BRIGHTNESS := 255
TW_DEFAULT_BRIGHTNESS := 162
TW_EXCLUDE_DEFAULT_USB_INIT := true
TW_INCLUDE_CRYPTO := false
TW_USE_TOOLBOX := true
TW_EXCLUDE_APPLYPATCH := true
TW_EXCLUDE_ENCRYPTED_BACKUPS := true
TW_NO_EXFAT_FUSE := true
TW_EXCLUDE_MTP := true
TW_EXCLUDE_FASTBOOTD := true
TW_EXCLUDE_NANO := true
TW_EXCLUDE_PYTHON := true
TW_NO_BASH := true
TW_NO_HAPTICS := true
TW_EXCLUDE_TZDATA := true
TW_EXCLUDE_LOGCAT := true
TW_NO_LEGACY_PROPERTIES := true
TW_EXCLUDE_WAIT_FOR_SERVICE := true

# Recovery
TARGET_RECOVERY_FSTAB := $(DEVICE_PATH)/recovery.fstab
