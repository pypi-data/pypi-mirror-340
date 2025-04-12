from pyprlink.tcp_client import ask_PV
from pyprlink import __version__
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='PyPrLink - TCP/IP client for communicating with PrairieView')
    parser.add_argument('command', nargs='+', help='Command and arguments to send to PrairieView')
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    
    args = parser.parse_args()
    
    try:
        ask_PV(*args.command)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()        