#!/usr/bin/python2
# -*- coding: utf-8 -*-

import socket
import sys

success=open('success.txt','a')

def check(ip, port, timeout):
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        s.send("INFO\r\n")
        result = s.recv(1024)
        if "redis_version" in result:
            return u"[+] IP:{0}存在未授权访问".format(ip)
        elif "Authentication" in result:
            with open('pass.txt','r') as  p:
                passwds = p.readlines()
                for passwd in passwds:
                    passwd = passwd.strip("\n")
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((ip, int(port)))
                    s.send("AUTH %s\r\n" %(passwd))
                    # print u"[HACKING] hacking to passwd --> "+passwd
                    result = s.recv(1024)
                    if 'OK' in result:
                        success.write(u"[+] IP:{0} 存在弱口令，密码：{1}\n".format(ip,passwd))
                        return u"[+] IP:{0} 存在弱口令，密码：{1}".format(ip,passwd)
                    else:pass
        else:pass
        s.close()
    except Exception, e:
        return u"[+] IP:{0}已过滤".format(ip)
        pass

if __name__ == '__main__':
    port="6379"
    with open('ip.txt','r') as  f:
        ips = f.readlines()
        for i in ips:
            ip = i.strip("\n")
            result = check(ip,port,timeout=10)
            print(result)