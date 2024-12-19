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
                    "tls": True if tmp.get("tls") == "tls" or tmp.get("net") == "h2" or tmp.get("net") == "grpc"else False,
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
            if cipher and ("chacha20-poly1305" not in cipher) and password and server and port:
                proxy={
                    # "name": ''.join(random.sample(string.ascii_letters + string.digits, 8)), #urllib.parse.unquote(url.fragment),
                    "name"      :   IP2name(server),
                    "type": "ss",
                    "server": server,
                    "port": port,
                    "password": password,
                    "alterId": 2,
                    "cipher": cipher if cipher!="ss" else "aes-128-gcm",
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

def load_subscribe_url_txt(url):
    if not url: return []
    log('begin load_subscribe_url: '+url)
    try:
        v2rayTxt = requests.request("GET", url, verify=False)
        sub=v2rayTxt.text.splitlines()
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
    servers=''''''
    return servers.splitlines()
    
def getClashSubscribeUrl(url):
    if not url: return []
    res=[]
    log('begin getClashSubscribeUrl: '+url)
    try:
        # txt = requests.request("GET", url, verify=False)
        # ,proxies={'https':'http://127.0.0.1:7890'}
        txt = requests.get(url, verify=False)
        # txt = requests.request("GET", url, verify=False)
        raw=yaml.safe_load(txt.text)
    except Exception as e:
        log('getClashSubscribeUrl: '+url+': '+e.__str__())
        return []
    for proxy in raw["proxies"]:
        if proxy["type"]=="ss":
            # print(proxy)
            res.append(f"ss://{base64.b64encode((proxy['cipher']+':'+proxy['password']).encode('utf-8')).decode('utf-8')}@{proxy['server']}:{proxy['port']}#{proxy['name']}")
        elif proxy["type"]=="vmess":
            # print(proxy)
            tmp= {
                "v": "2",
                "ps": proxy['name'],
                "add": proxy['server'],
                "port": str(proxy['port']),
                "id": proxy['uuid'],
                "aid": "0",
                "scy": "auto",
                "net": proxy.get('network',''),
                "type": "none",
                "host": "v16.583181.xyz",
                "path": "",
                "tls": "tls" if proxy['tls'] else "",
                "sni": "",
                "alpn": ""
                }
            res.append(f"vmess://{base64.b64encode(bytes(json.dumps(tmp),'utf-8')).decode('utf-8')}")
    log(f'{url} import {len(res)} servers')
    return res

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


    # proxies.extend(load_subscribe_url('https://sub.xeton.dev/sub?target=v2ray&url=https://9527521.xyz/config/r619xXVEup802SRh&insert=false'))
    # proxies.extend(load_subscribe_url('https://xn--wbs186a7vao45a8qd.v50.one/api/v1/client/subscribe?token=9249ef731acd8c150e656f6e4b77700f'))
    # proxies.extend(load_subscribe_url('https://raw.fastgit.org/Pawdroid/Free-servers/main/sub'))
    # proxies.extend(load_subscribe_url('https://web.anqi.ml/api/v1/client/subscribe?token=21e483aa1e50e796f543b9d63b4a27d1'))
    
    # proxies.extend(load_subscribe_url('https://raw.githubusercontent.com/ssrsub/ssr/master/V2Ray'))
    # proxies.extend(load_subscribe_url('https://sub.marsix.cc/api/v1/client/subscribe?token=f6f817ddb0c62fdbaff1c90c9a074c45'))
    # proxies.extend(load_subscribe_url('https://getinfo.bigwatermelon.org/api/v1/client/subscribe?token=8fe4290ba47b6fe0e207ead380a2396a'))

    proxies.extend(load_subscribe_url_txt('https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt'))
    # proxies.extend(load_subscribe_url('https://bulinkbulink.com/freefq/free/master/v2'))
    # proxies.extend(load_subscribe_url('https://sub.xeton.dev/sub?target=v2ray&url=https://9527521.xyz/config/GkUDhPycfnu0TXSC&insert=false'))
    
    now=datetime.date.today()
    proxies.extend(load_subscribe_url(f"https://v2rayshare.com/wp-content/uploads/{now.year:04}/{now.month:02}/{now.year:04}{now.month:02}{now.day:02}.txt"))
    proxies.extend(load_subscribe_url(f"https://clashgithub.com/wp-content/uploads/rss/{now.year:04}{now.month:02}{now.day:02}.txt"))
    now+=datetime.timedelta(days=-1)
    proxies.extend(load_subscribe_url(f"https://v2rayshare.com/wp-content/uploads/{now.year:04}/{now.month:02}/{now.year:04}{now.month:02}{now.day:02}.txt"))
    proxies.extend(load_subscribe_url(f"https://clashgithub.com/wp-content/uploads/rss/{now.year:04}{now.month:02}{now.day:02}.txt"))
    # proxies.extend(getClashSubscribeUrl("https://raw.githubusercontent.com/freenodes/freenodes/main/clash.yaml"))
    # localtime = time.localtime(time.time())
    # proxies.extend(load_subscribe_url(f"https://v2rayshare.com/wp-content/uploads/{localtime.tm_year:04}/{localtime.tm_mon:02}/{localtime.tm_year:04}{localtime.tm_mon:02}{localtime.tm_mday:02}.txt"))
    # proxies.extend(manual_input())

    proxies.extend(load_subscribe_url('https://dercylee.us.kg/271828?b64'))
    proxies.extend(load_subscribe_url('https://dercylee.us.kg/271828?sub=zrf.zrf.me'))
    proxies.extend(load_subscribe_url('https://dercylee.us.kg/271828?sub=Trojan.fxxk.dedyn.io'))
    proxies.extend(load_subscribe_url('https://dercylee.us.kg/271828?sub=altrojan.comorg.us.kg'))
    proxies.extend(load_subscribe_url('https://dercylee.us.kg/271828?sub=alvless.comorg.us.kg'))
    proxies.extend(load_subscribe_url('https://dercylee.us.kg/271828?sub=VLESS.fxxk.dedyn.io'))
    proxies.extend(load_subscribe_url('https://oxo.o00o.ooo/ooo'))
    
    

    proxies=list(set(proxies))
    gen_v2ray_subscribe(proxies)
    gen_clash_subscribe(list(filter(None,map(protocol_decode,proxies))))
    
