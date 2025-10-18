# encoding: utf-8

"""
爬取器通用工具函数
提供统一的请求处理、反爬虫规避等功能
"""

import random
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib3

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 常用的 User-Agent 列表
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
]

def get_default_headers(referer=None):
    """
    获取默认的请求头，模拟浏览器
    
    Args:
        referer: 可选的 Referer 头
    
    Returns:
        dict: 请求头字典
    """
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    }
    
    if referer:
        headers['Referer'] = referer
    
    return headers

def create_session_with_retry(retries=3, backoff_factor=1):
    """
    创建带有重试机制的 requests Session
    
    Args:
        retries: 重试次数
        backoff_factor: 退避因子
    
    Returns:
        requests.Session: 配置好的 Session 对象
    """
    session = requests.Session()
    retry = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[500, 502, 503, 504, 429]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def safe_get(url, headers=None, timeout=15, verify=True, delay_range=(0.5, 2)):
    """
    安全的 GET 请求，自动添加请求头、重试、延迟等
    
    Args:
        url: 请求 URL
        headers: 自定义请求头（会与默认请求头合并）
        timeout: 超时时间（秒）
        verify: 是否验证 SSL 证书
        delay_range: 随机延迟范围（秒），设为 None 则不延迟
    
    Returns:
        requests.Response: 响应对象
    
    Raises:
        Exception: 请求失败时抛出异常
    """
    # 添加随机延迟，避免请求过快
    if delay_range:
        time.sleep(random.uniform(delay_range[0], delay_range[1]))
    
    # 准备请求头
    default_headers = get_default_headers()
    if headers:
        default_headers.update(headers)
    
    # 创建带重试的 session
    session = create_session_with_retry()
    
    # 发送请求
    response = session.get(url, headers=default_headers, timeout=timeout, verify=verify)
    response.raise_for_status()
    
    return response

