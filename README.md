# Printer Scanner Web Interface

A simple web interface for printing and scanning documents using Windows native functions. Built with Python and Gradio.

## Features

- Upload and print documents
- Scan documents using Windows native scanning
- Simple web interface
- Configurable settings

## Requirements

- Windows 10 Pro
- Python 3.7+
- Connected printer
- Connected scanner or all-in-one device

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/printer-scanner-web.git
cd printer-scanner-web
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Configuration

Edit `config/config.yaml` to customize:
- Server host and port
- Storage directories
- Printing settings
- Scanning settings

## Usage

1. Start the application:
```bash
python run.py
```

2. Open your web browser and navigate to `http://localhost:7860` (or your configured host/port)

3. Use the interface to:
   - Upload and print documents
   - Scan documents

## Limitations

- Currently supports Windows 10 Pro only
- Uses default printer unless specified in config
- Basic scanning functionality using Windows native app

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Gradio team for the wonderful web interface library
- Windows for providing native printing and scanning capabilities

## Security Features

### Authentication
The application supports basic authentication with username and password:
- Enable/disable authentication in config.yaml
- Default credentials (change these in production):
  - Username: admin
  - Password: admin123

### External Access
The application can be configured for external access:
- Set `external_access: true` in config.yaml to enable
- Configure SSL for secure connections
- Use appropriate firewall settings

### SSL Support
For secure connections:
1. Set `ssl_enabled: true` in config.yaml
2. Provide paths to SSL certificate and key
3. Use HTTPS to access the application

## Configuration Options

### Server Settings
```yaml
server:
  host: "0.0.0.0"  # Use 0.0.0.0 for external access
  port: 7860
  external_access: false  # Enable for external access
  auth_enabled: true     # Enable authentication
  username: "admin"      # Change in production
  password: "admin123"   # Change in production
  ssl_enabled: false     # Enable for HTTPS
  ssl_cert: ""          # Path to SSL certificate
  ssl_key: ""           # Path to SSL private key
```
```

5. Add security-related packages to `requirements.txt`:

```
gradio>=3.50.2
PyYAML>=6.0.1
pywin32>=306
cryptography>=3.4.7  # For SSL support