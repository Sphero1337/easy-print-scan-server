from app import scanner


class WindowsScanningBackend:
    def __init__(self, config):
        self.config = config

    def scan_document(self, colormode, target_file_path):
        ok, msg = scanner.scan_document_without_selection(
            self.config['scanning']["device_num"],
            target_file_path,
            colormode,
        )
        return ok, msg
