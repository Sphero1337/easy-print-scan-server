import win32com.client
import pythoncom
from enum import Enum

class ImageMode(Enum):
    COLOR = 1
    GRAYSCALE = 2
    BLACK_AND_WHITE = 4

def scan_document_without_selection(device_num, target_file_path, ImageMode=ImageMode.COLOR):
    try:
        # Initialize WIA Automation
        pythoncom.CoInitialize()
        wia_manager = win32com.client.Dispatch("WIA.DeviceManager")
        # Connect to the scanner using the Device ID
        
        device = wia_manager.DeviceInfos[device_num].Connect()
        
        if len(wia_manager.DeviceInfos) < device_num - 1:
            return "No device with device num %d found. Check scanner device index!" % device_num
        
        # Get the first item from the scanner
        item = device.Items[0]
        
        #list_properties(item)

        # Adjust scanner settings (e.g., DPI, color mode)
        item.Properties["6146"].Value = ImageMode  # 1 = Color, 2 = Grayscale, 4 = Black/White
        item.Properties["6147"].Value = 300  # DPI X (300x300 resolution)
        item.Properties["6148"].Value = 300  # DPI Y
        item.Properties["6149"].Value = 0    # xPos
        item.Properties["6150"].Value = 0    # yPos
        
        # Execute the scan
        image = item.Transfer()
        
        # Save the scanned file
        image.SaveFile(target_file_path)
        return True, f"Document scanned and saved to {target_file_path}"
    
    except Exception as e:
        return False, f"Error: {e}"


def list_properties(item):
    for prop in item.Properties:
        print(f"Property: {prop.Name} (ID: {prop.PropertyID})")
        print(f"Value: {prop.Value}")
        print(f"Is ReadOnly: {prop.IsReadOnly}")
        print("-" * 30)

#if __name__ == "__main__":
#    # Replace this with your scanner's Device ID
#    device_num = 0
#    result = scan_document_without_selection("scan.pdf", device_num)
#    print(result)
