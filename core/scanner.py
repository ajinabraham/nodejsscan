#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""
The Core Static Analyzer
"""
import os
import re
import xml.dom.minidom
import jsbeautifier
import core.utils as utils
import core.settings as settings


def read_rules():
    """Load Static Scan Rules"""
    scan_rules = {}
    vuln_regex = {}
    vuln_mul_regex = {}
    vuln_dyn_regex = {}
    vuln_rules = {}
    missing_sec_header = {}
    good_to_have_rgx = {}
    desc = {}
    tag = {}
    dom_tree = xml.dom.minidom.parse(settings.RULES_FILE)
    collection = dom_tree.documentElement
    rules_collection = collection.getElementsByTagName("rule")
    for rule in rules_collection:
        if rule.hasAttribute("name"):
            rule_name = rule.getAttribute("name")
            signature = rule.getElementsByTagName('signature')[0]
            vuln_rules[rule_name] = signature.childNodes[0].data
            description = rule.getElementsByTagName('description')[0]
            desc[rule_name] = description.childNodes[0].data
            tag_dat = rule.getElementsByTagName('tag')[0]
            tag[rule_name] = tag_dat.childNodes[0].data
    regexs = collection.getElementsByTagName("regex")
    for regex in regexs:
        if regex.hasAttribute("name"):
            regex_name = regex.getAttribute("name")
            signature = regex.getElementsByTagName('signature')[0]
            vuln_regex[regex_name] = signature.childNodes[0].data
            description = regex.getElementsByTagName('description')[0]
            desc[regex_name] = description.childNodes[0].data
            tag_dat = regex.getElementsByTagName('tag')[0]
            tag[regex_name] = tag_dat.childNodes[0].data

    mul_regexs = collection.getElementsByTagName("mulregex")
    for mul_regex in mul_regexs:
        if mul_regex.hasAttribute("name"):
            temp_regex_dict = {}
            mul_regex_name = mul_regex.getAttribute("name")
            sig_source = mul_regex.getElementsByTagName('sig_source')[0]
            temp_regex_dict["sig_source"] = sig_source.childNodes[0].data
            sig_line = mul_regex.getElementsByTagName('sig_line')[0]
            temp_regex_dict["sig_line"] = sig_line.childNodes[0].data
            vuln_mul_regex[mul_regex_name] = temp_regex_dict
            description = mul_regex.getElementsByTagName('description')[0]
            desc[mul_regex_name] = description.childNodes[0].data
            tag_dat = mul_regex.getElementsByTagName('tag')[0]
            tag[mul_regex_name] = tag_dat.childNodes[0].data

    dyn_regexs = collection.getElementsByTagName("dynregex")
    for dyn_regex in dyn_regexs:
        if dyn_regex.hasAttribute("name"):
            temp_regex_dict = {}
            dyn_regex_name = dyn_regex.getAttribute("name")
            signature = dyn_regex.getElementsByTagName('signature')[0]
            temp_regex_dict["signature"] = signature.childNodes[0].data
            dyn_sig = dyn_regex.getElementsByTagName('dyn_sig')[0]
            temp_regex_dict["dyn_sig"] = dyn_sig.childNodes[0].data
            vuln_dyn_regex[dyn_regex_name] = temp_regex_dict
            description = dyn_regex.getElementsByTagName('description')[0]
            desc[dyn_regex_name] = description.childNodes[0].data
            tag_dat = dyn_regex.getElementsByTagName('tag')[0]
            tag[dyn_regex_name] = tag_dat.childNodes[0].data

    sec_headers = collection.getElementsByTagName("missing_header")
    for header in sec_headers:
        if header.hasAttribute("name"):
            signature = header.getElementsByTagName('signature')[0]
            missing_sec_header[header.getAttribute(
                "name")] = signature.childNodes[0].data
            description = header.getElementsByTagName('description')[0]
            desc[header.getAttribute("name")] = description.childNodes[0].data
            tag_dat = header.getElementsByTagName('tag')[0]
            tag[header.getAttribute("name")] = tag_dat.childNodes[0].data

    good_to_have = collection.getElementsByTagName("good_to_have")
    for good in good_to_have:
        if good.hasAttribute("name"):
            signature = good.getElementsByTagName('signature')[0]
            good_to_have_rgx[good.getAttribute("name")] = signature.childNodes[
                0].data
            description = good.getElementsByTagName('description')[0]
            desc[good.getAttribute("name")] = description.childNodes[0].data
            tag_dat = good.getElementsByTagName('tag')[0]
            tag[good.getAttribute("name")] = tag_dat.childNodes[0].data
    scan_rules["vuln_rules"] = vuln_rules
    scan_rules["vuln_regex"] = vuln_regex
    scan_rules["vuln_mul_regex"] = vuln_mul_regex
    scan_rules["vuln_dyn_regex"] = vuln_dyn_regex
    scan_rules["missing_sec_header"] = missing_sec_header
    scan_rules["good_to_have_rgx"] = good_to_have_rgx
    scan_rules["desc"] = desc
    scan_rules["tag"] = tag
    return scan_rules


def get_lines(line_no, lines):
    """Get Lines before and after the given line"""
    lines = lines[max(0, line_no - 5): min(len(lines), line_no + 5)]
    lines = '\n'.join(lines)
    try:
        lines = jsbeautifier.beautify(lines)
    except:
        pass
    return lines


def is_valid_node(filename, file_path):
    """Make sure file is a Valid Node.js File"""
    # Files that doesn't needs to be scanned
    ignore_files = ["jquery.min.js", "bootstrap.js", "bootstrap-tour.js",
                    "raphael-min.js", "tinymce.min.js", "tinymce.js",
                    "codemirror-compressed.js", "codemirror.js"]
    ext = os.path.splitext(filename)[1]
    is_js_file = bool(ext.lower() in settings.JS_SCAN_FILE_EXTENSIONS)
    ignore_file = bool(filename.lower() not in ignore_files)
    is_node_www = bool(file_path.lower().endswith("bin/www"))
    valid = (is_js_file or is_node_www) and ignore_file
    if valid:
        data = utils.unicode_safe_file_read(file_path)
        if re.search(r"require\(('|\")(.+?)('|\")\)|module\.exports {0,5}= {0,5}", data):
            # Possible Node.js Source Code
            return data
    return None


def is_valid_template_file(filename, file_path):
    """Check if it's a valid template file"""
    data = None
    ext = os.path.splitext(filename)[1]
    if ext.lower() in settings.OTHER_SCAN_FILE_EXTENSIONS:
        data = utils.unicode_safe_file_read(file_path)
    return data

def general_code_analysis(paths):
    """Static Code Analysis"""
    try:
        scan_results = {}
        scan_rules = read_rules()
        security_issues = []
        good_finding = []
        missing_header = []
        all_files = []
        # Initializing Security Header flag as not present
        header_found = {}
        sec_issues_by_tag = {}
        good_finding_by_tag = {}
        missing_header_by_tag = {}
        vuln_n_count = {}
        count = {}
        # Sort By Tag
        tags = {'rce': 'Remote Command Execution',
                'rci': 'Remote Code Injection',
                'ssrf': 'Server Side Request Forgery',
                'module': 'Vulnerable Node Module',
                'node': 'Application Related',
                'web': 'Web Security',
                'dir': 'Directory Traversal',
                'opr': 'Open Redirect Vulnerability',
                'sqli': 'SQL Injection (SQLi)',
                'xss': 'Cross Site Scripting (XSS)',
                'nosqli': 'NoSQL Injection',
                'hhi': 'HTTP Header Injection',
                }
        for path in paths:
            for header in scan_rules["missing_sec_header"].iterkeys():
                header_found[header] = 0
            print "\n[INFO] Running Static Analyzer Running on - " + path + "\n"
            for root, _, files in os.walk(path):
                for filename in files:
                    full_file_path = os.path.join(root, filename)
                    relative_path = full_file_path.replace(path, "")
                    all_files.append({relative_path.replace(
                        "/", "", 1): full_file_path.replace(settings.UPLOAD_FOLDER, "", 1)})
                    nodejs_data = is_valid_node(filename, full_file_path)
                    template_data = is_valid_template_file(filename, full_file_path)
                    if nodejs_data or template_data:
                        if nodejs_data:
                            data = nodejs_data
                        else:
                            data = template_data
                        # print relative_path
                        beautified_data = None
                        lines = data.splitlines()
                        if len(lines) <= 2:
                            # Possible Minified Single Line Code
                            try:
                                # Try Because of Possible Bug in JS Beautifier
                                beautified_data = jsbeautifier.beautify(data)
                                lines = beautified_data.splitlines()
                            except:
                                pass
                        for line_no, line in enumerate(lines):
                            # Avoid Comments - Multiline is a problem still
                            if not line.lstrip().startswith("//") and not line.lstrip().startswith("/*"):
                                # Limit the no of caracters in a line to 2000
                                line = line[0:2000]
                                # Vulnerability String Match
                                for rule_key in scan_rules["vuln_rules"].iterkeys():
                                    if scan_rules["vuln_rules"][rule_key] in line:
                                        finding = {}
                                        finding["title"] = rule_key
                                        finding["description"] = scan_rules[
                                            "desc"][rule_key]
                                        finding["tag"] = scan_rules[
                                            "tag"][rule_key]
                                        finding["line"] = line_no + 1
                                        finding["lines"] = get_lines(
                                            line_no, lines)
                                        finding["filename"] = filename
                                        finding["path"] = full_file_path.replace(
                                            settings.UPLOAD_FOLDER, "", 1)
                                        finding["sha2"] = utils.gen_sha256_hash(
                                            finding["lines"].encode(encoding="utf-8", errors="replace"))
                                        security_issues.append(finding)
                                # Vulnerability Regex Match
                                for regex in scan_rules["vuln_regex"].iterkeys():
                                    if re.search(scan_rules["vuln_regex"][regex], line):
                                        finding = {}
                                        finding["title"] = regex
                                        finding["description"] = scan_rules[
                                            "desc"][regex]
                                        finding["tag"] = scan_rules[
                                            "tag"][regex]
                                        finding["line"] = line_no + 1
                                        finding["lines"] = get_lines(
                                            line_no, lines)
                                        finding["filename"] = filename
                                        finding["path"] = full_file_path.replace(
                                            settings.UPLOAD_FOLDER, "", 1)
                                        finding["sha2"] = utils.gen_sha256_hash(
                                            finding["lines"].encode(encoding="utf-8", errors="replace"))
                                        security_issues.append(finding)
                                # Vulnerability Multi Regex Match
                                for mulregex in scan_rules["vuln_mul_regex"].iterkeys():
                                    sig_source = scan_rules["vuln_mul_regex"][
                                        mulregex]["sig_source"]
                                    sig_line = scan_rules["vuln_mul_regex"][
                                        mulregex]["sig_line"]
                                    if re.search(sig_source, data):
                                        if re.search(sig_line, line):
                                            finding = {}
                                            finding["title"] = mulregex
                                            finding["description"] = scan_rules[
                                                "desc"][mulregex]
                                            finding["tag"] = scan_rules[
                                                "tag"][mulregex]
                                            finding["line"] = line_no + 1
                                            finding["lines"] = get_lines(
                                                line_no, lines)
                                            finding["filename"] = filename
                                            finding["path"] = full_file_path.replace(
                                                settings.UPLOAD_FOLDER, "", 1)
                                            finding["sha2"] = utils.gen_sha256_hash(
                                                finding["lines"].encode(encoding="utf-8", errors="replace"))
                                            security_issues.append(finding)
                                # Dynamic Regex
                                for dynregex in scan_rules["vuln_dyn_regex"].iterkeys():
                                    signature = scan_rules["vuln_dyn_regex"][
                                        dynregex]["signature"]
                                    dyn_sig = scan_rules["vuln_dyn_regex"][
                                        dynregex]["dyn_sig"]
                                    sig = re.search(signature, line)
                                    if sig:
                                        index = line.find(sig.group())
                                        dyn_variable = line[0:index]
                                        dyn_variable = dyn_variable.replace(
                                            "var", "").replace("=", "").strip()
                                        if re.match(r'^[\w]+$', dyn_variable):
                                            dyn_sig = dyn_variable + dyn_sig
                                            for line_no, nline in enumerate(lines):
                                                if re.search(dyn_sig, nline):
                                                    finding = {}
                                                    finding["title"] = dynregex
                                                    finding["description"] = scan_rules[
                                                        "desc"][dynregex]
                                                    finding["tag"] = scan_rules[
                                                        "tag"][dynregex]
                                                    finding[
                                                        "line"] = line_no + 1
                                                    finding["lines"] = get_lines(
                                                        line_no, lines)
                                                    finding[
                                                        "filename"] = filename
                                                    finding[
                                                        "path"] = full_file_path.replace(settings.UPLOAD_FOLDER, "", 1)
                                                    finding["sha2"] = utils.gen_sha256_hash(
                                                        finding["lines"].encode(encoding="utf-8", errors="replace"))
                                                    security_issues.append(
                                                        finding)
                                # Good Finding String Match
                                for good_find in scan_rules["good_to_have_rgx"].iterkeys():
                                    if re.search(scan_rules["good_to_have_rgx"][good_find], line):
                                        finding = {}
                                        finding["title"] = good_find
                                        finding["description"] = scan_rules[
                                            "desc"][good_find]
                                        finding["tag"] = scan_rules[
                                            "tag"][good_find]
                                        finding["line"] = line_no + 1
                                        finding["lines"] = get_lines(
                                            line_no, lines)
                                        finding["filename"] = filename
                                        finding["path"] = full_file_path.replace(
                                            settings.UPLOAD_FOLDER, "", 1)
                                        finding["sha2"] = utils.gen_sha256_hash(
                                            finding["lines"].encode(encoding="utf-8", errors="replace"))
                                        good_finding.append(finding)
                                # Missing Security Headers String Match
                                for header in scan_rules["missing_sec_header"].iterkeys():
                                    if re.search(scan_rules["missing_sec_header"][header], line, re.I):
                                        # Good Header is present
                                        header_found[header] = 1
                        # Write Beautifed Data If Any
                        if beautified_data is not None:
                            utils.unicode_safe_file_write(
                                full_file_path, beautified_data)
        # After Every Files are done.
        # Check for missing Security Headers
        for header in header_found.iterkeys():
            if header_found[header] == 0:
                finding = {}
                finding["title"] = header
                finding["description"] = scan_rules["desc"][header]
                finding["tag"] = scan_rules["tag"][header]
                missing_header.append(finding)
        #Vulnerability and Count
        for issue in security_issues:
            if not issue["title"] in vuln_n_count:
                vuln_n_count[issue["title"]] = 0
            vuln_n_count[issue["title"]] += 1

        for issue in security_issues:
            if not tags[issue["tag"]] in sec_issues_by_tag:
                sec_issues_by_tag[tags[issue["tag"]]] = []
            sec_issues_by_tag[tags[issue["tag"]]].append(issue)

        for find in good_finding:
            if not tags[find["tag"]] in good_finding_by_tag:
                good_finding_by_tag[tags[find["tag"]]] = []
            good_finding_by_tag[tags[find["tag"]]].append(find)

        for sec_header in missing_header:
            if not tags[sec_header["tag"]] in missing_header_by_tag:
                missing_header_by_tag[tags[sec_header["tag"]]] = []
            missing_header_by_tag[tags[sec_header["tag"]]].append(sec_header)

        count["sec"] = len(security_issues)
        count["mis"] = len(missing_header)
        count["good"] = len(good_finding)

        scan_results["sec_issues"] = sec_issues_by_tag
        scan_results["good_finding"] = good_finding_by_tag
        scan_results["missing_sec_header"] = missing_header_by_tag
        scan_results["total_count"] = count
        scan_results["vuln_count"] = vuln_n_count
        scan_results["files"] = all_files
        return scan_results
    except:
        utils.print_exception("Error Performing Code Analysis")
