# -*- coding: utf-8 -*-
import os,re,time
from splinter import Browser 
import csv

def getresult(caseid):
    f_csv = "%s.csv" %session
    ifile  = open(f_csv, "rb")
    reader = csv.reader(ifile)
    rownum = 0
    for row in reader:
        if rownum == 0:
            header = row
        else:
            colnum = 0
            for i, col in enumerate(row):
                if col == str(caseid+1):
                    #print '%-8s: %s' % (header[colnum], col)
                    return str(row[2]).lower() 
                colnum += 1                
        rownum += 1
    ifile.close()

def getresult2(caseid):
    f_csv = "%s.csv" %session
    ifile  = open(f_csv, "rb")
    reader = csv.reader(ifile)
    rownum = 0
    for row in reader:
        if rownum == 0:
            header = row
        else:
            colnum = 0
            for i, col in enumerate(row):
                #print col
                if col == str(caseid):
                    #print '%-8s: %s' % (header[colnum], col)
                    return  str(row[3])
                colnum += 1                
        rownum += 1
    ifile.close()

def getcount():
    f_html = "%s.html" %session
    html = open(f_html, "r").read()
    return len(re.findall('class="TYPE_tc_table"', html))

def wait_till_page_load(browser):
    text = '%s' %session
    while browser.title.find(text) == -1: 
        time.sleep(3)
        print "no found"

def fill_result():
    sleep_time=10000
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
        case_count = getcount()

        for i in range(case_count):
            option = 'results_%s' %i
            print option
            option_jira = 'RUNDATA_atm_prid_%s' %i
            print option_jira
            option_jiralink = 'RUNDATA_atm_prlink_%s' %i
            value = getresult(i)
            print value
            jira = getresult2(i+1)
            print jira
            jira_link = 'http://jira.lsi.com/browse/%s' %jira
            if value is not None:
                browser.select(option, value)
            
            if jira is not None and jira != '':
                browser.fill(option_jira, jira)
                browser.fill(option_jiralink, jira_link)
            
        button = browser.find_by_name('Finish')
        button.click()
        #time.sleep(sleep_time)
    
if __name__ == "__main__":

    list_session = ['002462','002461']
    for session in list_session:
        fill_result()

    