# -*- coding: utf-8 -*-
import urllib2
import re
import threading
import Queue
import time


# 获取网页数据
def getdata(url):
    try:
        data = urllib2.urlopen(url).read().decode("utf-8")
        # 没有异常返回字符串
        return data
    except:
        # 有异常，返回空
        return ""

# 获取网页邮箱,data为网页数据
def getallemail(data):
    try:
        mailregex = re.compile(r"([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4})", re.IGNORECASE)
        emaillist = mailregex.findall(data)
        return emaillist
    except:
        return []

# 获取网页所有的链接
def getallhttp(data):
    try:
        mailregex = re.compile(r"(http://\S*?)[\"|>|)]", re.IGNORECASE)
        mylist = mailregex.findall(data)
        return mylist
    except:
        return []

# 获取网页链接的主机域名
def gethostname(httpstr):
    try:
        hostregex = re.compile(r"(http://\S*?)/",re.IGNORECASE)
        # 正则提取出来的都是放在一个列表里面
        mylist = hostregex.findall(httpstr)
        if len(mylist) == 0:
            return None
        else:
            return mylist[0]
    except:
        return None

# 通过主机域名和页面内容中的href中的子链接拼接得到完整的url
def getabsurl(url,data):
    try:
        # 子链接url
        regex = re.compile("href=\"(.*?)\"",re.IGNORECASE)
        urllist = regex.findall(data)
        # 深拷贝，这样对拷贝文件操作时不会破坏原列表
        newurllist = urllist.copy()

        for data in newurllist:
            # 如果找到的href中的子链接有带http开头的，就移除掉
            if data.find("http://") != -1:
                urllist.remove(data)
            # 如果找到javascript文本页将其移除
            if data.find("javascript") != -1:
                urllist.remove(data)

        # 获取主机域名
        hostname = gethostname(url)
        # 如果主域名部位空
        if hostname != None:
            # 循环将主域名和子链接拼接，构成完整的url
            for i in range(len(urllist)):
                urllist[i] = hostname + urllist[i]

        return urllist
    except:
        return []

# 获取所有的url
def geteveryurl(data):
    alllist = []
    mylist1 = []
    mylist2 = []

    # 获取主域名
    mylist1 = getallhttp(data)
    # 如果域名不为空，通过主机域名获取完整的链接
    if len(mylist1) > 0:
        mylist2 = getabsurl(mylist1[0], data)

    alllist.extend(mylist1)
    alllist.extend(mylist2)
    return alllist

# 循环所有的url，获取邮箱和网页内容
def BFS(url):
    # 创建队列
    queue = Queue.Queue()
    # 将链接放进队列
    queue.put(url)

    # 当队列不为空
    while not queue.empty():
        # 从队列取出url
        url = queue.get()
        # 获取网页数据
        pagedata = getdata(url)
        print "抓取",url
        # 获取网页邮箱
        emaillist = getallemail(pagedata)
        # 如果邮箱不为空，取出邮箱
        if len(emaillist) != 0:
            for email in emaillist:
                print email

        urllist = geteveryurl(pagedata)
        if len(urllist) != 0:
            for myurl in urllist:
                queue.put(myurl)


print gethostname("http://bbs.tianya.cn/m/post-140-393974-1.shtml")

