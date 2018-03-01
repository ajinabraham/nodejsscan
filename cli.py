import json
import argparse
from core.scanner import general_code_analysis

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", nargs='+',
                        help="Path to Node.js Source Code to Scan", required=True)
    parser.add_argument("-r", "--results",
                        help="Generate Json report for DevSecOps CI/CD pipelines", required=False)
    args = parser.parse_args()
    if args.directory:
        scan_results = general_code_analysis(args.directory)
        if args.results:
            with open(str(args.results) + ".json", 'w') as outfile:
                json.dump(scan_results, outfile, sort_keys=True,
                          indent=4, separators=(',', ': '))
        else:
            print(json.dumps(scan_results, sort_keys=True,
                             indent=4, separators=(',', ': ')))
    else:
        parser.print_help()
