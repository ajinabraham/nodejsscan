import json
import argparse
from core.scanner import general_code_analysis


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", nargs='+',
                        help="Node.js source code directory to scan", required=False)
    parser.add_argument("-o", "--output",
                        help="Output file to save JSON report", required=False)
    args = parser.parse_args()
    if args.directory:
        scan_results = general_code_analysis(args.directory)
        if args.output:
            with open("./" + str(args.output) + ".json", 'w') as outfile:
                json.dump(scan_results, outfile, sort_keys=True,
                          indent=4, separators=(',', ': '))
        else:
            print(json.dumps(scan_results, sort_keys=True,
                             indent=4, separators=(',', ': ')))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

