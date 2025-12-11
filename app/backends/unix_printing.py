import subprocess


class UnixPrintingBackend:
    def __init__(self, config):
        self.config = config

    def print_files(self, file_paths):
        printer = self.config['printing'].get('default_printer') or None

        for path in file_paths:
            cmd = ["lp"]
            if printer:
                cmd += ["-d", printer]
            cmd.append(path)

            try:
                result = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=True,
                )
            except FileNotFoundError:
                return "Printing command 'lp' not found. Install CUPS or configure printing manually."
            except subprocess.CalledProcessError as e:
                return f"Error printing {path}: {e.stderr.strip() or e.stdout.strip()}"

        return f"Files sent to printer{(' ' + printer) if printer else ''}"
