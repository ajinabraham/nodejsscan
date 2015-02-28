import re,os,platform,webbrowser,subprocess,xml.dom.minidom
from optparse import OptionParser
from xml.dom.minidom import parse

def NodeJSStaticAnalyzer(path):
    rules, rx, seccode,desc=ReadRules()
    regex_flag={}
    sec=''
    final=''
    for init0 in seccode.iterkeys():
        regex_flag[init0]='0'      
    print "Running Static Analyzer Running on - "+ path + "\n"
    for dirName, subDir, files in os.walk(path):
        for jfile in files:
            jfile_path=os.path.join(path,dirName,jfile)
            if jfile.endswith('.js'):
                '''
                try:
                '''
                line_no=0
                data=''

                with open(jfile_path,'r') as f:
                    for line in f:
                        line=line.decode('utf8', 'ignore')
                        line_no+=1
                        for key in rules.iterkeys():

                            if rules[key] in line:
                                data+= '<tr><td>'+ key + '</td><td>' + desc[key] + '</td><td>'+ str(line_no)+ '</td><td>'+ jfile + '</td><td><a href="' + jfile_path + '">'+jfile_path+'</a></td></tr>'
                        for regex in rx.iterkeys():
                            if re.search(rx[regex],line,re.I):
                                data+= '<tr><td>'+regex + '</td><td>'  + desc[regex] + '</td><td>' + str(line_no)+ '</td><td>' + jfile + '</td><td><a href="'  + jfile_path + '">'+jfile_path+'</a></td></tr>'
                        for scode in seccode.iterkeys():
                            if re.search(seccode[scode],line,re.I):
                                regex_flag[scode]='1'
                final+=data
    #After Every Files are done.  
    for rflag in regex_flag.iterkeys():
        if '0' in regex_flag[rflag]:
            sec+= '<tr><td>'+rflag + '</td><td>' + desc[rflag] + '</td></tr>'     
    outdated=RunRetire(path)
    return final, sec, outdated

    '''
                except Exception as e:
                    print "ERROR - " + str(e)
                    pass
                '''
def ReadRules():
    #Load Rules
    rx={}
    rules={}
    sec_code={}
    desc={}
    DOMTree = xml.dom.minidom.parse("rules.xml")
    collection = DOMTree.documentElement
    rules_collection = collection.getElementsByTagName("rule")
    for rule in rules_collection:
        if rule.hasAttribute("name"):
            signature = rule.getElementsByTagName('signature')[0]
            rules[rule.getAttribute("name")] = signature.childNodes[0].data
            description= rule.getElementsByTagName('description')[0]
            desc[rule.getAttribute("name")] = description.childNodes[0].data
    regexs=collection.getElementsByTagName("regex")
    for regex in regexs:
        if regex.hasAttribute("name"):
            signature = regex.getElementsByTagName('signature')[0]
            rx[regex.getAttribute("name")] = signature.childNodes[0].data
            description= regex.getElementsByTagName('description')[0]
            desc[regex.getAttribute("name")] = description.childNodes[0].data
    seccodes=collection.getElementsByTagName("notpresent")
    for scode in seccodes:
        if scode.hasAttribute("name"):
            signature = scode.getElementsByTagName('signature')[0]
            sec_code[scode.getAttribute("name")] = signature.childNodes[0].data
            description= scode.getElementsByTagName('description')[0]
            desc[scode.getAttribute("name")] = description.childNodes[0].data

    return rules, rx, sec_code, desc
def Report(data,sec,out):
    path = os.path.join(os.getcwd() + '/template/template.html')
    with open(path,'r') as f:
        dat=f.read()
    report_path= os.path.join(os.getcwd() + '/Report.html')
    with open(report_path,'w') as f:
        f.write(dat.replace('{{DATA}}',data).replace('{{SEC}}',sec).replace('{{LIB}}',out))
    print "Report generated.\nOpening Report.html"
    if platform.system()=="Darwin":
        os.system("open "+report_path)
    else:
        webbrowser.open_new_tab(report_path)

    
def RunRetire(path):
    args=[]
    retirepath=os.path.join(os.path.curdir, 'node','bin','retire')
    if platform.system()=="Windows":
        args=['node.exe',retirepath, '--nodepath', path]
    else:
        args=['node',retirepath, '--nodepath', path]
    x=''
    err=''
    try:
        x, err = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        x+=err
    except Exception as e:
        print "ERROR - Install node.js > 0.8" 
        pass
    if '<tr>' in x:
        return x
    else:
        return ''
        
        

def main():
    nodeonly=False
    usage = "usage: %prog -d <dir>"
    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--dir", dest="dir")
    (options, args) = parser.parse_args()
    if options.dir is not None:
        print '\nNodeJsScan is a node.js Static Analysis Tool that can detect possible security issues, insecure code and outdated libraries (using retire.js).\n\n'
        dat,sec, out=NodeJSStaticAnalyzer(options.dir)
        Report(dat,sec,out)
    else:
        print "Usage: NodeJsScan.py -d <dir>"



if __name__ == '__main__':
    main()
