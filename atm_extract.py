# -*- coding: utf-8 -*-
import os,re,time
from bs4 import BeautifulSoup
from splinter import Browser 
import csv

def dumpfile(browser):
    f_html = "%s.html" %session
    file_html = open(f_html,'w')
    str_source = browser.html.encode('utf-8')
    file_html.write(str_source)
    file_html.close()

def dumpintofile(browser):
    dumpfile(browser)
    f_html = "%s.html" %session
    if os.path.getsize(f_html) < 10000:
        dumpfile(browser)

def getsource():
    f_html = "%s.html" %session
    str_source = open(f_html,'r').read()
    #str_source = browser.html.encode('utf-8')
    return str_source

def getridofgarbage(lines):
    return lines.replace('\xc2\xa0',' ') #nbsp;

def process_line(str_line):
    str_script_argu = ''

    for lines in str_line.split('\n'):
        pattern1 = re.compile(r'.*\s(\S+py).*')
        match1 = pattern1.match(getridofgarbage(lines))
        if match1:
            script_name=match1.group(1)
            str_script_argu += script_name
            pattern2 = re.compile(r'.*\s{1,2}(-{1,2}\w{1,20}=\d{1,10}|[a-z][A-Z]{1})')
            match2 = pattern2.match(lines)
            if match2:
                script_argument = match2.group(1)
                str_script_argu += ' ' + script_argument

            pattern3 = re.compile(r'.*\s{1,2}(--unsafed).*')
            match3 = pattern3.match(lines)
            if match3:
                script_argument = match3.group(1)
                str_script_argu += ' ' + script_argument
        pattern1 = re.compile(r'.*\s(\S+srt).*')
        match1 = pattern1.match(getridofgarbage(lines))
        if match1:
            script_name=match1.group(1)
            str_script_argu += script_name
    return str_script_argu

def convert_test_case():
    list_script = []
    str_script_argu = ''

    soup = BeautifulSoup(getsource())
    for line in soup.find_all('table',{'class':"TYPE_tc_table"}):
        str_line = str(line.text.encode('utf-8')) 
        str_script_argu = process_line(str_line)
        if str_script_argu != '':
            list_script.append(str_script_argu)
    #print list_script
    return list_script

def getcount():
    f_html = "%s.html" %session
    html = open(f_html, "r").read()
    return len(re.findall('class="TYPE_tc_table"', html))

def script_list():
    dir_script = 'Z:\Test_Tip\Scripts\\'
    script_list = []
    for dirpath, dirnames, files in os.walk(dir_script):
        for filename in files:
            script_list.append(filename) 
    return script_list

def correctscriptname(scriptname):
    source_script_list = script_list()
    for index, files in enumerate(source_script_list):
        if scriptname.lower() == files.lower():
            scriptname = source_script_list[index]
    return scriptname

def checkvalid(target_script):
    source_script_list = script_list()
    for index,files in enumerate(target_script):
        scriptname = files.split(' ')[0]
        if scriptname not in source_script_list:
            correct_name = correctscriptname(scriptname)
            if correct_name is not None:
                if len(target_script[index].split(' ')) == 1:
                    target_script[index] = correct_name
                else:
                    target_script[index] = correct_name + ''.join(target_script[index].split(' ')[1:])

    return target_script

def wait_till_page_load(browser):
    text = '%s' %session
    #print 2
    while browser.title.find(text) == -1: 
        #print 1
        time.sleep(5)
        print "no found"


def write():
    target_script = extract_result()
    file_csv = '%s.csv' %session
    writer = csv.writer(file(file_csv, 'wb'))
    writer.writerow(['Case Number', ' Test case', 'result', 'JIRA'])
    
    case_number = getcount()

    print target_script
    case = [[] for i in range(case_number)]

    for index in range(case_number):
        num = index + 1
        #print index
        case[index]
        #print num
        #print target_script[index]
        case[index].append('%d' %num)
        case[index].append(target_script[index])
        case[index].append('')
        case[index].append('')
    #print case
    for line in case:
        writer.writerow(line)

def getURLsource():
    with Browser() as browser: 

        url = "http://ftcsvn.lsi.com/atm/run/runWholeSession.mpl?suite=FCD&sessNum=%s/Nightly&tid=-1" %session
        browser.visit(url)
        try:
            browser.find_by_name('Yoyo Xu').first.click()
        except:
            browser.fill('name','yoxu')
            browser.fill('pass','Lsi201312')
            browser.find_by_name('submit').first.click()

        wait_till_page_load(browser)
        dumpintofile(browser)

def extract_result():
    getURLsource()
    target_script = convert_test_case()
    return checkvalid(target_script)

    
if __name__ == "__main__":

    list_session = ['002463', '002462', '002461', '002451', '002447', '002446', '002445', '002444', '002443', '002442', '002441', '002440', '002439']
    #list_session = ['002446']
    for session in list_session:
        time.sleep(5)
        write()
    
