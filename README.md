# PyEYE - Python Endpoint Extractor

![Python](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

PyEYE is a powerful tool designed to extract endpoints and paths from websites by analyzing HTML content and associated resources. It identifies potential API endpoints, routes, and file paths which can be useful for security research, web mapping, and application analysis.

## Features

- Extracts endpoints from main page HTML and all linked resources
- Validates paths based on security criteria
- Follows JavaScript and CSS sources to find additional endpoints
- Rich console output with progress tracking
- Saves results to a customizable output file

## Installation

```bash
# Clone the repository
git clone https://github.com/medjahdi/PyEYE.git

# Navigate to the project directory
cd PyEYE

# Install required packages
pip install -r requirements.txt
```

## Usage

```bash
python app.py https://example.com [-o output_file.txt]
```

### Arguments

- `url`: Target website URL (required)
- `-o, --output`: Output file name (default: endpoints.txt)

### Example

```bash
python app.py https://example.com -o results.txt
```

## Requirements

- Python 3.6+
- requests
- beautifulsoup4
- rich

## Screenshots

(Consider adding screenshots of the tool in action)

## Disclaimer

This tool is for educational purposes only. Always ensure you have permission before scanning websites that do not belong to you. The author is not responsible for any misuse of this software.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support the Project

If you find this tool useful, consider supporting the development:

[![Donate with PayPal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif)](https://www.paypal.com/ncp/payment/W5SHTZX6LZH86)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

@medjahdi