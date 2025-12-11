import subprocess


class UnixScanningBackend:
    def __init__(self, config):
        self.config = config

    def _mode_from_colormode(self, colormode):
        if colormode == 1:
            return "Color"
        if colormode == 2:
            return "Gray"
        if colormode == 4:
            return "Lineart"
        return "Color"

    def scan_document(self, colormode, target_file_path):
        device_name = self.config['scanning'].get('unix_device_name')
        resolution = self.config['scanning'].get('resolution', 300)

        if not device_name:
            return False, "No Unix SANE device configured (scanning.unix_device_name)."

        mode = self._mode_from_colormode(colormode)

        cmd = [
            "scanimage",
            f"--device-name={device_name}",
            "--format=jpeg",
            f"--mode={mode}",
            f"--resolution={resolution}",
        ]

        try:
            with open(target_file_path, "wb") as out:
                subprocess.run(
                    cmd,
                    stdout=out,
                    stderr=subprocess.PIPE,
                    check=True,
                )
        except FileNotFoundError:
            return False, "scanimage command not found. Install SANE (e.g., sane-utils)."
        except subprocess.CalledProcessError as e:
            return False, f"Error from scanner: {e.stderr.decode(errors='ignore').strip()}"

        return True, f"Document scanned and saved to {target_file_path}"
