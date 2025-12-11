import win32print
import win32api


class WindowsPrintingBackend:
    def __init__(self, config):
        self.config = config

    def print_files(self, file_paths):
        printer = (
            self.config['printing'].get('default_printer')
            or win32print.GetDefaultPrinter()
        )

        for path in file_paths:
            win32api.ShellExecute(
                0,
                "print",
                path,
                f'/d:"{printer}"',
                ".",
                0,
            )

        return f"Files sent to printer: {printer}"
