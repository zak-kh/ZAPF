# ZAPF - z4 Admin Panel Finder

ZAPF (z4 Admin Panel Finder) is a command-line tool designed to discover common admin panels on websites. It performs a brute-force search by trying various URLs based on a wordlist and provides feedback on the status of each URL.

## Features

- Efficiently searches for admin panels using a wordlist
- Supports HTTP and HTTPS URLs
- Allows proxy usage for requests
- Color-coded output for easy identification of results

## Requirements

- Python 3.6 or higher
- Dependencies (install using `pip install -r requirements.txt`):
  - requests
  - termcolor
  - tqdm
  - pyfiglet
  - socks
  - tabulate

## Usage

1. Clone or download the ZAPF repository.

2. Install the required dependencies by running the following command:

python3 zapf.py -r 

or

pip install -r requirements.txt

3. Run ZAPF with the desired command-line options. The minimum required option is the URL of the target website:

Optional Arguments:
- `--wordlist`: Path to the wordlist file (default: admin_common.txt).
- `--proxy`: Proxy URL for requests. Supports HTTP, SOCKS4, and SOCKS5 proxies.

4. ZAPF will start searching for admin panels using the specified wordlist. Progress will be displayed, and any discovered panels will be shown in a tabular format at the end of the process.

## Example Usage

python zapf.py -u https://example.com --wordlist wordlist.txt --proxy socks5://localhost:1080


## Contributing

Contributions to ZAPF are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request on the GitHub repository.

## License

ZAPF is released under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Credits

ZAPF was developed by [Your Name] and is inspired by the need to efficiently discover admin panels for website security assessment.

---

**Note:** The requirements for ZAPF can be found in the `requirements.txt` file. Install them using `pip install -r requirements.txt`.
