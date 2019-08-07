import core.scanner as njsscan
res_dir = njsscan.scan_dirs(['./static/js'])
res_file = njsscan.scan_file(['./static/js/jquery.min.js'])
print(res_file)
