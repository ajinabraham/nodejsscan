#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""Command-line interface for nodejsscan."""
import json
import sys
import argparse
from core.scanner import scan_dirs, scan_file
import core.settings as settings


def output(out, scan_results):
    """Output"""
    if out:
        # out is the fully qualified path and filename for the output file. We recommend you use a .json extension
        with open(out, 'w') as outfile:
            json.dump(scan_results, outfile, sort_keys=True,
                      indent=4, separators=(',', ': '))
    else:
        print((json.dumps(scan_results, sort_keys=True,
                          indent=4, separators=(',', ': '))))

def handle_exit(results):
    if len(results['vuln_count']) > 0:
        sys.exit(1)

    sys.exit(0)

def main():
    """Main CLI"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file",
                        nargs='+',
                        help="Node.js file(s) to scan",
                        required=False)
    parser.add_argument("-d", "--directory",
                        nargs='+',
                        help="Node.js source code directory/directories to scan",
                        required=False)
    parser.add_argument("-o", "--output",
                        help="Output file to save JSON report",
                        required=False)
    parser.add_argument("-v", "--version",
                        help="Show nodejsscan version",
                        required=False,
                        action='store_true')
    args = parser.parse_args()
    if args.directory:
        scan_results = scan_dirs(args.directory)
        output(args.output, scan_results)
        handle_exit(scan_results)
    elif args.file:
        scan_results = scan_file(args.file)
        output(args.output, scan_results)
        handle_exit(scan_results)
    elif args.version:
        print("nodejsscan v" + settings.VERSION)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
