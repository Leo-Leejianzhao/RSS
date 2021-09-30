'''
Author: Leo Lee (leejianzhao@gmail.com)
Date: 2021-07-18 16:34:45
LastEditTime: 2021-10-01 01:31:22
FilePath: \RSS\main.py
Description:
'''

import base64
import requests
import json
import time
import re
import base64
# import logging
# import traceback
import os
import random
import datetime
import feedparser
import urllib
import yaml
# import utils
# import wxpusher
# import pytz
import string

# from lxml.html import fromstring
import urllib.parse
import urllib3
urllib3.disable_warnings()

dirs = './subscribe'

def log(msg):
    time = datetime.datetime.now()
    print('['+time.strftime('%Y.%m.%d-%H:%M:%S')+']:'+msg)


# def getFeeds():
#     rss = feedparser.parse('http://feeds.feedburner.com/mattkaydiary/pZjG')
#     current = rss["entries"][0]
#     result = re.findall(r"vmess://(.+?)</div>", rss["entries"][0]["summary"])
#     i = 0
#     dy = ''
#     for point in result:
#         i = i + 1
#         dy += 'vmess://'+point+'\n'
#         logging.info('【'+('%02d' % i) + '】 vmess://' + point)
#     return base64.b64encode(dy.encode('utf-8'))

# 获取文章地址


def getSubscribeUrl():
    try:
        rss = feedparser.parse('http://feeds.feedburner.com/mattkaydiary/pZjG')
        current = rss["entries"][0]
        v2rayList = re.findall(
            r"v2ray\(请开启代理后再拉取\)：(.+?)</div>", current.summary)
        clashList = re.findall(
            r"clash\(请开启代理后再拉取\)：(.+?)</div>", current.summary)
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        if v2rayList:
            v2rayTxt = requests.request(
                "GET", v2rayList[len(v2rayList)-1].replace('amp;',''), verify=False)
            with open(dirs + '/v2ray.txt', 'w') as f:
                f.write(v2rayTxt.text)
            # print(v2rayTxt.text)
        if clashList:
            clashTxt = requests.request(
                "GET", clashList[len(clashList)-1].replace('amp;',''), verify=False)
            day = time.strftime('%Y.%m.%d',time.localtime(time.time()))
            with open(dirs + '/clash.yml', 'w',encoding='utf-8') as f:
                f.write(clashTxt.text.replace('mattkaydiary.com',day))
            # print(clashTxt.text)
    except Exception as e:
        log('RSS load error: '+e.__str__())



# https://github.com/p4gefau1t/trojan-go/issues/132
# trojan-go://
#     $(trojan-password)
#     @
#     trojan-host
#     :
#     port
# ?
#     sni=$(update.microsoft.com)&
#     type=$(original|ws|h2|h2+ws)&
#         host=$(update-01.microsoft.com)&
#         path=$(/update/whatever)&
#     encryption=$(ss;aes-256-gcm:ss-password)&
#     plugin=$(...)
# #$(descriptive-text)
# 特别说明：$() 代表此处需要 encodeURIComponent。
# example:
#   trojan://f@uck.me/?sni=microsoft.com&type=ws&path=%2Fgo&encryption=ss%3Baes-256-gcm%3Afuckgfw


def protocol_decode(proxy_str):
    proxy={}
    # url = urllib.parse.urlparse(proxy_str)
    proxy_str_split=proxy_str.split('://')
    if proxy_str_split[0] == 'trojan':
        try:
            tmp=urllib.parse.urlparse(proxy_str)
            server=tmp.hostname
            port=tmp.port
            password=tmp.username
            # password, addr_port = proxy_str_split[1].split('@')
            # password = urllib.parse.unquote(password)
            # addr, port = addr_port.rsplit(':', 1)
            # if addr[0] == '[':
            #     addr = addr[1:-1]
            # port = int(port)
            proxy={
                "name"      :   ''.join(random.sample(string.ascii_letters + string.digits, 8)), #urllib.parse.unquote(url.fragment),
                "type"      :   "trojan",
                "server"    :   server,
                "password"  :   password,
                "port"      :   port,
                # "sni"       :   server
            }
        except:
            log('Invalid trojan URL:'+proxy_str)
    elif proxy_str_split[0] == 'vmess':
        try:
            tmp=json.loads(base64.b64decode(proxy_str_split[1]+'=='))
            proxy={
                "name": ''.join(random.sample(string.ascii_letters + string.digits, 8)),#tmp["ps"],
                "type": "vmess",
                "server": tmp["add"],
                "port": tmp["port"],
                "uuid": tmp["id"],
                "alterId": tmp["aid"],
                "cipher": "auto" if tmp["type"] == "none" else None,
                "network": tmp["net"],
                'ucp':True,
                'network':tmp['net'],
                'ws-path':tmp['path'] if tmp.__contains__('path') else None,
                'ws-headers':{'Host':tmp['host']} if tmp.__contains__('host') else None,
                "tls": True if tmp["tls"] == "tls" else None,
            }
        except:
            log('Invalid vmess URL:'+proxy_str)
    elif proxy_str_split[0] == 'ss':
        tmp=urllib.parse.urlparse(proxy_str)
        if tmp.username is not None:
            server=tmp.hostname
            port=tmp.port
            cipher,password=base64.b64decode(tmp.username+'==').decode().split(':')
        else:
            tmp=base64.b64decode(tmp.netloc+'==').decode()
            cipher,other,port=tmp.split(':')
            password,server=other.split('@')
        proxy={
            "name": ''.join(random.sample(string.ascii_letters + string.digits, 8)), #urllib.parse.unquote(url.fragment),
            "type": "ss",
            "server": server,
            "port": port,
            "password": password,
            "alterId": 2,
            "cipher": cipher,
        }
    elif proxy_str_split[0] == 'ssr':
        #todo
        #   - name: "ssr"
        #     type: ssr
        #     server: server
        #     port: 443
        #     cipher: chacha20-ietf
        #     password: "password"
        #     obfs: tls1.2_ticket_auth
        #     protocol: auth_sha1_v4
        proxy={}
    return proxy

def load_subscribe_url(url):
    v2rayTxt = requests.request("GET", url, verify=False)
    raw=base64.b64decode(v2rayTxt.text).decode('utf-8').splitlines()
    return list(map(protocol_decode,raw))

def load_subscribe(file):
    with open(file, 'rb') as f:
        raw=base64.b64decode(f.read()).decode('utf-8').splitlines()
    # print(raw)
    # proxies=map(protocol_decode,raw)
    return list(map(protocol_decode,raw))

def gen_clash_subscribe(proxies):
    with open(r"./template/clash_proxy_group.yaml", 'r', encoding='UTF-8') as f:
        proxy_groups = yaml.safe_load(f)
    # print(proxy_groups)
    for p in proxy_groups:
        if not p.__contains__('proxies'):
            p['proxies']=[n["name"] for n in proxies if n]
    with open(r"./template/clash_tmp.yaml", 'r',encoding="utf-8") as f:
        template = yaml.safe_load(f)
    template["proxies"]=proxies
    template["proxy-groups"]=proxy_groups
    with open(r"./subscribe/tmp.yaml",'w', encoding="utf-8") as f:
        yaml.dump(template,f, sort_keys=False)


# 主函数入口
if __name__ == '__main__':
    log("RSS begin...")
    getSubscribeUrl()
    proxies=[]
    proxies.extend(load_subscribe(dirs + '/v2ray.txt'))
    proxies.extend(load_subscribe_url('https://jiang.netlify.app/'))
    gen_clash_subscribe(proxies)