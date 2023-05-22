import requests
import sys
import signal
import os
import argparse
import time
from termcolor import colored
from tqdm import tqdm
from pyfiglet import Figlet
import socks
from urllib.parse import urlparse
import subprocess

quit_requested = False

def signal_handler(signal, frame):
    global quit_requested
    print()
    quit_requested = True
    confirm = input(colored("Do you want to quit? (y/n): ", "yellow"))
    if confirm.lower() == "y":
        sys.exit(0)

def print_banner():
    f = Figlet(font='slant')
    print(colored(f.renderText('ZAPF'), "cyan"))
    print(colored("z4 admin panel finder", "yellow"))
    print()

def parse_arguments():
    parser = argparse.ArgumentParser(description='ZAPF - z4 admin panel finder')
    parser.add_argument('-r', '--requirement', help='Install requirements from requirements.txt', action='store_true')
    parser.add_argument('-u', '--url', help='URL of the website')
    parser.add_argument('--wordlist', help='Path to the wordlist file (default: admin_common.txt)', default='admin_common.txt')
    parser.add_argument('--proxy', help='Proxy URL for requests (http : http://proxy.example.com:8080, https : https://proxy.example.com:8443, socks4 : socks4://localhost:1080, socks5 : socks5://localhost:1080)')
    args = parser.parse_args()
    return args

def install_requirements():
    try:
        print("Installing requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Requirements installed successfully.")
    except subprocess.CalledProcessError as e:
        print("Failed to install requirements. Please check the error message above.")
        sys.exit(1)
    except Exception as e:
        print("An error occurred during requirements installation:")
        print(str(e))
        sys.exit(1)

def check_admin_panel(url, wordlist, proxy):
    wordlist_size = sum(1 for line in open(wordlist))

    with open(wordlist, 'r') as file:
        for word in tqdm(file, total=wordlist_size, unit='word', leave=False, ncols=80):
            if quit_requested:
                break
            word = word.strip()
            if not word or word.startswith('#'):
                continue
            admin_url = url.rstrip('/') + '/' + word
            try:
                signal.signal(signal.SIGINT, signal_handler)  # Register signal handler for each iteration
                response = requests.get(admin_url, proxies=proxy)
                response_code = response.status_code
                if response_code == 200:
                    result = colored(f"\n   ✅ {admin_url} [{response_code}]", "green")
                elif response_code == 404:
                    result = colored(f"\n   ❌ {admin_url} [{response_code}]", "red")
                else:
                    result = colored(f"\n   ⚠️ {admin_url} [{response_code}]", "yellow")
                print(result)
            except requests.exceptions.RequestException:
                result = colored(f"\n   ⚠️ {admin_url} [network not connect]", "yellow")
                print(result)
                continue

def main():
    signal.signal(signal.SIGINT, signal_handler)
    print_banner()
    args = parse_arguments()
    
    if args.requirement:
        install_requirements()
        sys.exit(0)
    
    if not args.url:
        print("URL argument is required. Use -u or --url to specify the URL.")
        sys.exit(1)

    url = args.url
    wordlist = args.wordlist
    proxy_url = args.proxy

    proxy = None
    if proxy_url:
        proxy_type = urlparse(proxy_url).scheme
        proxy_host = urlparse(proxy_url).hostname
        proxy_port = urlparse(proxy_url).port

        if proxy_type == "http":
            proxy = {"http": proxy_url, "https": proxy_url}
        elif proxy_type == "https":
            proxy = {"https": proxy_url}
        elif proxy_type == "socks4":
            socks.set_default_proxy(socks.SOCKS4, proxy_host, proxy_port)
            proxy = {"http": proxy_url, "https": proxy_url}
        elif proxy_type == "socks5":
            socks.set_default_proxy(socks.SOCKS5, proxy_host, proxy_port)
            proxy = {"http": proxy_url, "https": proxy_url}
        else:
            print("Invalid proxy type. Supported types: http, https, socks4, socks5")
            sys.exit(1)

    check_admin_panel(url, wordlist, proxy)

if __name__ == '__main__':
    main()
