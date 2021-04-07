import os
import uuid
import time
import whois
import random
import requests
import tldextract
from django.conf import settings

shodan_api_keys = ['i37Ufat06GkptmiWLSD5GHh0jkR28VCq', '3wcRxSjFlNR6JaJcfctB5vZp3w9ZbZSd', '2d6xiC0oN2V1NtjBWSdkJa3fPia4glx9']
zoomeye_api_keys = ['D85a12af-136B-7017E-5CD9-dF79C0ffb1a']


# shodan api,传入ip
def request_shodan_io_api(site, flag, page, config={}):  # 请求shodan api

    if config.get('shodan'):
        key = config.get('shodan')
    else:
        key = random.choice(shodan_api_keys)
    if flag == 1:  # ip
        ip_info = {
            'ip': site,
            'service_ports': [],
            'asn_code': '',
            'protocol_list': [],
            'vulns': [],
            'country_name': '',
            'org': '',
            'isp': '',
            'last_update': ''
        }
        url = f'https://api.shodan.io/shodan/host/{site}?key={key}'
        try:
            res = requests.get(url, timeout=30)
        except:
            print('shodan请求超时/出错')
            return ip_info
        if res.status_code == 200:
            try:
                data = res.json()
            except:
                return ip_info
            ip_info['country_name'] = data['country_name']
            ip_info['org'] = data['org']
            ip_info['isp'] = data['isp']
            ip_info['last_update'] = data['last_update']
            ip_info['asn_code'] = data['asn']
            ip_info['ports'] = data['ports']
            for item in data.get('data', []):
                ip_info['protocol_list'].append(item['_shodan']['module'])
            for item in data.get('data', []):
                ip_info['vulns'] += [{'name': vuln, 'summary': item['vulns'][vuln]['summary']} for vuln in item.get('vulns', [])]
        return ip_info
    elif flag == 2:  # 域名
        url = f'https://api.shodan.io/shodan/host/search?key={key}&query={site}&page={page}'
        try:
            res = requests.get(url, timeout=30)
        except:
            print('shodan请求超时/出错')
            return {}
        try:
            data = res.json()
        except:
            print('返回出错')
            return {}
        total = data['total']
        matches = [{'ip': item['ip_str'], 'timestamp': item['timestamp'], 'portinfo': {'port': item['port'], 'service': item['_shodan']['module']}, 'country': item['location']['country_name'], 'info': item['data']} for item in data['matches']]
        return {
            'total': total,
            'data': matches
        }
    elif flag == 3:  # 网段
        return {}
    else:
        return {}


# zoomeye api查询
def request_zoomeye_api(site, flag, page, config={}):
    if config.get('zoomeye'):
        key = config.get('zoomeye')
    else:
        key = random.choice(zoomeye_api_keys)
    headers = {
        'API-KEY': key
    }
    if flag == 1:  # ip
        url = f'https://api.zoomeye.org/host/search?query=ip:{site}&page={page}'
        try:
            res = requests.get(url, headers=headers, timeout=30)
        except Exception as e:
            print('zoomeye请求超时/出错')
            return {}
        try:
            data = res.json()
        except:
            print('返回出错')
            return {}
        total = data['total']
        matches = [{'ip': item['ip'], 'timestamp': item['timestamp'],
                    'portinfo': {'port': item['portinfo']['port'], 'service': item['portinfo']['service']},
                    'country': item['geoinfo']['country']['names']['zh-CN'], 'info': item['portinfo']['banner']} for
                   item in data['matches']]
        return {
            'total': total,
            'data': matches
        }
    elif flag == 2:  # 域名
        url = f'https://api.zoomeye.org/host/search?query=site:{site}&page={page}'
        try:
            res = requests.get(url, headers=headers, timeout=30)
        except Exception as e:
            print('zoomeye请求超时/出错')
            return {}
        try:
            data = res.json()
        except:
            print('返回出错')
            return {}
        total = data['total']
        matches = [{'ip': item['ip'], 'timestamp': item['timestamp'], 'portinfo': {'port': item['portinfo']['port'], 'service': item['portinfo']['service']}, 'country': item['geoinfo']['country']['names']['zh-CN'], 'info': item['portinfo']['banner']} for item in data['matches']]
        return {
            'total': total,
            'data': matches
        }
    elif flag == 3:  # 网段
        url = f'https://api.zoomeye.org/host/search?query=cidr:{site}&page={page}'
        try:
            res = requests.get(url, headers=headers, timeout=30)
        except:
            print('zoomeye请求超时/出错')
            return {}
        try:
            data = res.json()
        except:
            print('返回出错')
            return {}
        total = data['total']
        matches = [{'ip': item['ip'], 'timestamp': item['timestamp'], 'portinfo': {'port': item['portinfo']['port'], 'service': item['portinfo']['service']}, 'country': item['geoinfo']['country']['names']['zh-CN'], 'info': item['portinfo']['banner']} for item in data['matches']]
        return {
            'total': total,
            'data': matches
        }

    else:
        return {}


# dirsearch目录扫描
def dirsearch_func(site, report_name, config={}):
    search_dir = settings.BASE_DIR + '/webscanApp/dirsearch'
    report_dir = search_dir + '/reports'
    report_path = os.path.join(report_dir, report_name)
    proxy = config.get('proxy')
    if proxy:
        cmd = f'cd {search_dir} && python dirsearch.py -u {site} -e php,asp,jsp,aspx --proxy http://{proxy} --json-report {report_path}'
    else:
        cmd = f'cd {search_dir} python dirsearch.py -u {site} -e php,asp,jsp,aspx --json-report {report_path}'
    os.system(cmd)
    for _ in range(10):
        if not os.path.exists(report_path):
            time.sleep(1)
        else:
            break
    else:
        print('获取报告失败')
        return None
    return report_path


# whois信息查询
def whois_func(site):
    reg_domain = tldextract.extract(site).registered_domain
    item = {}
    item['domain'] = reg_domain
    for _ in range(5):
        res = whois.whois(reg_domain)
        if not res['domain_name']:
            time.sleep(2)
            continue
        item['whois_server'] = res['whois_server']
        item['update_time'] = res['updated_date']
        item['create_time'] = res['creation_date']
        item['expire_time'] = res['expiration_date']
        item['name_server'] = res['name_servers']
        item['email'] = res['emails']
        item['phone'] = ""
        item['registrar'] = res['registrar']
        item['registrant_state'] = res['state']
        item['error'] = ""
        break

    return item
