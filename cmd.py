import json
import argparse
from core.scanner import general_code_analysis

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", nargs='+',
                        help="Path to Node.js Source Code to Scan", required=True)
    args = parser.parse_args()
    if args.directory:
        scan_results = general_code_analysis(args.directory)
        print (json.dumps(scan_results))
    else:
        parser.print_help()
