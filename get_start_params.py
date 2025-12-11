#!/usr/bin/env python

"""Helper script to discover printer and scanner parameters.

Run this script to see:
- Available printers and how to pass them as --printer
- Available scanners and how to pass them as --scanner

Examples (adapt paths/venv as needed):
  python run.py --printer "HP_LaserJet" --scanner "genesys:libusb:001:002"   # Unix
  python run.py --printer "HP_LaserJet" --scanner 0                           # Windows
"""

import os
import sys
import subprocess
from typing import List, Tuple


def is_windows() -> bool:
    return sys.platform.startswith("win")


# ---------------------- Unix helpers ----------------------


def list_unix_printers() -> List[str]:
    """Return a list of printer names using CUPS (lpstat)."""
    try:
        result = subprocess.run(
            ["lpstat", "-p"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
    except FileNotFoundError:
        print("lpstat not found. Install CUPS (e.g., cups, cups-client) to list printers.")
        return []
    except subprocess.CalledProcessError as e:
        print("Error while listing printers with lpstat:")
        print(e.stderr.strip() or e.stdout.strip())
        return []

    printers: List[str] = []
    for line in result.stdout.splitlines():
        # Typical line: "printer HP_LaserJet_Pro is idle.  enabled since ..."
        parts = line.split()
        if len(parts) >= 2 and parts[0] == "printer":
            printers.append(parts[1])
    return printers


def list_unix_scanners() -> List[Tuple[str, str]]:
    """Return a list of (device_name, description) from scanimage -L."""
    try:
        result = subprocess.run(
            ["scanimage", "-L"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
    except FileNotFoundError:
        print("scanimage not found. Install SANE utilities (e.g., sane-utils) to list scanners.")
        return []
    except subprocess.CalledProcessError as e:
        # Some SANE backends print info to stderr on success; try to parse stdout anyway.
        output = e.stdout or ""
        if not output:
            print("Error while listing scanners with scanimage:")
            print(e.stderr.strip())
            return []
        raw = output
    else:
        raw = result.stdout

    devices: List[Tuple[str, str]] = []
    for line in raw.splitlines():
        line = line.strip()
        # Example: "device `genesys:libusb:001:002' is a Canon ..."
        if line.startswith("device `") and "' is" in line:
            try:
                dev_part, desc_part = line.split("' is", 1)
                device_name = dev_part[len("device `") :]
                description = desc_part.strip().lstrip("a ")
                devices.append((device_name, description))
            except ValueError:
                continue
    return devices


# ---------------------- Windows helpers ----------------------


def list_windows_printers() -> List[str]:
    try:
        import win32print  # type: ignore
    except ImportError:
        print("win32print is not available. Install pywin32 to list Windows printers.")
        return []

    flags = win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
    printers = win32print.EnumPrinters(flags)
    names: List[str] = []
    for p in printers:
        # p is a tuple; the printer name is usually at index 2
        if len(p) >= 3:
            names.append(p[2])
    return names


def list_windows_scanners() -> List[Tuple[int, str]]:
    """Return a list of (index, name) for WIA scanners."""
    try:
        import win32com.client  # type: ignore
        import pythoncom  # type: ignore
    except ImportError:
        print("win32com / pythoncom not available. Install pywin32 to list scanners.")
        return []

    pythoncom.CoInitialize()
    try:
        wia_manager = win32com.client.Dispatch("WIA.DeviceManager")
        devices: List[Tuple[int, str]] = []
        for i, device_info in enumerate(wia_manager.DeviceInfos):
            try:
                name = device_info.Properties["Name"].Value
            except Exception:
                name = "Unknown device"
            devices.append((i, name))
        return devices
    finally:
        pythoncom.CoUninitialize()


# ---------------------- Main CLI ----------------------


def main() -> None:
    print("=== Easy Print & Scan: Helper for start parameters ===")
    print(f"Detected platform: {sys.platform}\n")

    if is_windows():
        printers = list_windows_printers()
        scanners = list_windows_scanners()

        print("Available printers (use with --printer):")
        if printers:
            for name in printers:
                print(f"  - {name}")
        else:
            print("  (no printers found or pywin32 not installed)")
        print()

        print("Available scanners (use index with --scanner):")
        if scanners:
            for idx, name in scanners:
                print(f"  - index {idx}: {name}")
        else:
            print("  (no scanners found or pywin32 not installed)")
        print()

        print("Example start command:")
        print("  python run.py --printer \"<PRINTER_NAME>\" --scanner <SCANNER_INDEX>")

    else:
        printers = list_unix_printers()
        scanners = list_unix_scanners()

        print("Available printers (use with --printer):")
        if printers:
            for name in printers:
                print(f"  - {name}")
        else:
            print("  (no printers found or CUPS not installed / configured)")
        print()

        print("Available scanners (use SANE device name with --scanner):")
        if scanners:
            for dev, desc in scanners:
                print(f"  - {dev}    ({desc})")
        else:
            print("  (no scanners found or sane-utils not installed / configured)")
        print()

        print("Example start command:")
        print("  python run.py --printer \"<PRINTER_NAME>\" --scanner \"<SANE_DEVICE_NAME>\"")


if __name__ == "__main__":
    main()
