#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""
The Core Static Analyzer
"""
import os
import re
import ntpath
import defusedxml
import xml.dom.minidom
import jsbeautifier

import core.utils as utils
import core.settings as settings


defusedxml.defuse_stdlib()
MULTI_COMMENT = re.compile(r'/\*[\s\S]+?\*/')
NODE_RGX = re.compile(
    r"require\(('|\")(.+?)('|\")\)|module\.exports {0,5}= {0,5}")


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


def read_tags():
    """Read Tags from XML"""
    tags_dict = {}
    dom_tree = xml.dom.minidom.parse(settings.RULES_FILE)
    collection = dom_tree.documentElement
    tags = collection.getElementsByTagName("tag")
    for tag in tags:
        tags_dict[tag.getAttribute("name")] = tag.childNodes[0].data
    return tags_dict


def get_lines(line_no, lines):
    """Get Lines before and after the given line"""
    lines = lines[max(0, line_no - 5): min(len(lines), line_no + 5)]
    lines = '\n'.join(lines)
    try:
        lines = jsbeautifier.beautify(lines)
    except:
        pass
    return lines


def is_valid_node(file_path):
    """Make sure file is a Valid Node.js File"""
    # Files that doesn't needs to be scanned
    filename = ntpath.basename(file_path)
    ext = os.path.splitext(filename)[1]
    is_js_file = bool(ext.lower() in settings.JS_SCAN_FILE_EXTENSIONS)
    ignore_dirs = any(ignr in file_path for ignr in settings.IGNORE_DIRS)
    ignore_file = bool(filename.lower() in settings.IGNORE_FILES)
    is_node_www = bool(file_path.lower().endswith("bin/www"))
    valid = (is_js_file or is_node_www) and not ignore_file and not ignore_dirs
    if valid:
        data = utils.read_file(file_path)
        if re.search(NODE_RGX, data):
            # Possible Node.js Source Code
            return data
    return None


def is_valid_template_file(file_path):
    """Check if it's a valid template file"""
    data = None
    filename = ntpath.basename(file_path)
    ignore_dirs = any(ignr in file_path for ignr in settings.IGNORE_DIRS)
    ignore_file = bool(filename.lower() in settings.IGNORE_FILES)
    ext = os.path.splitext(filename)[1]
    if (ext.lower() in settings.OTHER_SCAN_FILE_EXTENSIONS and
            not ignore_dirs and
            not ignore_file):
        data = utils.read_file(file_path)
    return data


def beautify_js(data, full_file_path):
    """Beautify JS"""
    lines = data.splitlines()
    if len(lines) <= 2:
        # Possible Minified Single Line Code
        try:
            # Try Because of Possible Bug in JS Beautifier
            beautified_data = jsbeautifier.beautify(data)
            data = beautified_data
            utils.write_file(full_file_path, beautified_data)
        except:
            pass
    return data


def add_findings(title, scan_rules, line_no, lines, full_file_path):
    """Add Findings"""
    filename = ntpath.basename(full_file_path)
    finding = {}
    finding["title"] = title
    finding["description"] = scan_rules[
        "desc"][title]
    finding["tag"] = scan_rules[
        "tag"][title]
    finding["line"] = line_no + 1
    finding["lines"] = get_lines(
        line_no, lines)
    finding["filename"] = filename
    finding["path"] = full_file_path.replace(
        settings.UPLOAD_FOLDER, "", 1)
    finding["sha2"] = utils.gen_sha256_hash(
        finding["lines"])
    return finding


def sanitize_comments(data):
    """Replace Comments : for /**/ and //
    """
    # Replace Multiline Comments
    matches = re.findall(MULTI_COMMENT, data)
    for match in matches:
        match_len = len(match.splitlines())
        new_lst = []
        for _ in range(match_len):
            new_lst.append(" ")
        new_str = "\n".join(new_lst)
        data = data.replace(match, new_str)
    # Replace Single line Comments
    new_lines = []
    lines = data.splitlines()
    for line in lines:
        if line.lstrip().startswith("//"):
            new_lines.append(" ")
        else:
            new_lines.append(line)
    new_data = "\n".join(new_lines)
    return new_lines, new_data


def scan_file(paths):
    """ Scan a File """
    security_issues = []
    scan_rules = read_rules()

    # Initializing Security Header flag as not present
    header_found = {}
    for header in scan_rules["missing_sec_header"].keys():
        header_found[header] = 0
    for path in paths:
        print("\n[INFO] Running Static Code Analysis on - " + path + "\n")
        if os.path.isfile(path):
            nodejs_data = is_valid_node(path)
            template_data = is_valid_template_file(path)
            if nodejs_data or template_data:
                data = nodejs_data if nodejs_data else template_data
                sec, _ = code_analysis(data, path, scan_rules, header_found)
                security_issues += sec
    return security_issues


def scan_dirs(paths):
    """Scan the Dir"""
    scan_results = {}
    all_files = []
    security_issues = []
    good_finding = []
    missing_header = []

    scan_rules = read_rules()
    tags = read_tags()

    # Initializing Security Header flag as not present
    header_found = {}
    for header in scan_rules["missing_sec_header"].keys():
        header_found[header] = 0

    for path in paths:
        print("\n[INFO] Running Static Analyzer on - " + path + "\n")
        for root, _, files in os.walk(path):
            for filename in files:
                full_file_path = os.path.join(root, filename)
                nodejs_data = is_valid_node(full_file_path)
                template_data = is_valid_template_file(full_file_path)
                if nodejs_data or template_data:
                    data = nodejs_data if nodejs_data else template_data
                    # Add only files we scan
                    relative_path = full_file_path.replace(path, "")
                    mpath = full_file_path.replace(
                        settings.UPLOAD_FOLDER, "", 1)
                    all_files.append({relative_path: mpath})

                    sec, good = code_analysis(
                        data, full_file_path, scan_rules, header_found)
                    good_finding += good
                    security_issues += sec

    # After Every Files are done.
    # Check for missing Security Headers
    for header, val in header_found.items():
        if val == 0:
            finding = {}
            finding["title"] = header
            finding["description"] = scan_rules["desc"][header]
            finding["tag"] = scan_rules["tag"][header]
            missing_header.append(finding)

    sec_issues_by_tag = {}
    good_finding_by_tag = {}
    missing_header_by_tag = {}
    vuln_n_count = {}
    count = {}

    # Vulnerability and Count
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


def code_analysis(data, full_file_path, scan_rules, header_found):
    """ Static Code Analysis of File"""
    security_issues = []
    good_finding = []

    bdata = beautify_js(data, full_file_path)
    org_lines = bdata.splitlines()
    # Sanitized lines are only for scan
    lines, san_data = sanitize_comments(bdata)
    for line_no, line in enumerate(lines):
        # Limit the no of caracters in a line to 2000
        line = line[0:2000]
        # Vulnerability String Match
        for rule_key in scan_rules["vuln_rules"].keys():
            if scan_rules["vuln_rules"][rule_key] in line:
                adds = add_findings(
                    rule_key, scan_rules, line_no, org_lines, full_file_path)
                security_issues.append(adds)
        # Vulnerability Regex Match
        for regex in scan_rules["vuln_regex"].keys():
            if re.search(scan_rules["vuln_regex"][regex], line):
                addr = add_findings(
                    regex, scan_rules, line_no, org_lines, full_file_path)
                security_issues.append(addr)
        # Vulnerability Multi Regex Match
        for mulregex in scan_rules["vuln_mul_regex"].keys():
            sig_source = scan_rules["vuln_mul_regex"][
                mulregex]["sig_source"]
            sig_line = scan_rules["vuln_mul_regex"][
                mulregex]["sig_line"]
            if re.search(sig_source, san_data):
                if re.search(sig_line, line):
                    addm = add_findings(
                        mulregex, scan_rules, line_no, org_lines, full_file_path)
                    security_issues.append(addm)
        # Dynamic Regex
        for dynregex in scan_rules["vuln_dyn_regex"].keys():
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
                    for lno, nline in enumerate(lines):
                        nline = nline[0:2000]
                        if re.search(dyn_sig, nline):
                            addd = add_findings(
                                dynregex, scan_rules, lno, org_lines, full_file_path)
                            security_issues.append(addd)
        # Good Finding String Match
        for good_find in scan_rules["good_to_have_rgx"].keys():
            if re.search(scan_rules["good_to_have_rgx"][good_find], line):
                addg = add_findings(
                    good_find, scan_rules, line_no, org_lines, full_file_path)
                good_finding.append(addg)
        # Missing Security Headers String Match
        for header in scan_rules["missing_sec_header"].keys():
            if re.search(scan_rules["missing_sec_header"][header], line, re.I):
                # Good Header is present
                header_found[header] = 1
    return security_issues, good_finding
