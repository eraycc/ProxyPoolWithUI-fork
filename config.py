# encoding: utf-8

"""
配置文件，一般来说不需要修改
如果需要启用或者禁用某些网站的爬取器，可在网页上进行配置
"""

import os

# 数据库文件路径
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'data.db')

# 每次运行所有爬取器之后，睡眠多少时间，单位秒
PROC_FETCHER_SLEEP = 5 * 60

# 验证器每次睡眠的时间，单位秒
PROC_VALIDATOR_SLEEP = 5

# 验证器的配置参数
VALIDATE_THREAD_NUM = 200 # 验证线程数量
# 验证器的逻辑是：
# 使用代理访问 VALIDATE_URL 网站，超时时间设置为 VALIDATE_TIMEOUT
# 如果没有超时：
# 1、若选择的验证方式为GET：  返回的网页中包含 VALIDATE_KEYWORD 文字，那么就认为本次验证成功
# 2、若选择的验证方式为HEAD： 返回的响应头中，对于的 VALIDATE_HEADER 响应字段内容包含 VALIDATE_KEYWORD 内容，那么就认为本次验证成功
# 上述过程最多进行 VALIDATE_MAX_FAILS 次，只要有一次成功，就认为代理可用
VALIDATE_URL = 'https://qq.com'
VALIDATE_METHOD = 'HEAD' # 验证方式，可选：GET、HEAD
VALIDATE_HEADER = 'location' # 仅用于HEAD验证方式，百度响应头Server字段KEYWORD可填：bfe
VALIDATE_KEYWORD = 'www.qq.com'
VALIDATE_TIMEOUT = 5 # 超时时间，单位s
VALIDATE_MAX_FAILS = 3

# ============= 认证配置 =============

# JWT密钥 - 用于签名Token，请在生产环境中修改为强密钥
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-secret-key-change-it-in-production-2025')

# Token过期时间（小时）
TOKEN_EXPIRATION_HOURS = 24

# 默认管理员账户
# 首次启动会自动创建，用户名：admin，密码：admin123
# 登录后请立即修改密码

# 初始化认证管理器
from auth import AuthManager
auth_manager = AuthManager(
    secret_key=JWT_SECRET_KEY,
    token_expiration_hours=TOKEN_EXPIRATION_HOURS
)