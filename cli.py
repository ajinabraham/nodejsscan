import json
import argparse
from core.scanner import general_code_analysis

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", nargs='+',
                        help="Path to Node.js Source Code to Scan", required=True)
    parser.add_argument("-r","--results",
                        help="Generate Json report for DevSecOps CI/CD pipelines", required=False )
    args = parser.parse_args()
    if args.directory and not args.results:
        scan_results = general_code_analysis(args.directory)
        print (json.dumps(scan_results))
    elif args.directory and args.results:
    	scan_results = general_code_analysis(args.directory)
    	with open(str(args.results)+".json", 'w') as outfile:
			json.dump(scan_results, outfile,sort_keys=True, indent=4, separators=(',', ': '))
    else:
        parser.print_help()
