# encoding: utf-8

from .BaseFetcher import BaseFetcher
from .FetcherUtils import safe_get
from pyquery import PyQuery as pq

class KuaidailiFetcher(BaseFetcher):
    """
    https://www.kuaidaili.com/free
    """

    def fetch(self):
        """
        执行一次爬取，返回一个数组，每个元素是(protocol, ip, port)，portocal是协议名称，目前主要为http
        返回示例：[('http', '127.0.0.1', 8080), ('http', '127.0.0.1', 1234)]
        """
        
        # 减少页面数量，避免触发反爬虫
        urls = []
        urls = urls + [f'https://www.kuaidaili.com/free/inha/{page}/' for page in range(1, 4)]  # 只爬前3页
        urls = urls + [f'https://www.kuaidaili.com/free/intr/{page}/' for page in range(1, 4)]  # 只爬前3页

        proxies = []
        
        # 自定义请求头
        headers = {
            'Referer': 'https://www.kuaidaili.com/'
        }

        for url in urls:
            try:
                # 使用 safe_get 自动处理反爬虫
                response = safe_get(url, headers=headers, delay_range=(1, 3))
                html = response.text
                
                doc = pq(html)
                for item in doc('table tbody tr').items():
                    try:
                        ip = item.find('td[data-title="IP"]').text()
                        port_text = item.find('td[data-title="PORT"]').text()
                        
                        if ip and port_text:
                            port = int(port_text)
                            proxies.append(('http', ip, port))
                    except (ValueError, AttributeError):
                        continue
                        
            except Exception as e:
                # 单个页面失败不影响其他页面
                print(f"爬取 {url} 失败: {e}")
                continue
        
        return list(set(proxies))
