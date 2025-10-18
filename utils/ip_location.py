# encoding: utf-8

import requests
import time

class IPLocation:
    """
    IP地理位置查询工具
    使用免费的IP API服务查询IP地址的国家和详细地址
    """
    
    @staticmethod
    def get_location(ip: str) -> dict:
        """
        获取IP地址的地理位置信息
        返回: {'country': '国家', 'address': '详细地址'}
        """
        # 检查是否为内网IP
        if ip.startswith('192.168') or ip.startswith('10.') or ip.startswith('172.16') or ip.startswith('127.'):
            return {'country': '本地', 'address': '内网地址'}
        
        # 尝试多个免费API服务
        result = IPLocation._try_ip_api_com(ip)
        if result:
            return result
        
        # 如果第一个API失败，尝试第二个
        result = IPLocation._try_ipapi_co(ip)
        if result:
            return result
        
        # 如果都失败，返回默认值
        return {'country': '未知', 'address': '无法获取'}
    
    @staticmethod
    def _try_ip_api_com(ip: str) -> dict:
        """
        使用 ip-api.com 查询
        免费限制: 45次/分钟
        """
        try:
            url = f'http://ip-api.com/json/{ip}?lang=zh-CN&fields=status,country,regionName,city,isp'
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    country = data.get('country', '未知')
                    region = data.get('regionName', '')
                    city = data.get('city', '')
                    isp = data.get('isp', '')
                    
                    # 组合详细地址
                    address_parts = [part for part in [country, region, city, isp] if part]
                    address = ' '.join(address_parts)
                    
                    return {'country': country, 'address': address}
        except Exception as e:
            print(f"IP查询失败(ip-api.com): {e}")
        
        return None
    
    @staticmethod
    def _try_ipapi_co(ip: str) -> dict:
        """
        使用 ipapi.co 查询
        免费限制: 1000次/天
        """
        try:
            url = f'https://ipapi.co/{ip}/json/'
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                data = response.json()
                country = data.get('country_name', '未知')
                region = data.get('region', '')
                city = data.get('city', '')
                org = data.get('org', '')
                
                # 组合详细地址
                address_parts = [part for part in [country, region, city, org] if part]
                address = ' '.join(address_parts)
                
                return {'country': country, 'address': address}
        except Exception as e:
            print(f"IP查询失败(ipapi.co): {e}")
        
        return None

# 缓存，避免重复查询同一个IP
_ip_cache = {}
_cache_expire_time = 3600  # 缓存1小时

def get_ip_location_cached(ip: str) -> dict:
    """
    带缓存的IP位置查询
    """
    current_time = time.time()
    
    # 检查缓存
    if ip in _ip_cache:
        cached_data, cache_time = _ip_cache[ip]
        if current_time - cache_time < _cache_expire_time:
            return cached_data
    
    # 查询新数据
    result = IPLocation.get_location(ip)
    _ip_cache[ip] = (result, current_time)
    
    return result

