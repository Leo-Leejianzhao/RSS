'''
Author: Leo Lee (leejianzhao@gmail.com)
Date: 2021-07-18 16:34:45
LastEditTime: 2022-03-24 08:32:11
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

def get_mattkaydiary():
    log('begin get_mattkaydiary')
    v2ray_add=None
    try:
        rss = feedparser.parse('http://feeds.feedburner.com/mattkaydiary/pZjG')
        current = rss["entries"][0]
        v2rayList = re.findall(r"v2ray\(请开启代理后再拉取\)：(.+?)</div>", current.summary)
        clashList = re.findall(r"clash\(请开启代理后再拉取\)：(.+?)</div>", current.summary)
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        if v2rayList:
            v2ray_add=v2rayList[len(v2rayList)-1].replace('amp;', '').strip()
            v2rayTxt = requests.request(
                "GET", v2ray_add)
            with open(dirs + '/v2ray_mat.txt', 'w') as f:
                f.write(v2rayTxt.text)
            # print(v2rayTxt.text)
        if clashList:
            clashTxt = requests.request(
                "GET", clashList[len(clashList)-1].replace('amp;','').strip(), verify=False)
            day = time.strftime('%Y.%m.%d',time.localtime(time.time()))
            with open(dirs + '/clash_mat.yml', 'w',encoding='utf-8') as f:
                f.write(clashTxt.text.replace('mattkaydiary.com',day))
    except Exception as e:
        log('can not get_mattkaydiary:'+e.__str__())
    return v2ray_add

# def IP2name(ip):
#     try:
#         res=requests.get(f'http://ip-api.com/json/{ip}?fields=country,countryCode,city&lang=zh-CN', timeout=10).json()
#         return f"{ip}@{res['country']}({res['countryCode']})-{res['city']}/"+''.join(random.sample(string.ascii_letters + string.digits, 3))
#     except Exception as e:
#         log('IP2name: '+ip+': '+e.__str__())
#         return ip+''.join(random.sample(string.ascii_letters + string.digits, 8))

def IP2name(ip):
    return ip+''.join(random.sample(string.ascii_letters + string.digits, 8))


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
        pass
        # try:
        #     tmp=urllib.parse.urlparse(proxy_str)
        #     server=tmp.hostname
        #     port=tmp.port
        #     password=tmp.username
        #     # password, addr_port = proxy_str_split[1].split('@')
        #     # password = urllib.parse.unquote(password)
        #     # addr, port = addr_port.rsplit(':', 1)
        #     # if addr[0] == '[':
        #     #     addr = addr[1:-1]
        #     # port = int(port)
        #     proxy={
        #         # "name"      :   ''.join(random.sample(string.ascii_letters + string.digits, 8)), #urllib.parse.unquote(url.fragment),
        #         "name"      :   IP2name(server),
        #         "type"      :   "trojan",
        #         "server"    :   server,
        #         "password"  :   password,
        #         "port"      :   port,
        #         # "sni"       :   server
        #     }
        # except Exception as e:
        #     log('Invalid trojan URL:'+proxy_str)
        #     log(e.__str__())
    elif proxy_str_split[0] == 'vmess':
        try:
            tmp=json.loads(base64.b64decode(proxy_str_split[1]+'=='))
            if tmp["add"]!='127.0.0.1':
                proxy={
                    # "name": ''.join(random.sample(string.ascii_letters + string.digits, 8)),#tmp["ps"],
                    "name"      :   IP2name(tmp.get("add")),
                    "type": "vmess",
                    "server": tmp.get("add"),
                    "port": tmp.get("port"),
                    "uuid": tmp.get("id"),
                    "alterId": tmp.get("aid"),
                    "cipher": "auto",
                    "network": tmp.get("net"),
                    'ucp':True,
                    'ws-path':tmp.get('path'),
                    'ws-headers':{'Host':tmp['host']} if tmp.__contains__('host') else None,
                    "tls": True if tmp.get("tls") == "tls" or tmp.get("net") == "h2"else False,
                }
        except Exception as e:
            log('Invalid vmess URL:'+proxy_str)
            log(e.__str__())
    elif proxy_str_split[0] == 'ss':
        try:
            tmp=urllib.parse.urlparse(proxy_str)
            if tmp.username is not None:
                server=tmp.hostname
                port=tmp.port
                cipher,password=base64.b64decode(tmp.username+'==').decode().split(':')
            else:
                tmp=base64.b64decode(tmp.netloc+'==').decode()
                cipher,other,port=tmp.split(':')
                password,server=other.split('@')
            if cipher and password and server and port:
                proxy={
                    # "name": ''.join(random.sample(string.ascii_letters + string.digits, 8)), #urllib.parse.unquote(url.fragment),
                    "name"      :   IP2name(server),
                    "type": "ss",
                    "server": server,
                    "port": port,
                    "password": password,
                    "alterId": 2,
                    "cipher": cipher,
                }
        except Exception as e:
            log('Invalid vmess URL:'+proxy_str)
            log(e.__str__())
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
    if not url: return []
    log('begin load_subscribe_url: '+url)
    try:
        v2rayTxt = requests.request("GET", url, verify=False)
        sub=base64.b64decode(v2rayTxt.text+'==').decode('utf-8').splitlines()
        log(f'{url} import {len(sub)} servers')
        return sub
    except Exception as e:
        log('load_subscribe_url: '+url+': '+e.__str__())
        return []


def load_subscribe(file):
    with open(file, 'rb') as f:
        raw=base64.b64decode(f.read()).decode('utf-8').splitlines()
    return raw

# def gen_clash_subscribe(proxies):
#     with open(r"./template/clash_proxy_group.yaml", 'r', encoding='UTF-8') as f:
#         proxy_groups = yaml.safe_load(f)
#     # print(proxy_groups)
#     for p in proxy_groups:
#         if not p.__contains__('proxies'):
#             p['proxies']=[n["name"] for n in proxies if n]
#     with open(r"./template/clash_tmp.yaml", 'r',encoding="utf-8") as f:
#         template = yaml.safe_load(f)
#     template["proxies"]=proxies
#     template["proxy-groups"]=proxy_groups
#     with open(r"./subscribe/tmp.yaml",'w', encoding="utf-8") as f:
#         yaml.dump(template,f, sort_keys=False,encoding="utf-8",allow_unicode=True)

def gen_clash_subscribe(proxies):
    with open(r"./subscribe/config.yml", 'r', encoding='UTF-8') as f:
        config = yaml.safe_load(f)
    config['proxies']=proxies
    proxies_name=[proxies[i]['name'] for i in range(len(proxies))]
    config['proxy-groups'][0]['proxies'].extend(proxies_name)
    config['proxy-groups'][1]['proxies']=proxies_name
    with open(r"./subscribe/clash.yml",'w', encoding="utf-8") as f:
        yaml.dump(config,f, sort_keys=False,encoding="utf-8",allow_unicode=True)

def gen_v2ray_subscribe(proxies):
    with open(dirs + '/v2ray.txt','wb') as f:
        f.write(base64.b64encode('\n'.join(proxies).encode(encoding="ascii",errors="ignore")))

def manual_input():
    servers='''vmess://eyJhZGQiOiI2NC4zMi4yNC4yMTMiLCJhaWQiOiI2NCIsImFscG4iOiIiLCJmcCI6IiIsImhvc3QiOiIiLCJpZCI6ImNmZjlkODYwLTczMzAtNGVlMS1iMDcyLTcxNDJkZGYxNTcxZCIsIm5ldCI6InRjcCIsInBhdGgiOiIiLCJwb3J0IjoiNDg2NTkiLCJwcyI6Iue+juWbvSDliqDliKnnpo/lsLzkuprlt57mtJvmnYnnn7ZTaGFya3RlY2jmlbDmja7kuK3lv4MiLCJzY3kiOiJhdXRvIiwic25pIjoiIiwidGxzIjoiIiwidHlwZSI6Im5vbmUiLCJ2IjoiMiJ9
vmess://eyJhZGQiOiI2NC4zMi40LjQyIiwiYWlkIjoiNjQiLCJhbHBuIjoiIiwiZnAiOiIiLCJob3N0IjoiIiwiaWQiOiI4NjUzMDA0Zi1kZTY3LTQ0YzItOWNjZS1lMDgzMDkzM2ZiMDMiLCJuZXQiOiJ0Y3AiLCJwYXRoIjoiIiwicG9ydCI6IjQzMTY2IiwicHMiOiLnvo7lm70g5Yqg5Yip56aP5bC85Lqa5bee5rSb5p2J55+2U2hhcmt0ZWNo5pWw5o2u5Lit5b+DIiwic2N5IjoiYXV0byIsInNuaSI6IiIsInRscyI6IiIsInR5cGUiOiJub25lIiwidiI6IjIifQ==
vmess://eyJhZGQiOiI2NC4zMi40LjYiLCJhaWQiOiI2NCIsImFscG4iOiIiLCJmcCI6IiIsImhvc3QiOiIiLCJpZCI6IjQxODA0OGFmLWEyOTMtNGI5OS05YjBjLTk4Y2EzNTgwZGQyNCIsIm5ldCI6InRjcCIsInBhdGgiOiIiLCJwb3J0IjoiNTAwMDUiLCJwcyI6Iue+juWbvSDliqDliKnnpo/lsLzkuprlt57mtJvmnYnnn7ZTaGFya3RlY2jmlbDmja7kuK3lv4MiLCJzY3kiOiJhdXRvIiwic25pIjoiIiwidGxzIjoiIiwidHlwZSI6Im5vbmUiLCJ2IjoiMiJ9
vmess://eyJhZGQiOiIxMDguMTg2LjExNi4xNzgiLCJhaWQiOiI2NCIsImFscG4iOiIiLCJmcCI6IiIsImhvc3QiOiIiLCJpZCI6IjQxODA0OGFmLWEyOTMtNGI5OS05YjBjLTk4Y2EzNTgwZGQyNCIsIm5ldCI6InRjcCIsInBhdGgiOiIiLCJwb3J0IjoiNTUwMDUiLCJwcyI6Iue+juWbvSBWMkNST1NTLkNPTSIsInNjeSI6ImF1dG8iLCJzbmkiOiIiLCJ0bHMiOiIiLCJ0eXBlIjoibm9uZSIsInYiOiIyIn0=
vmess://eyJhZGQiOiIxNDAuOTkuNDkuNTciLCJhaWQiOiI2NCIsImFscG4iOiIiLCJmcCI6IiIsImhvc3QiOiIiLCJpZCI6IjQxODA0OGFmLWEyOTMtNGI5OS05YjBjLTk4Y2EzNTgwZGQyNCIsIm5ldCI6InRjcCIsInBhdGgiOiIiLCJwb3J0IjoiNTU2MDIiLCJwcyI6Iue+juWbvSBEYXRhYmlsaXR5Iiwic2N5IjoiYXV0byIsInNuaSI6IiIsInRscyI6IiIsInR5cGUiOiJub25lIiwidiI6IjIifQ==
vmess://eyJhZGQiOiIxNDAuOTkuMTQ5LjQzIiwiYWlkIjoiNjQiLCJhbHBuIjoiIiwiZnAiOiIiLCJob3N0IjoiIiwiaWQiOiI0MTgwNDhhZi1hMjkzLTRiOTktOWIwYy05OGNhMzU4MGRkMjQiLCJuZXQiOiJ0Y3AiLCJwYXRoIjoiIiwicG9ydCI6IjUzMDgyIiwicHMiOiLnvo7lm70gRGF0YWJpbGl0eSIsInNjeSI6ImF1dG8iLCJzbmkiOiIiLCJ0bHMiOiIiLCJ0eXBlIjoibm9uZSIsInYiOiIyIn0=
vmess://eyJhZGQiOiIyMy4yMjQuMTUuMTgwIiwiYWlkIjoiNjQiLCJhbHBuIjoiIiwiZnAiOiIiLCJob3N0IjoiIiwiaWQiOiI0MTgwNDhhZi1hMjkzLTRiOTktOWIwYy05OGNhMzU4MGRkMjQiLCJuZXQiOiJ0Y3AiLCJwYXRoIjoiIiwicG9ydCI6IjUwMDAyIiwicHMiOiLnvo7lm73liqDliKnnpo/lsLzkuprlt57mtJvmnYnnn7YgQ29wZXJhdGlvbiBDb2xvY3Rpb27mlbDmja7kuK3lv4MiLCJzY3kiOiJhdXRvIiwic25pIjoiIiwidGxzIjoiIiwidHlwZSI6Im5vbmUiLCJ2IjoiMiJ9
vmess://eyJhZGQiOiI0NS41OC4xODAuMTM0IiwiYWlkIjoiNjQiLCJhbHBuIjoiIiwiZnAiOiIiLCJob3N0IjoiIiwiaWQiOiI0MTgwNDhhZi1hMjkzLTRiOTktOWIwYy05OGNhMzU4MGRkMjQiLCJuZXQiOiJ0Y3AiLCJwYXRoIjoiIiwicG9ydCI6IjQ5ODc3IiwicHMiOiLojbflhbAg5YyX6I235YWw55yB6Zi/5aeG5pav54m55Li5U2hhcmt0ZWNo5pWw5o2u5Lit5b+DIiwic2N5IjoiYXV0byIsInNuaSI6IiIsInRscyI6IiIsInR5cGUiOiJub25lIiwidiI6IjIifQ==
vmess://eyJhZGQiOiIxNTQuODUuMS4zIiwiYWlkIjoiNjQiLCJhbHBuIjoiIiwiZnAiOiIiLCJob3N0IjoiIiwiaWQiOiI0MTgwNDhhZi1hMjkzLTRiOTktOWIwYy05OGNhMzU4MGRkMjQiLCJuZXQiOiJ0Y3AiLCJwYXRoIjoiIiwicG9ydCI6IjQwNDI0IiwicHMiOiLnvo7lm70gQ2xvdWRpbm5vdmF0aW9u5pWw5o2u5Lit5b+DIiwic2N5IjoiYXV0byIsInNuaSI6IiIsInRscyI6IiIsInR5cGUiOiJub25lIiwidiI6IjIifQ==
vmess://eyJhZGQiOiIxNTYuMjQ5LjE4LjEyNyIsImFpZCI6IjY0IiwiYWxwbiI6IiIsImZwIjoiIiwiaG9zdCI6IiIsImlkIjoiMTExMTdkNGMtM2I2YS00ZTc2LThiY2MtMmI0MWIzZTljYTkzIiwibmV0IjoidGNwIiwicGF0aCI6IiIsInBvcnQiOiI0ODEwMCIsInBzIjoi5Y2X6Z2e6LGq55m755yB57qm57+w5YaF5pav5aChIENsb3VkaW5ub3ZhdGlvbuaVsOaNruS4reW/gyIsInNjeSI6ImF1dG8iLCJzbmkiOiIiLCJ0bHMiOiIiLCJ0eXBlIjoibm9uZSIsInYiOiIyIn0=
vmess://eyJhZGQiOiIxNTYuMjQ5LjE4LjM3IiwiYWlkIjoiNjQiLCJhbHBuIjoiIiwiZnAiOiIiLCJob3N0IjoiIiwiaWQiOiI0MTgwNDhhZi1hMjkzLTRiOTktOWIwYy05OGNhMzU4MGRkMjQiLCJuZXQiOiJ0Y3AiLCJwYXRoIjoiIiwicG9ydCI6IjQ4MjIyIiwicHMiOiLljZfpnZ7osarnmbvnnIHnuqbnv7DlhoXmlq/loKEgQ2xvdWRpbm5vdmF0aW9u5pWw5o2u5Lit5b+DIiwic2N5IjoiYXV0byIsInNuaSI6IiIsInRscyI6IiIsInR5cGUiOiJub25lIiwidiI6IjIifQ==
vmess://eyJhZGQiOiIxNDAuOTkuMTI5LjI0NCIsImFpZCI6IjY0IiwiYWxwbiI6IiIsImZwIjoiIiwiaG9zdCI6IiIsImlkIjoiNDE4MDQ4YWYtYTI5My00Yjk5LTliMGMtOThjYTM1ODBkZDI0IiwibmV0IjoidGNwIiwicGF0aCI6IiIsInBvcnQiOiI0ODkwMSIsInBzIjoi576O5Zu9IERhdGFiaWxpdHkiLCJzY3kiOiJhdXRvIiwic25pIjoiIiwidGxzIjoiIiwidHlwZSI6Im5vbmUiLCJ2IjoiMiJ9
vmess://eyJhZGQiOiIxNDAuOTkuNTkuMjMwIiwiYWlkIjoiNjQiLCJhbHBuIjoiIiwiZnAiOiIiLCJob3N0IjoiIiwiaWQiOiI0MTgwNDhhZi1hMjkzLTRiOTktOWIwYy05OGNhMzU4MGRkMjQiLCJuZXQiOiJ0Y3AiLCJwYXRoIjoiIiwicG9ydCI6IjU1NTEyIiwicHMiOiLnvo7lm70gRGF0YWJpbGl0eSIsInNjeSI6ImF1dG8iLCJzbmkiOiIiLCJ0bHMiOiIiLCJ0eXBlIjoibm9uZSIsInYiOiIyIn0=
vmess://eyJhZGQiOiI2NC4zMi40LjM0IiwiYWlkIjoiNjQiLCJhbHBuIjoiIiwiZnAiOiIiLCJob3N0IjoiIiwiaWQiOiI4NjUzMDA0Zi1kZTY3LTQ0YzItOWNjZS1lMDgzMDkzM2ZiMDMiLCJuZXQiOiJ0Y3AiLCJwYXRoIjoiIiwicG9ydCI6IjQzMTY2IiwicHMiOiLnvo7lm70g5Yqg5Yip56aP5bC85Lqa5bee5rSb5p2J55+2U2hhcmt0ZWNo5pWw5o2u5Lit5b+DIiwic2N5IjoiYXV0byIsInNuaSI6IiIsInRscyI6IiIsInR5cGUiOiJub25lIiwidiI6IjIifQ==
vmess://eyJhZGQiOiIxNDAuOTkuNTkuMjI3IiwiYWlkIjoiNjQiLCJhbHBuIjoiIiwiZnAiOiIiLCJob3N0IjoiIiwiaWQiOiI0MTgwNDhhZi1hMjkzLTRiOTktOWIwYy05OGNhMzU4MGRkMjQiLCJuZXQiOiJ0Y3AiLCJwYXRoIjoiIiwicG9ydCI6IjU1NTEyIiwicHMiOiLnvo7lm70gRGF0YWJpbGl0eSIsInNjeSI6ImF1dG8iLCJzbmkiOiIiLCJ0bHMiOiIiLCJ0eXBlIjoibm9uZSIsInYiOiIyIn0=
vmess://eyJhZGQiOiIxNTYuMjQ5LjE4LjE2MyIsImFpZCI6IjY0IiwiYWxwbiI6IiIsImZwIjoiIiwiaG9zdCI6IiIsImlkIjoiNDE4MDQ4YWYtYTI5My00Yjk5LTliMGMtOThjYTM1ODBkZDI0IiwibmV0IjoidGNwIiwicGF0aCI6IiIsInBvcnQiOiI0MjI5MiIsInBzIjoi5Y2X6Z2e6LGq55m755yB57qm57+w5YaF5pav5aChIENsb3VkaW5ub3ZhdGlvbuaVsOaNruS4reW/gyIsInNjeSI6ImF1dG8iLCJzbmkiOiIiLCJ0bHMiOiIiLCJ0eXBlIjoibm9uZSIsInYiOiIyIn0=
vmess://eyJhZGQiOiIxMDQuMzEuMTYuNDYiLCJhaWQiOiIwIiwiYWxwbiI6IiIsImZwIjoiIiwiaG9zdCI6ImNhNS50ZWhtZTEwMC5mdW4iLCJpZCI6IjU4ZmUxNTQyLTUyOTAtNDBhZC04MTVhLTc3NzA3YTgxYWZlNSIsIm5ldCI6IndzIiwicGF0aCI6Ii9JT2ViaExNaGwxQ1RiRkhiTDk1bXlmUlgyIiwicG9ydCI6IjIwODIiLCJwcyI6Iue+juWbvSBWMkNST1NTLkNPTSIsInNjeSI6ImF1dG8iLCJzbmkiOiIiLCJ0bHMiOiIiLCJ0eXBlIjoiIiwidiI6IjIifQ==
vmess://eyJhZGQiOiIxNTYuMjQ1LjguMjM0IiwiYWlkIjoiNjQiLCJhbHBuIjoiIiwiZnAiOiIiLCJob3N0IjoiIiwiaWQiOiI2MTkzMTE2ZC05NmY5LTRkN2EtOWJlNS01YmIwNmE2OWFmMGIiLCJuZXQiOiJ0Y3AiLCJwYXRoIjoiIiwicG9ydCI6IjQ5MTU1IiwicHMiOiLpppnmuK8gVjJDUk9TUy5DT00iLCJzY3kiOiJhdXRvIiwic25pIjoiIiwidGxzIjoiIiwidHlwZSI6Im5vbmUiLCJ2IjoiMiJ9
vmess://eyJhZGQiOiIxMDguMTg2LjExNi4xNzgiLCJhaWQiOiI2NCIsImFscG4iOiIiLCJmcCI6IiIsImhvc3QiOiIiLCJpZCI6IjQxODA0OGFmLWEyOTMtNGI5OS05YjBjLTk4Y2EzNTgwZGQyNCIsIm5ldCI6InRjcCIsInBhdGgiOiIiLCJwb3J0IjoiNTUwMDUiLCJwcyI6Iue+juWbvSBWMkNST1NTLkNPTSIsInNjeSI6ImF1dG8iLCJzbmkiOiIiLCJ0bHMiOiIiLCJ0eXBlIjoibm9uZSIsInYiOiIyIn0=
vmess://eyJhZGQiOiIxMDQuMzEuMTYuNDYiLCJhaWQiOiIwIiwiYWxwbiI6IiIsImZwIjoiIiwiaG9zdCI6ImNhNS50ZWhtZTEwMC5mdW4iLCJpZCI6IjU4ZmUxNTQyLTUyOTAtNDBhZC04MTVhLTc3NzA3YTgxYWZlNSIsIm5ldCI6IndzIiwicGF0aCI6Ii9JT2ViaExNaGwxQ1RiRkhiTDk1bXlmUlgyIiwicG9ydCI6IjIwODIiLCJwcyI6Iue+juWbvSBWMkNST1NTLkNPTSIsInNjeSI6ImF1dG8iLCJzbmkiOiIiLCJ0bHMiOiIiLCJ0eXBlIjoiIiwidiI6IjIifQ==
vmess://eyJhZGQiOiIxMDcuMTY3LjcuMTIiLCJhaWQiOiI2NCIsImFscG4iOiIiLCJmcCI6IiIsImhvc3QiOiIiLCJpZCI6ImJkZWUyMDJjLThmYWUtNDQxZi1hNTg4LTdiYzRkMzg4NzAxOSIsIm5ldCI6InRjcCIsInBhdGgiOiIiLCJwb3J0IjoiNDE2NTQiLCJwcyI6Iue+juWbvSDliqDliKnnpo/lsLzkuprlt57mtJvmnYnnn7bluIJTaGFya1RlY2jmlbDmja7kuK3lv4MiLCJzY3kiOiJhdXRvIiwic25pIjoiIiwidGxzIjoiIiwidHlwZSI6Im5vbmUiLCJ2IjoiMiJ9
vmess://eyJhZGQiOiIxMDQuMjAuMjQwLjIxNCIsImFpZCI6IjAiLCJhbHBuIjoiIiwiZnAiOiIiLCJob3N0IjoiZmNjLnZ0Y3NzLnRvcCIsImlkIjoiNTRkNGE1ZTktNjQ0MS00NDJjLWNhYjctMDU2MjBjYmU0ZjdkIiwibmV0Ijoid3MiLCJwYXRoIjoiL3F3ZXIiLCJwb3J0IjoiODA4MCIsInBzIjoi576O5Zu9IENsb3VkRmxhcmXoioLngrkiLCJzY3kiOiJhdXRvIiwic25pIjoiIiwidGxzIjoiIiwidHlwZSI6IiIsInYiOiIyIn0=
vmess://eyJhZGQiOiIxNDAuOTkuMTQ5LjQ1IiwiYWlkIjoiNjQiLCJhbHBuIjoiIiwiZnAiOiIiLCJob3N0IjoiIiwiaWQiOiI0MTgwNDhhZi1hMjkzLTRiOTktOWIwYy05OGNhMzU4MGRkMjQiLCJuZXQiOiJ0Y3AiLCJwYXRoIjoiIiwicG9ydCI6IjUzMDgyIiwicHMiOiLnvo7lm70gRGF0YWJpbGl0eSIsInNjeSI6ImF1dG8iLCJzbmkiOiIiLCJ0bHMiOiIiLCJ0eXBlIjoibm9uZSIsInYiOiIyIn0=
vmess://eyJhZGQiOiIxODguMTE0Ljk5LjY3IiwiYWlkIjoiMCIsImFscG4iOiIiLCJmcCI6IiIsImhvc3QiOiJmY2MudnRjc3MudG9wIiwiaWQiOiI1NGQ0YTVlOS02NDQxLTQ0MmMtY2FiNy0wNTYyMGNiZTRmN2QiLCJuZXQiOiJ3cyIsInBhdGgiOiIvcXdlciIsInBvcnQiOiI4MDgwIiwicHMiOiLlt7Topb/lnKPkv53nvZcgQ2xvdWRGbGFyZeiKgueCuSIsInNjeSI6ImF1dG8iLCJzbmkiOiIiLCJ0bHMiOiIiLCJ0eXBlIjoiIiwidiI6IjIifQ==
vmess://eyJhZGQiOiIxNzMuMjQ1LjU4LjIzMyIsImFpZCI6IjAiLCJhbHBuIjoiIiwiZnAiOiIiLCJob3N0IjoiZmNjLnZ0Y3NzLnRvcCIsImlkIjoiNTRkNGE1ZTktNjQ0MS00NDJjLWNhYjctMDU2MjBjYmU0ZjdkIiwibmV0Ijoid3MiLCJwYXRoIjoiL3F3ZXIiLCJwb3J0IjoiODA4MCIsInBzIjoi576O5Zu9IENsb3VkRmxhcmXoioLngrkiLCJzY3kiOiJhdXRvIiwic25pIjoiIiwidGxzIjoiIiwidHlwZSI6IiIsInYiOiIyIn0=
vmess://eyJhZGQiOiIxMDQuMjAuMjM3LjI0NyIsImFpZCI6IjAiLCJhbHBuIjoiIiwiZnAiOiIiLCJob3N0IjoiZmNjLnZ0Y3NzLnRvcCIsImlkIjoiNTRkNGE1ZTktNjQ0MS00NDJjLWNhYjctMDU2MjBjYmU0ZjdkIiwibmV0Ijoid3MiLCJwYXRoIjoiL3F3ZXIiLCJwb3J0IjoiODA4MCIsInBzIjoi576O5Zu9IENsb3VkRmxhcmXoioLngrkiLCJzY3kiOiJhdXRvIiwic25pIjoiIiwidGxzIjoiIiwidHlwZSI6IiIsInYiOiIyIn0=
vmess://eyJhZGQiOiIxNjIuMTU5LjguNDAiLCJhaWQiOiIwIiwiYWxwbiI6IiIsImZwIjoiIiwiaG9zdCI6ImZjYy52dGNzcy50b3AiLCJpZCI6IjAwNjAyM2Y2LTZkMTctNGVjNi1hZjI0LWJjYzVmN2M0NGUzNSIsIm5ldCI6IndzIiwicGF0aCI6Ii9xd2VyIiwicG9ydCI6Ijg4ODAiLCJwcyI6Iue+juWbvSBDbG91ZEZsYXJl6IqC54K5Iiwic2N5IjoiYXV0byIsInNuaSI6IiIsInRscyI6IiIsInR5cGUiOiIiLCJ2IjoiMiJ9
vmess://eyJhZGQiOiIxODguMTE0Ljk2LjI1MiIsImFpZCI6IjAiLCJhbHBuIjoiIiwiZnAiOiIiLCJob3N0IjoiZmNjLnZ0Y3NzLnRvcCIsImlkIjoiMDA2MDIzZjYtNmQxNy00ZWM2LWFmMjQtYmNjNWY3YzQ0ZTM1IiwibmV0Ijoid3MiLCJwYXRoIjoiL3F3ZXIiLCJwb3J0IjoiODg4MCIsInBzIjoi5be06KW/5Zyj5L+d572XIENsb3VkRmxhcmXoioLngrkiLCJzY3kiOiJhdXRvIiwic25pIjoiIiwidGxzIjoiIiwidHlwZSI6IiIsInYiOiIyIn0=
vmess://eyJhZGQiOiIxMDQuMTYuMjExLjE3NiIsImFpZCI6IjAiLCJhbHBuIjoiIiwiZnAiOiIiLCJob3N0IjoiZmNjLnZ0Y3NzLnRvcCIsImlkIjoiNTRkNGE1ZTktNjQ0MS00NDJjLWNhYjctMDU2MjBjYmU0ZjdkIiwibmV0Ijoid3MiLCJwYXRoIjoiL3F3ZXIiLCJwb3J0IjoiODA4MCIsInBzIjoi576O5Zu9IENsb3VkRmxhcmXoioLngrkiLCJzY3kiOiJhdXRvIiwic25pIjoiIiwidGxzIjoiIiwidHlwZSI6IiIsInYiOiIyIn0=
vmess://eyJhZGQiOiIxMDQuMjUuMTY3LjY5IiwiYWlkIjoiMCIsImFscG4iOiIiLCJmcCI6IiIsImhvc3QiOiJmY2MudnRjc3MudG9wIiwiaWQiOiI1NGQ0YTVlOS02NDQxLTQ0MmMtY2FiNy0wNTYyMGNiZTRmN2QiLCJuZXQiOiJ3cyIsInBhdGgiOiIvcXdlciIsInBvcnQiOiI4MDgwIiwicHMiOiLnvo7lm70gQ2xvdWRGbGFyZeiKgueCuSIsInNjeSI6ImF1dG8iLCJzbmkiOiIiLCJ0bHMiOiIiLCJ0eXBlIjoiIiwidiI6IjIifQ==
vmess://eyJhZGQiOiIyMDMuMjMuMTA0LjE5MCIsImFpZCI6IjAiLCJhbHBuIjoiIiwiZnAiOiIiLCJob3N0IjoiRHVzc2VsZG9yZi5rb3RpY2suc2l0ZSIsImlkIjoiNDk1RkFGOUUtOTc3NS00REM1LTkxRjAtQzQzNDFCNzg5QjRGIiwibmV0Ijoid3MiLCJwYXRoIjoiL3NwZWVkdGVzdCIsInBvcnQiOiI0NDMiLCJwcyI6Iua+s+Wkp+WIqeS6miDmgonlsLwiLCJzY3kiOiJhdXRvIiwic25pIjoiRHVzc2VsZG9yZi5rb3RpY2suc2l0ZSIsInRscyI6InRscyIsInR5cGUiOiIiLCJ2IjoiMiJ9
vmess://eyJhZGQiOiIxODguMTE0Ljk4LjE3MSIsImFpZCI6IjAiLCJhbHBuIjoiIiwiZnAiOiIiLCJob3N0IjoiZmNjLnZ0Y3NzLnRvcCIsImlkIjoiMDA2MDIzZjYtNmQxNy00ZWM2LWFmMjQtYmNjNWY3YzQ0ZTM1IiwibmV0Ijoid3MiLCJwYXRoIjoiL3F3ZXIiLCJwb3J0IjoiODg4MCIsInBzIjoi5be06KW/5Zyj5L+d572XIENsb3VkRmxhcmXoioLngrkiLCJzY3kiOiJhdXRvIiwic25pIjoiIiwidGxzIjoiIiwidHlwZSI6IiIsInYiOiIyIn0=
vmess://eyJhZGQiOiIyMDMuMjMuMTA0LjE5MCIsImFpZCI6IjAiLCJhbHBuIjoiIiwiZnAiOiIiLCJob3N0IjoiRHVzc2VsZG9yZi5rb3RpY2suc2l0ZSIsImlkIjoiNDk1RkFGOUUtOTc3NS00REM1LTkxRjAtQzQzNDFCNzg5QjRGIiwibmV0Ijoid3MiLCJwYXRoIjoiL3NwZWVkdGVzdCIsInBvcnQiOiI0NDMiLCJwcyI6Iua+s+Wkp+WIqeS6miDmgonlsLwiLCJzY3kiOiJhdXRvIiwic25pIjoiRHVzc2VsZG9yZi5rb3RpY2suc2l0ZSIsInRscyI6InRscyIsInR5cGUiOiIiLCJ2IjoiMiJ9
vmess://eyJhZGQiOiIxNTYuMjQ5LjE4LjEyNyIsImFpZCI6IjY0IiwiYWxwbiI6IiIsImZwIjoiIiwiaG9zdCI6IiIsImlkIjoiMTExMTdkNGMtM2I2YS00ZTc2LThiY2MtMmI0MWIzZTljYTkzIiwibmV0IjoidGNwIiwicGF0aCI6IiIsInBvcnQiOiI0ODEwMCIsInBzIjoi5Y2X6Z2e6LGq55m755yB57qm57+w5YaF5pav5aChIENsb3VkaW5ub3ZhdGlvbuaVsOaNruS4reW/gyIsInNjeSI6ImF1dG8iLCJzbmkiOiIiLCJ0bHMiOiIiLCJ0eXBlIjoibm9uZSIsInYiOiIyIn0=
vmess://eyJhZGQiOiIxNjIuMTU5LjM0LjQiLCJhaWQiOiIwIiwiYWxwbiI6IiIsImZwIjoiIiwiaG9zdCI6ImZjYy52dGNzcy50b3AiLCJpZCI6IjAwNjAyM2Y2LTZkMTctNGVjNi1hZjI0LWJjYzVmN2M0NGUzNSIsIm5ldCI6IndzIiwicGF0aCI6Ii9xd2VyIiwicG9ydCI6Ijg4ODAiLCJwcyI6Iue+juWbvSBDbG91ZEZsYXJl6IqC54K5Iiwic2N5IjoiYXV0byIsInNuaSI6IiIsInRscyI6IiIsInR5cGUiOiIiLCJ2IjoiMiJ9
vmess://eyJhZGQiOiIxMDguMTg2LjExNi4xNzciLCJhaWQiOiI2NCIsImFscG4iOiIiLCJmcCI6IiIsImhvc3QiOiIiLCJpZCI6IjQxODA0OGFmLWEyOTMtNGI5OS05YjBjLTk4Y2EzNTgwZGQyNCIsIm5ldCI6InRjcCIsInBhdGgiOiIiLCJwb3J0IjoiNTUwMDUiLCJwcyI6Iue+juWbvSBWMkNST1NTLkNPTSIsInNjeSI6ImF1dG8iLCJzbmkiOiIiLCJ0bHMiOiIiLCJ0eXBlIjoibm9uZSIsInYiOiIyIn0=
vmess://eyJhZGQiOiIxMDQuMTkuMTQ4LjIxNCIsImFpZCI6IjAiLCJhbHBuIjoiIiwiZnAiOiIiLCJob3N0IjoiZmNjLnZ0Y3NzLnRvcCIsImlkIjoiNTRkNGE1ZTktNjQ0MS00NDJjLWNhYjctMDU2MjBjYmU0ZjdkIiwibmV0Ijoid3MiLCJwYXRoIjoiL3F3ZXIiLCJwb3J0IjoiODA4MCIsInBzIjoi576O5Zu9IENsb3VkRmxhcmXoioLngrkiLCJzY3kiOiJhdXRvIiwic25pIjoiIiwidGxzIjoiIiwidHlwZSI6IiIsInYiOiIyIn0=
vmess://eyJhZGQiOiIxMDQuMTcuMjAuNTUiLCJhaWQiOiIwIiwiYWxwbiI6IiIsImZwIjoiIiwiaG9zdCI6IkR1c3NlbGRvcmYua290aWNrLnNpdGUiLCJpZCI6IjQ5NUZBRjlFLTk3NzUtNERDNS05MUYwLUM0MzQxQjc4OUI0RiIsIm5ldCI6IndzIiwicGF0aCI6Ii9zcGVlZHRlc3QiLCJwb3J0IjoiNDQzIiwicHMiOiLnvo7lm70gQ2xvdWRGbGFyZeiKgueCuSIsInNjeSI6ImF1dG8iLCJzbmkiOiJEdXNzZWxkb3JmLmtvdGljay5zaXRlIiwidGxzIjoidGxzIiwidHlwZSI6IiIsInYiOiIyIn0=
vmess://eyJhZGQiOiIxMDQuMTcuMTA2LjcyIiwiYWlkIjoiMCIsImFscG4iOiIiLCJmcCI6IiIsImhvc3QiOiJmY2MudnRjc3MudG9wIiwiaWQiOiIwMDYwMjNmNi02ZDE3LTRlYzYtYWYyNC1iY2M1ZjdjNDRlMzUiLCJuZXQiOiJ3cyIsInBhdGgiOiIvcXdlciIsInBvcnQiOiI4ODgwIiwicHMiOiLnvo7lm70gQ2xvdWRGbGFyZeiKgueCuSIsInNjeSI6ImF1dG8iLCJzbmkiOiIiLCJ0bHMiOiIiLCJ0eXBlIjoiIiwidiI6IjIifQ==
vmess://eyJhZGQiOiIxODguMTE0Ljk2LjczIiwiYWlkIjoiMCIsImFscG4iOiIiLCJmcCI6IiIsImhvc3QiOiJmY2MudnRjc3MudG9wIiwiaWQiOiIwMDYwMjNmNi02ZDE3LTRlYzYtYWYyNC1iY2M1ZjdjNDRlMzUiLCJuZXQiOiJ3cyIsInBhdGgiOiIvcXdlciIsInBvcnQiOiI4ODgwIiwicHMiOiLlt7Topb/lnKPkv53nvZcgQ2xvdWRGbGFyZeiKgueCuSIsInNjeSI6ImF1dG8iLCJzbmkiOiIiLCJ0bHMiOiIiLCJ0eXBlIjoiIiwidiI6IjIifQ==
vmess://eyJhZGQiOiIxMDguMTg2LjExNi4xODMiLCJhaWQiOiI2NCIsImFscG4iOiIiLCJmcCI6IiIsImhvc3QiOiIiLCJpZCI6IjQxODA0OGFmLWEyOTMtNGI5OS05YjBjLTk4Y2EzNTgwZGQyNCIsIm5ldCI6InRjcCIsInBhdGgiOiIiLCJwb3J0IjoiNTUwMDUiLCJwcyI6Iue+juWbvSBWMkNST1NTLkNPTSIsInNjeSI6ImF1dG8iLCJzbmkiOiIiLCJ0bHMiOiIiLCJ0eXBlIjoibm9uZSIsInYiOiIyIn0=
vmess://eyJhZGQiOiIxMDQuMTcuMjAuNTUiLCJhaWQiOiIwIiwiYWxwbiI6IiIsImZwIjoiIiwiaG9zdCI6IkR1c3NlbGRvcmYua290aWNrLnNpdGUiLCJpZCI6IjQ5NUZBRjlFLTk3NzUtNERDNS05MUYwLUM0MzQxQjc4OUI0RiIsIm5ldCI6IndzIiwicGF0aCI6Ii9zcGVlZHRlc3QiLCJwb3J0IjoiNDQzIiwicHMiOiLnvo7lm70gQ2xvdWRGbGFyZeiKgueCuSIsInNjeSI6ImF1dG8iLCJzbmkiOiJEdXNzZWxkb3JmLmtvdGljay5zaXRlIiwidGxzIjoidGxzIiwidHlwZSI6IiIsInYiOiIyIn0=
vmess://eyJhZGQiOiIxNTYuMjQ1LjguODQiLCJhaWQiOiI2NCIsImFscG4iOiIiLCJmcCI6IiIsImhvc3QiOiIiLCJpZCI6ImQ3NzM1MDU4LTFkYWMtNDYxOC05OWZmLTBhYTA0NDFlYzJkNyIsIm5ldCI6InRjcCIsInBhdGgiOiIiLCJwb3J0IjoiNDgxMjMiLCJwcyI6Iummmea4ryBWMkNST1NTLkNPTSIsInNjeSI6ImF1dG8iLCJzbmkiOiIiLCJ0bHMiOiIiLCJ0eXBlIjoibm9uZSIsInYiOiIyIn0=
vmess://eyJhZGQiOiIxNjIuMTU5LjUwLjU1IiwiYWlkIjoiMCIsImFscG4iOiIiLCJmcCI6IiIsImhvc3QiOiJ1eHgudnRjc3MudG9wIiwiaWQiOiJkN2NhMjM2My04MWMyLTQzYTAtZjE0MS0zNTI4MTVkYTNhYzMiLCJuZXQiOiJ3cyIsInBhdGgiOiIvcXdlciIsInBvcnQiOiI4ODgwIiwicHMiOiLnvo7lm70gQ2xvdWRGbGFyZeiKgueCuSIsInNjeSI6ImF1dG8iLCJzbmkiOiIiLCJ0bHMiOiIiLCJ0eXBlIjoiIiwidiI6IjIifQ=='''
    return servers.splitlines()

# 主函数入口
if __name__ == '__main__':
    log("RSS begin...")
    proxies=[]
    # getSubscribeUrl()
    # proxies.extend(load_subscribe(dirs + '/v2ray.txt'))
    # proxies.extend(load_subscribe_url(get_mattkaydiary()))
    # gen_clash_subscribe(list(filter(None,map(protocol_decode,proxies))))
    # proxies.extend(load_subscribe_url('https://jiang.netlify.app'))
    # proxies.extend(load_subscribe_url('https://sspool.herokuapp.com/ss/sub'))
    # proxies.extend(load_subscribe_url('https://sspool.herokuapp.com/sip002/sub'))
    # proxies.extend(load_subscribe_url('https://sspool.herokuapp.com/ssr/sub'))
    # proxies.extend(load_subscribe_url('https://sspool.herokuapp.com/vmess/sub'))
    # proxies.extend(load_subscribe_url('https://sspool.herokuapp.com/trojan/sub'))
    # proxies.extend(load_subscribe_url('https://fforever.github.io/v2rayfree'))
    # proxies.extend(load_subscribe_url('https://muma16fx.netlify.app'))
    # proxies.extend(load_subscribe_url('https://cdn.jsdelivr.net/gh/fggfffgbg/https-aishangyou.tube-@master/README.md'))
    # proxies.extend(load_subscribe_url('https://freev2ray.netlify.app/'))
    # proxies.extend(load_subscribe_url('https://raw.githubusercontent.com/eycorsican/rule-sets/master/kitsunebi_sub'))


    # proxies.extend(load_subscribe_url('https://iwxf.netlify.app'))
    # proxies.extend(load_subscribe_url('https://shadowshare.v2cross.com/publicserver/servers/temp/ud4HOnWAsQxBmSIl'))   
    # proxies.extend(load_subscribe_url('https://youlianboshi.netlify.com'))
    # proxies.extend(load_subscribe_url('https://raw.githubusercontent.com/freefq/free/master/v2'))


    proxies.extend(load_subscribe_url('https://sub.xeton.dev/sub?target=v2ray&url=https://9527521.xyz/config/r619xXVEup802SRh&insert=false'))
    # proxies.extend(load_subscribe_url('https://xn--wbs186a7vao45a8qd.v50.one/api/v1/client/subscribe?token=9249ef731acd8c150e656f6e4b77700f'))
    proxies.extend(load_subscribe_url('https://raw.fastgit.org/Pawdroid/Free-servers/main/sub'))
    # proxies.extend(load_subscribe_url('https://web.anqi.ml/api/v1/client/subscribe?token=21e483aa1e50e796f543b9d63b4a27d1'))
    
    proxies.extend(load_subscribe_url('https://raw.githubusercontent.com/ssrsub/ssr/master/V2Ray'))
    # proxies.extend(load_subscribe_url('https://sub.marsix.cc/api/v1/client/subscribe?token=f6f817ddb0c62fdbaff1c90c9a074c45'))
    # proxies.extend(load_subscribe_url('https://getinfo.bigwatermelon.org/api/v1/client/subscribe?token=8fe4290ba47b6fe0e207ead380a2396a'))

    proxies.extend(load_subscribe_url('https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt'))
    proxies.extend(load_subscribe_url('https://bulinkbulink.com/freefq/free/master/v2'))
    proxies.extend(load_subscribe_url('https://9527521.xyz/pubconfig/tTU5oB98cLGazROS'))
    
    now=datetime.date.today()
    proxies.extend(load_subscribe_url(f"https://v2rayshare.com/wp-content/uploads/{now.year:04}/{now.month:02}/{now.year:04}{now.month:02}{now.day:02}.txt"))
    proxies.extend(load_subscribe_url(f"https://clashgithub.com/wp-content/uploads/rss/{now.year:04}{now.month:02}{now.day:02}.txt"))
    now+=datetime.timedelta(days=-1)
    proxies.extend(load_subscribe_url(f"https://v2rayshare.com/wp-content/uploads/{now.year:04}/{now.month:02}/{now.year:04}{now.month:02}{now.day:02}.txt"))
    proxies.extend(load_subscribe_url(f"https://clashgithub.com/wp-content/uploads/rss/{now.year:04}{now.month:02}{now.day:02}.txt"))
    
    # localtime = time.localtime(time.time())
    # proxies.extend(load_subscribe_url(f"https://v2rayshare.com/wp-content/uploads/{localtime.tm_year:04}/{localtime.tm_mon:02}/{localtime.tm_year:04}{localtime.tm_mon:02}{localtime.tm_mday:02}.txt"))
    # proxies.extend(manual_input())

    proxies=list(set(proxies))
    gen_v2ray_subscribe(proxies)
    gen_clash_subscribe(list(filter(None,map(protocol_decode,proxies))))
    
