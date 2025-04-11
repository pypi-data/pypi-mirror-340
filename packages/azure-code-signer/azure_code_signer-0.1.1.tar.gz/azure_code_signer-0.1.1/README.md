# Azure Code Signer

Azure Code Signer is a command line tool that allows you to code sign files using a code signing certificate stored in Azure Key Vault. This tool is designed to work across multiple platforms, including Linux, macOS, and Windows.

## Features

- Authenticate with Azure Key Vault to retrieve code signing certificates.
- Sign files using the retrieved certificates.
- Verify the signatures of signed files.

## Installation

To install the Azure Code Signer, clone the repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/azure-code-signer.git
cd azure-code-signer
pip install -r requirements.txt
```

## Usage

To use the Azure Code Signer, run the following command in your terminal:

```bash
python src/main.py <file_to_sign>
```

Replace `<file_to_sign>` with the path to the file you want to sign.

## Authentication

The tool uses Azure Key Vault for authentication. Ensure you have the necessary permissions to access the Key Vault and retrieve the code signing certificate.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.