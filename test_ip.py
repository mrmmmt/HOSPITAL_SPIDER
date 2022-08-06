# 检测代理ip是否有效
import requests


def test_ip(proxy):
    if len(proxy) != 1:
        raise KeyError('只能输入1个代理IP')
    url = 'http://icanhazip.com'
    ip = proxy[list(proxy.keys())[0]].split(':')[0]
    r = requests.get(url, proxy)
    if r.text.strip() == ip:
        print('ip:', r.text.strip(), 'succ')
        return True
    else:
        print('ip:', r.text.strip(), 'fail')
        return False

if __name__ == '__main__':
    proxy = {
        'http': '59.124.224.205:3128'
    }
    test_ip(proxy)
