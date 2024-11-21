import gradio as gr
import os
import subprocess
from datetime import datetime
import win32print
import win32api
import yaml
from functools import partial
from .utils import load_config, ensure_directories, check_auth

class PrinterScannerApp:
    def __init__(self):
        self.config = load_config()
        ensure_directories(self.config)
        self.setup_app()

    def print_file(self, username, file):
        if not username:
            return "Authentication required"
            
        try:
            file_path = os.path.join(
                self.config['storage']['upload_dir'], 
                file.name
            )
            
            # Check file extension
            _, ext = os.path.splitext(file.name)
            if ext.lower() not in self.config['printing']['allowed_extensions']:
                return f"File type {ext} not allowed"

            # Save the uploaded file
            with open(file_path, "wb") as f:
                f.write(file.read())
            
            # Get printer
            printer = (self.config['printing']['default_printer'] or 
                      win32print.GetDefaultPrinter())
            
            # Print file
            win32api.ShellExecute(
                0,
                "print",
                file_path,
                f'/d:"{printer}"',
                ".",
                0
            )
            
            return f"File sent to printer: {printer}"
        
        except Exception as e:
            return f"Error printing file: {str(e)}"

    def scan_document(self, username):
        if not username:
            return "Authentication required"
            
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(
                self.config['storage']['scan_dir'],
                f"scan_{timestamp}.{self.config['scanning']['default_format']}"
            )
            
            scan_command = f'start ms-screenclip:'
            subprocess.run(scan_command, shell=True)
            
            return output_file
        
        except Exception as e:
            return f"Error scanning document: {str(e)}"

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
                file_input = gr.File(label="Upload file to print")
                print_button = gr.Button("Print")
                print_output = gr.Textbox(label="Status")
                print_button.click(
                    fn=partial(self.print_file),
                    inputs=[username_state, file_input],
                    outputs=print_output
                )
            
            with gr.Tab("Scan Document"):
                scan_button = gr.Button("Start Scan")
                scan_output = gr.File(label="Scanned Document")
                scan_button.click(
                    fn=partial(self.scan_document),
                    inputs=[username_state],
                    outputs=scan_output
                )

    def run(self):
        ssl_config = {}
        if self.config['server']['ssl_enabled']:
            ssl_config = {
                "ssl_certfile": self.config['server']['ssl_cert'],
                "ssl_keyfile": self.config['server']['ssl_key']
            }

        self.app.launch(
            server_name=self.config['server']['host'],
            server_port=self.config['server']['port'],
            auth=None,  # We're handling auth ourselves
            share=self.config['server']['external_access'],
            **ssl_config
        )