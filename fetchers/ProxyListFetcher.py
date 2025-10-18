import time
import warnings

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib3

from .BaseFetcher import BaseFetcher

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ProxyListFetcher(BaseFetcher):
    """
    https://www.proxy-list.download/api/v1/get?type={{ protocol }}&_t={{ timestamp }}
    """

    def fetch(self):
        proxies = []
        type_list = ['socks4', 'socks5', 'http', 'https']
        
        # 配置重试策略
        session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        for protocol in type_list:
            try:
                url = "https://www.proxy-list.download/api/v1/get?type=" + protocol + "&_t=" + str(time.time())
                # 禁用SSL验证，增加超时
                response = session.get(url, verify=False, timeout=15)
                proxies_list = response.text.split("\n")
                
                for data in proxies_list:
                    if not data or ':' not in data:
                        continue
                    flag_idx = data.find(":")
                    ip = data[:flag_idx].strip()
                    port_str = data[flag_idx + 1:].strip()
                    
                    # 验证IP和端口格式
                    if ip and port_str:
                        try:
                            port = int(port_str)
                            if 1 <= port <= 65535:
                                proxies.append((protocol, ip, port))
                        except ValueError:
                            continue
            except Exception as e:
                # 单个协议失败不影响其他协议
                print(f"获取 {protocol} 代理失败: {e}")
                continue

        return list(set(proxies))
