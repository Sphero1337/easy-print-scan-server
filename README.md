# Printer Scanner Web Interface

A simple web interface for printing and scanning documents using Windows native functions. Built with Python and Gradio, this application aims to provide an intuitive interface for users to manage their printing and scanning tasks efficiently.

## Features

- **Upload and Print Documents**: Users can upload files and send them directly to the printer.
- **Scan Documents**: Scan documents using native Windows scanning capabilities.
- **User Authentication**: Basic authentication can be configured for secure access.
- **Configurable Server Settings**: Customize server host, port, and other functionalities through configuration.
- **External Access**: Option to enable the application for external access using SSL for secure connections.

## Requirements

- Windows Host
- Python 3.7+
- A connected printer and scanner (or all-in-one device)

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Sphero1337/easy-print-scan-server.git
    cd easy-print-scan-server
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3. **Install required packages**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Edit the `config/config.yaml` file to customize the following settings:

- **Server Host and Port**:
    ```yaml
    server:
      host: "0.0.0.0"  # Use 0.0.0.0 for external access
      port: 7860
    ```

- **Storage Directories**:
    Specify where uploads and scans will be stored:
    ```yaml
    storage:
      upload_dir: "path/to/upload_dir"
      scan_dir: "path/to/scan_dir"
    ```

- **Printing and Scanning Settings**:
    Adjust settings to control functionality.

### Default Credentials
- Username: `admin`
- Password: `admin123`

### SSL Support
1. Set `ssl_enabled: true` in `config.yaml`.
2. Provide paths for the SSL certificate and key.

## Usage

1. **Start the application**:
    ```bash
    python run.py
    ```

2. **Access the web interface**:
   Open your web browser and navigate to `http://localhost:7860` (or your configured host/port).

3. **Functions in the Interface**:
   - Upload and print documents.
   - Scan documents using the scanning feature.

## Limitations

- This application supports Windows hosts only.
- It uses the default printer unless a specific printer is specified in the configuration.
- The hosts must be able to open the respective documents in order to print them, e.g. if you want to print an excel document, the appropriate software must be installed on the host machine.
- The scanning functionality utilizes Microsoft Windows' native applications.

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Merge Request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- Thanks to the Gradio team for the wonderful web interface library.
- Also big thanks to OpenAI for providing free access to ChatGPT which was used to assist in developing this application.

## Security Features

### Authentication
- The application supports basic authentication with username and password.
- You can enable or disable authentication in the `config.yaml`.

### External Access
- Set `external_access: true` in `config.yaml` to enable external access.
- Ensure SSL is configured for secure connections.
