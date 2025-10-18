# 爬取器扩展信息支持说明

## 📝 概述

爬取器支持返回代理的扩展信息，包括：
- **账号密码**：由爬取器从网站爬取（如果有）
- **地理位置**：国家和地址信息（如果网站提供）

这些信息都是**可选的**，如果爬取器能获取到就直接返回，如果获取不到：
- 账号密码保持为 `None`（表示无需认证）
- 国家地址在验证成功后自动获取

## 🔧 返回格式

爬取器的 `fetch()` 方法支持三种格式：

### 1️⃣ 基本格式（只有代理信息）
```python
('http', '127.0.0.1', 8080)
```

### 2️⃣ 包含认证信息
```python
('socks5', '1.2.3.4', 1080, 'user123', 'pass456')
```

### 3️⃣ 完整信息（认证 + 地理位置）
```python
('socks5', '1.2.3.4', 1080, 'user123', 'pass456', '美国', '洛杉矶')
```

### 4️⃣ 只有地理位置，无认证
```python
('http', '5.6.7.8', 8080, None, None, '日本', '东京')
```

## 📚 示例代码

### 示例 1: 爬取无认证代理（现有所有爬取器）

```python
# encoding: utf-8

from .BaseFetcher import BaseFetcher
from pyquery import PyQuery as pq
import requests

class ExampleFetcher(BaseFetcher):
    """
    示例爬取器 - 无认证代理
    """

    def fetch(self):
        proxies = []
        
        url = 'https://example.com/free-proxy'
        response = requests.get(url, timeout=15)
        doc = pq(response.text)
        
        for item in doc('table tr').items():
            ip = item.find('td:nth-child(1)').text()
            port = int(item.find('td:nth-child(2)').text())
            protocol = item.find('td:nth-child(3)').text().lower()
            
            # 返回三元组: (protocol, ip, port)
            proxies.append((protocol, ip, port))
        
        return proxies
```

### 示例 2: 爬取有认证代理（新功能）

```python
# encoding: utf-8

from .BaseFetcher import BaseFetcher
from pyquery import PyQuery as pq
import requests

class PaidProxyFetcher(BaseFetcher):
    """
    示例爬取器 - 付费代理（带账号密码）
    """

    def fetch(self):
        proxies = []
        
        url = 'https://example.com/paid-proxy-list'
        response = requests.get(url, timeout=15)
        doc = pq(response.text)
        
        for item in doc('table tr').items():
            ip = item.find('td:nth-child(1)').text()
            port = int(item.find('td:nth-child(2)').text())
            protocol = item.find('td:nth-child(3)').text().lower()
            username = item.find('td:nth-child(4)').text()
            password = item.find('td:nth-child(5)').text()
            
            # 如果爬到了账号密码，返回五元组
            if username and password:
                proxies.append((protocol, ip, port, username, password))
            else:
                # 如果没有账号密码，返回三元组
                proxies.append((protocol, ip, port))
        
        return proxies
```

### 示例 3: 包含地理位置信息

```python
# encoding: utf-8

from .BaseFetcher import BaseFetcher
import requests

class LocationProxyFetcher(BaseFetcher):
    """
    示例爬取器 - 包含地理位置
    """

    def fetch(self):
        proxies = []
        
        url = 'https://example.com/proxy-with-location'
        response = requests.get(url, timeout=15)
        data = response.json()
        
        for item in data['proxies']:
            protocol = item['protocol']
            ip = item['ip']
            port = item['port']
            country = item.get('country')  # 可能为 None
            address = item.get('address')  # 可能为 None
            username = item.get('username')  # 可能为 None
            password = item.get('password')  # 可能为 None
            
            # 返回完整信息（7元组）
            if username or password or country or address:
                proxies.append((protocol, ip, port, username, password, country, address))
            # 或者返回基本信息（3元组）
            else:
                proxies.append((protocol, ip, port))
        
        return proxies
```

### 示例 4: 混合返回（不同格式）

```python
# encoding: utf-8

from .BaseFetcher import BaseFetcher
import requests

class MixedFormatFetcher(BaseFetcher):
    """
    示例爬取器 - 混合格式返回
    """

    def fetch(self):
        proxies = []
        
        # 场景1: 免费代理，无任何额外信息
        proxies.append(('http', '1.2.3.4', 8080))
        
        # 场景2: 付费代理，有认证信息
        proxies.append(('socks5', '5.6.7.8', 1080, 'user1', 'pass1'))
        
        # 场景3: 完整信息（认证 + 地理位置）
        proxies.append(('socks5', '9.10.11.12', 1080, 'user2', 'pass2', '美国', '纽约'))
        
        # 场景4: 只有地理位置，无认证
        proxies.append(('http', '13.14.15.16', 8080, None, None, '日本', '东京'))
        
        return proxies
```

## ✅ 数据流程

### 入库阶段（爬取器 → 数据库）
1. **爬取器** 从网站爬取代理信息
   - 如果网站提供了 username/password/country/address，直接返回
   - 如果没有，返回 `None` 或省略该字段
2. **run_fetcher.py** 自动识别格式（3/5/7元组）
3. **conn.pushNewFetch()** 将数据写入数据库
   - 爬取器提供的信息直接写入
   - 未提供的信息保持为 `NULL`

### 验证阶段（验证器 → 更新地理位置）
4. **验证器** 验证代理是否可用
5. **conn.pushValidateResult()** 
   - 如果验证成功 **且** 没有地理位置信息
   - 自动调用 IP 地理位置 API 获取 country 和 address
   - 更新到数据库

### 展示阶段（前端）
6. **前端** 显示代理信息
   - 有值显示实际值
   - `NULL` 显示"未知"

## ⚠️ 注意事项

### ✅ 推荐做法
1. **爬取器能获取到的信息，直接返回**
   - 减少后续 API 查询次数
   - 提高系统效率
2. **如果网站提供地理位置信息，建议返回**
   - 格式：`(protocol, ip, port, username, password, country, address)`
   - username/password 可以为 `None`
3. **账号密码从网站爬取**
   - 不要硬编码默认值

### ❌ 不推荐做法
1. 不要在爬取器中调用 IP 地理位置 API
   - 会导致爬取速度变慢
   - 系统会在验证成功后自动获取
2. 不要设置默认值（如 'test1', 'unknown'）
   - 返回 `None` 即可

## 🎯 格式选择指南

| 网站提供的信息 | 推荐返回格式 | 示例 |
|---|---|---|
| 只有IP和端口 | 3元组 | `('http', '1.2.3.4', 8080)` |
| IP + 认证信息 | 5元组 | `('socks5', '1.2.3.4', 1080, 'user', 'pass')` |
| IP + 地理位置 | 7元组 | `('http', '1.2.3.4', 8080, None, None, '美国', '纽约')` |
| 完整信息 | 7元组 | `('socks5', '1.2.3.4', 1080, 'user', 'pass', '日本', '东京')` |

## 🔄 兼容性

- **现有爬取器**：无需修改，继续返回 3元组即可
- **新爬取器**：根据网站提供的信息，选择合适的格式

