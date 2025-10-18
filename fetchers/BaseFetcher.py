# encoding: utf-8

class BaseFetcher(object):
    """
    所有爬取器的基类
    """

    def fetch(self):
        """
        执行一次爬取，返回一个数组
        每个元素可以是以下格式之一：
        1. (protocol, ip, port) - 最基本，只有代理信息
        2. (protocol, ip, port, username, password) - 包含认证信息
        3. (protocol, ip, port, username, password, country, address) - 包含完整信息
        
        protocol是协议名称，目前主要为http/https/socks5等
        
        返回示例：
        [
            ('http', '127.0.0.1', 8080),  # 只有代理
            ('socks5', '1.2.3.4', 1080, 'user1', 'pass1'),  # 有认证
            ('socks5', '1.2.3.4', 1080, 'user1', 'pass1', '美国', '洛杉矶'),  # 完整信息
            ('http', '5.6.7.8', 8080, None, None, '日本', '东京'),  # 有位置无认证
        ]
        
        说明：
        - username/password 为 None 表示无需认证
        - country/address 为 None 表示未知，系统会在验证成功后自动获取
        - 如果爬取器能获取到这些信息，建议直接返回，减少后续查询
        """
        raise NotImplementedError()
