import win32com.client

def list_scanners():
    wia_manager = win32com.client.Dispatch("WIA.DeviceManager")
    for device_info in wia_manager.DeviceInfos:
        print(f"Device Name: {device_info.Properties['Name'].Value}")
        print(f"Device ID: {device_info.DeviceID}")
        print("-" * 30)

list_scanners()