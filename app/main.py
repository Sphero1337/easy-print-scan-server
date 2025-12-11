import gradio as gr
import os
from datetime import datetime
from functools import partial
from PIL import Image
import sys

from .utils import load_config, ensure_directories, check_auth

# Import platform-specific backends conditionally so that
# Windows-only dependencies are not required on Unix systems.
if sys.platform.startswith("win"):
    from app.backends.windows_printing import WindowsPrintingBackend
    from app.backends.windows_scanning import WindowsScanningBackend
else:
    from app.backends.unix_printing import UnixPrintingBackend
    from app.backends.unix_scanning import UnixScanningBackend


class PrinterScannerApp:
    def __init__(self, printer: str | None = None, scanner: str | None = None):
        self.config = load_config()
        ensure_directories(self.config)

        # Allow overriding printer and scanner via command-line arguments
        if printer:
            self.config.setdefault('printing', {})
            self.config['printing']['default_printer'] = printer

        if scanner:
            self.config.setdefault('scanning', {})
            if sys.platform.startswith("win"):
                # On Windows, scanner is the numerical device index
                try:
                    self.config['scanning']['device_num'] = int(scanner)
                except ValueError:
                    # If it's not an int, leave config as-is
                    pass
            else:
                # On Unix, scanner is the SANE device name
                self.config['scanning']['unix_device_name'] = scanner

        # Select platform-specific backends
        if sys.platform.startswith("win"):
            self.print_backend = WindowsPrintingBackend(self.config)
            self.scan_backend = WindowsScanningBackend(self.config)
        else:
            self.print_backend = UnixPrintingBackend(self.config)
            self.scan_backend = UnixScanningBackend(self.config)

        self.setup_app()

    def print_file(self, username, files):
        if self.config['server']['auth_enabled'] and not username:
            return "Authentication required"

        try:
            file_paths = []
            for file in files:
                # Check file extension
                _, ext = os.path.splitext(file.name)
                if ext.lower() not in self.config['printing']['allowed_extensions']:
                    return f"File type {ext} not allowed"

                # Gradio's file objects expose a .name which is the temp file path
                file_paths.append(file.name)

            return self.print_backend.print_files(file_paths)

        except Exception as e:
            return f"Error printing file: {str(e)}"

    def scan_document(self, username, colormode):
        if self.config['server']['auth_enabled'] and not username:
            return "Authentication required"

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(
                self.config['storage']['scan_dir'],
                f"scan_{timestamp}.jpg"
            )

            ok, msg = self.scan_backend.scan_document(colormode, output_file)

            if not ok:
                return None, None, msg

            # load the image to add it into preview
            image = Image.open(output_file)
            pdfPath = output_file.replace(".jpg", ".pdf")
            image.save(pdfPath, "PDF", resolution=300.0)

            return [output_file, pdfPath], image, "Scan completed successfully"

        except Exception as e:
            return None, None, [f"Error scanning document: {str(e)}"]

    def setup_app(self):
        self.app = gr.Blocks()

        with self.app:
            username_state = gr.State(None)

            if self.config['server']['auth_enabled']:
                with gr.Row():
                    username_input = gr.Textbox(
                        label="Username",
                        type="text"
                    )
                    password_input = gr.Textbox(
                        label="Password",
                        type="password"
                    )
                    login_button = gr.Button("Login")
                    logout_button = gr.Button("Logout")
                    auth_status = gr.Textbox(
                        label="Status",
                        interactive=False
                    )

                def login(username, password, current_username):
                    if current_username:
                        return current_username, "Already logged in"
                    if check_auth(username, password, self.config):
                        return username, f"Welcome, {username}!"
                    return None, "Invalid credentials"

                def logout(current_username):
                    if current_username:
                        return None, "Logged out successfully"
                    return None, "Not logged in"

                login_button.click(
                    fn=login,
                    inputs=[username_input, password_input, username_state],
                    outputs=[username_state, auth_status]
                )

                logout_button.click(
                    fn=logout,
                    inputs=[username_state],
                    outputs=[username_state, auth_status]
                )

            gr.Markdown("# Document Printing and Scanning Service")

            with gr.Tab("Print Document"):
                file_input = gr.File(label="Upload files to print", file_count='multiple')
                print_button = gr.Button("Print")
                print_output = gr.Textbox(label="Status")
                print_button.click(
                    fn=partial(self.print_file),
                    inputs=[username_state, file_input],
                    outputs=print_output
                )

            with gr.Tab("Scan Document"):
                with gr.Row():
                    with gr.Column():
                        color_dropdown = gr.Dropdown(choices=[
                            ("Grayscale (ca 12s)", 2),
                            ("Color (ca 17s)", 1),
                            ("Black and White (ca 6s)", 4)])
                        scan_button = gr.Button("Start Scan")
                    with gr.Column():
                        scan_output = gr.File(label="Document Download")
                scan_result = gr.Textbox(label="Scan Result")
                scan_image = gr.Image(label="File Preview")
                scan_button.click(
                    fn=partial(self.scan_document),
                    inputs=[username_state, color_dropdown],
                    outputs=[scan_output, scan_image, scan_result]
                )

    def run(self):
        ssl_config = {}
        if self.config['server']['ssl_enabled']:
            ssl_config = {
                "ssl_certfile": self.config['server']['ssl_cert'],
                "ssl_keyfile": self.config['server']['ssl_key']
            }

        # If port is falsy (e.g. 0 or None), let Gradio choose a free port.
        port = self.config['server'].get('port')

        launch_kwargs = {
            "server_name": self.config['server']['host'],
            "auth": None,  # We're handling auth ourselves
            "share": self.config['server']['external_access'],
            **ssl_config,
        }

        if port:
            launch_kwargs["server_port"] = port

        self.app.launch(**launch_kwargs)