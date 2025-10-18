# ProxyPool With UI

一个功能完善的代理池系统，带有现代化的 Web 管理界面，支持多种代理协议和 Clash 订阅。

![term](docs/term.png)

## ✨ 核心特性

- 🎯 **自动爬取** - 从 14+ 个免费代理源自动爬取代理
- ✅ **自动验证** - 实时验证代理可用性，只返回可用代理
- 🌐 **多协议支持** - HTTP、HTTPS、SOCKS4、SOCKS5
- 🎨 **现代化 UI** - 基于 Nuxt 3 + Vue 3 + Ant Design Vue
- ⚡ **Clash 订阅** - 一键导入 Clash，支持 50+ 国家节点筛选
- 🚀 **V2Ray 订阅** - 支持 V2Ray 客户端，Base64 编码格式
- 🔄 **实时监控** - 代理状态、爬取器状态实时展示
- 📍 **地理位置** - 自动识别代理 IP 归属地（国家/城市）
- 🛠️ **手动添加** - 支持手动添加自有代理
- 🔐 **登录鉴权** - JWT Token 认证，保护管理接口安全
- 🔒 **单实例运行** - 防止多实例冲突，确保数据一致性

## 🚀 快速开始

### 方式一：本地运行

```bash
# 1. 克隆项目
git clone https://github.com/huppugo1/ProxyPoolWithUI.git
cd ProxyPoolWithUI

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务
python main.py
```

### 方式二：Docker 运行

```bash
# 1. 克隆项目
git clone https://github.com/huppugo1/ProxyPoolWithUI.git
cd ProxyPoolWithUI

# 2. 构建镜像
docker build --tag proxy_pool .

# 3. 运行容器
docker run -p 5000:5000 -v $(pwd):/proxy -d proxy_pool
```

启动成功后访问：**http://localhost:5000/web**

> 💡 首次启动需要等待 5-10 分钟让系统爬取和验证代理

### 默认登录账户

- **用户名**: `admin`
- **密码**: `admin123`

> ⚠️ **重要提示**: 首次登录后请立即修改默认密码！

## 🔐 登录鉴权

系统已集成 JWT Token 认证机制，所有管理接口均需要登录后才能访问。

### 认证流程

1. **登录获取 Token**
   ```bash
   curl -X POST http://localhost:5000/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin123"}'
   ```

   返回示例：
   ```json
   {
     "success": true,
     "message": "登录成功",
     "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "user": {
       "username": "admin",
       "role": "admin"
     }
   }
   ```

2. **使用 Token 访问接口**
   ```bash
   curl http://localhost:5000/proxies_status \
     -H "Authorization: Bearer YOUR_TOKEN_HERE"
   ```

### 认证接口

| 接口 | 方法 | 说明 | 是否需要认证 |
|------|------|------|--------------|
| `/auth/login` | POST | 用户登录 | ❌ |
| `/auth/verify` | GET | 验证 Token | ✅ |
| `/auth/change_password` | POST | 修改密码 | ✅ |

### Token 说明

- Token 有效期：24 小时（可在 `config.py` 中配置）
- Token 过期后需要重新登录
- 前端会自动处理 Token 过期跳转

### 修改默认密码

登录后点击右上角用户名，选择"修改密码"即可修改。

或通过 API：

```bash
curl -X POST http://localhost:5000/auth/change_password \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"old_password": "admin123", "new_password": "your_new_password"}'
```

## 📡 API 接口

> ⚠️ **注意**: 除了 `/ping`、`/fetch_*`、`/clash*` 和 `/v2ray` 等代理获取接口外，其他管理接口均需要认证。

### 基础接口

| 接口 | 说明 | 示例 |
|------|------|------|
| `/ping` | 测试 API 状态 | `curl http://localhost:5000/ping` |
| `/fetch_random` | 随机获取一个可用代理 | `curl http://localhost:5000/fetch_random` |
| `/fetch_all` | 获取所有可用代理 | `curl http://localhost:5000/fetch_all` |
| `/fetch_http` | 获取一个 HTTP 代理 | `curl http://localhost:5000/fetch_http` |
| `/fetch_https` | 获取一个 HTTPS 代理 | `curl http://localhost:5000/fetch_https` |
| `/fetch_socks5` | 获取一个 SOCKS5 代理 | `curl http://localhost:5000/fetch_socks5` |

### Clash 订阅接口

| 接口 | 说明 | 参数 |
|------|------|------|
| `/clash` | 获取 Clash 完整订阅配置 | `c`, `nc`, `protocol`, `limit` |
| `/clash/proxies` | 获取 Clash 代理节点列表 | `c`, `nc`, `protocol`, `limit` |

### V2Ray 订阅接口

| 接口 | 说明 | 参数 |
|------|------|------|
| `/v2ray` | 获取 V2Ray 订阅配置（Base64 编码） | `c`, `nc`, `protocol`, `limit` |

**参数说明：**
- `c` - 按国家筛选（如：`c=CN,US,JP`）
- `nc` - 排除指定国家（如：`nc=CN`）
- `protocol` - 筛选协议类型（`http`/`https`/`socks4`/`socks5`）
- `limit` - 限制返回数量（如：`limit=50`）

**支持的国家代码：** CN、HK、TW、US、CA、JP、SG、AU、RU、CH、DE、FR、GB、NL 等 50+ 个

**使用示例：**
```bash
# 获取所有代理
http://localhost:5000/clash
http://localhost:5000/v2ray

# 仅获取美国和日本的代理，限制 50 个
http://localhost:5000/clash?c=US,JP&limit=50
http://localhost:5000/v2ray?c=US,JP&limit=50

# 排除中国大陆的代理
http://localhost:5000/clash?nc=CN
http://localhost:5000/v2ray?nc=CN

# 仅获取 SOCKS5 代理
http://localhost:5000/clash?protocol=socks5
http://localhost:5000/v2ray?protocol=socks5
```

## 🎯 Clash 使用指南

### 方法 A：直接订阅（推荐）

1. 打开 Clash 客户端
2. 进入「配置」或「Profiles」
3. 添加订阅链接：`http://localhost:5000/clash`
4. 点击更新订阅并启用

### 方法 B：手动导入

1. 访问：http://localhost:5000/clash
2. 复制返回的 YAML 配置
3. 在 Clash 中创建新配置文件并保存

### 支持的 Clash 客户端

- ✅ Clash for Windows
- ✅ Clash for Android
- ✅ ClashX / ClashX Pro (macOS)
- ✅ Clash Premium
- ✅ Clash Meta / Mihomo

### 使用建议

1. **定期更新** - 建议设置自动更新订阅（每 6 小时）
2. **限制数量** - 使用 `limit` 参数限制代理数量（推荐 20-50 个）
3. **自动测试** - 启用 Clash 自动测试，选择最快的代理
4. **节点名称** - 自动显示国家 emoji 和 IP（如：🇨🇳 中国+1.2.3.4）

## 🚀 V2Ray 使用指南

### 方法 A：直接订阅（推荐）

1. 打开 V2Ray 客户端（如 V2RayN、V2RayX、Qv2ray 等）
2. 进入「订阅」或「Subscription」
3. 添加订阅链接：`http://localhost:5000/v2ray`
4. 点击更新订阅并启用

### 方法 B：手动导入

1. 访问：http://localhost:5000/v2ray
2. 复制返回的 Base64 编码内容
3. 在 V2Ray 客户端中导入订阅

### 支持的 V2Ray 客户端

- ✅ V2RayN (Windows)
- ✅ V2RayX (macOS)
- ✅ Qv2ray (跨平台)
- ✅ V2RayNG (Android)
- ✅ Shadowrocket (iOS)
- ✅ ClashX (macOS)

### 代理格式说明

V2Ray 订阅支持以下代理格式：
- **HTTP/HTTPS 代理** - 转换为 VMess 格式
- **SOCKS4/SOCKS5 代理** - 转换为 socks:// 格式
- **认证信息** - 自动处理用户名密码认证

### 使用建议

1. **定期更新** - 建议设置自动更新订阅（每 6 小时）
2. **限制数量** - 使用 `limit` 参数限制代理数量（推荐 20-50 个）
3. **协议选择** - 根据网络环境选择合适的协议类型
4. **节点测试** - 启用 V2Ray 自动测试，选择最快的代理

## 🐍 Python 使用示例

```python
import requests

# 获取一个随机代理
proxy_uri = requests.get('http://localhost:5000/fetch_random').text

if proxy_uri:
    proxies = {'http': proxy_uri, 'https': proxy_uri}
    response = requests.get('https://www.example.com', proxies=proxies)
    print(response.text)
else:
    print('暂时没有可用代理')
```

## 📦 已集成的代理源

| 名称 | 地址 | 备注 |
|------|------|------|
| 悠悠网络代理 | https://uu-proxy.com/ | |
| 快代理 | https://www.kuaidaili.com/ | |
| 全网代理 | http://www.goubanjia.com/ | |
| 66代理 | http://www.66ip.cn/ | |
| 云代理 | http://www.ip3366.net/ | |
| 免费代理库 | https://ip.jiangxianli.com/ | |
| 小幻HTTP代理 | https://ip.ihuan.me/ | |
| 89免费代理 | https://www.89ip.cn/ | |
| ProxyScan | https://www.proxyscan.io/ | |
| 开心代理 | http://www.kxdaili.com/ | |
| 西拉代理 | http://www.xiladaili.com/ | |
| 小舒代理 | http://www.xsdaili.cn/ | |
| ProxyList | https://www.proxy-list.download/ | |
| ProxyScrape | https://proxyscrape.com/ | 国内无法直接访问 |

## 📁 项目结构

```
ProxyPoolWithUI/
├── api/              # API 服务（Flask）
├── auth/             # 认证模块（JWT）
├── db/               # 数据库封装（SQLite）
├── fetchers/         # 代理爬取器
├── proc/             # 爬取和验证进程
├── frontend/         # Web 前端（Nuxt 3 + Vue 3）
├── utils/            # 工具类（IP 定位、单实例管理）
├── config.py         # 配置文件
└── main.py           # 启动入口
```

## ⚙️ 配置说明

大部分配置在 `config.py` 中，默认配置已经可以适应大部分情况。

### 主要配置项

- **验证超时时间** - 代理验证的超时设置
- **验证间隔** - 代理重新验证的时间间隔
- **爬取间隔** - 爬取器运行的时间间隔
- **数据库路径** - SQLite 数据库文件位置

### 认证配置

在 `config.py` 中可以配置认证相关参数：

```python
# JWT密钥 - 建议在生产环境使用环境变量
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-secret-key-change-it-in-production-2025')

# Token过期时间（小时）
TOKEN_EXPIRATION_HOURS = 24
```

生产环境建议设置环境变量：

```bash
export JWT_SECRET_KEY="your-very-strong-secret-key-here"
python main.py
```

## 🔧 高级功能

### 单实例运行保护

系统具备完善的单实例运行机制，防止多个实例同时运行：

- **端口占用检查** - 检测5000端口是否被占用
- **PID文件锁** - 在用户主目录创建PID文件记录进程ID
- **锁文件机制** - 创建包含时间戳的锁文件，支持过期清理
- **进程状态验证** - 验证PID对应的进程是否真实存在

如果检测到已有实例运行，系统会显示清理命令：

```bash
# Windows 清理命令
taskkill /f /im python.exe
del "%USERPROFILE%\.proxypoolwithui.pid"
del "%USERPROFILE%\.proxypoolwithui.lock"

# Linux/Unix 清理命令
pkill -f python.*main.py
rm -f ~/.proxypoolwithui.pid
rm -f ~/.proxypoolwithui.lock
```

### 添加自定义代理源

详见：[fetchers/README.md](fetchers/README.md)

### 自定义验证算法

详见：[db/README.md](db/README.md)

### 前端开发指南

详见：[frontend/src/README_NUXT3.md](frontend/src/README_NUXT3.md)

## 📊 工作流程

```
[代理源] → [爬取器] → [数据库] → [验证器] → [API] → [用户]
             ↓                      ↓
         [定时爬取]             [定时验证]
```

1. **爬取进程** - 定时从各代理源爬取代理，存入数据库
2. **验证进程** - 定时验证数据库中的代理是否可用
3. **API 服务** - 提供 HTTP 接口和 Web 界面

详细流程图：

![workflow](docs/workflow.png)

## 🔒 生产环境部署

### 安全检查清单

在部署到生产环境之前，请确保完成以下安全检查：

#### 必须完成的项目

1. **JWT 密钥配置**
   - [ ] 修改默认 JWT 密钥
   - [ ] 使用环境变量存储密钥（推荐）
   - [ ] 密钥长度至少 32 位
   - [ ] 使用随机字符串作为密钥

   ```bash
   # 生成强密钥示例
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   
   # 设置环境变量
   export JWT_SECRET_KEY="your-generated-secret-key"
   ```

2. **修改默认密码**
   - [ ] 首次登录后立即修改默认管理员密码
   - [ ] 新密码长度至少 8 位
   - [ ] 包含大小写字母、数字和特殊字符

3. **文件权限**
   ```bash
   chmod 600 users.json
   chmod 600 data.db
   ```

4. **网络安全**
   - [ ] 生产环境使用 HTTPS（必须）
   - [ ] 配置防火墙规则
   - [ ] 限制管理接口访问 IP（推荐）
   - [ ] 使用反向代理（Nginx/Apache）

### Nginx 反向代理配置

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # 安全头
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # 限制上传大小
    client_max_body_size 10M;
}

# HTTP 重定向到 HTTPS
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

### Systemd 服务配置

创建 `/etc/systemd/system/proxypool.service`：

```ini
[Unit]
Description=ProxyPool Management System
After=network.target

[Service]
Type=simple
User=proxypool
WorkingDirectory=/path/to/ProxyPoolWithUI
Environment="JWT_SECRET_KEY=your-secret-key-here"
ExecStart=/usr/bin/python3 /path/to/ProxyPoolWithUI/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable proxypool
sudo systemctl start proxypool
sudo systemctl status proxypool
```

### Docker 部署安全配置

```dockerfile
# 使用非 root 用户
RUN adduser --disabled-password --gecos '' proxypool
USER proxypool

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/ping || exit 1
```

运行容器：

```bash
docker run -d \
  --name proxypool \
  -p 5000:5000 \
  -e JWT_SECRET_KEY="your-secret-key" \
  -v /path/to/data:/proxy \
  --restart unless-stopped \
  --read-only \
  --tmpfs /tmp \
  proxy_pool
```

## ❓ 常见问题

### Q: 没有可用代理？
A: 首次启动需要等待 5-10 分钟。访问 http://localhost:5000/web 查看爬取和验证状态。

### Q: 代理不稳定？
A: 免费代理质量参差不齐，建议：
- 使用 Clash 自动测试功能
- 定期更新订阅
- 使用 `limit` 参数限制数量

### Q: 如何禁用某个爬取器？
A: 在 Web 界面的「爬取器状态」页面中操作，或访问 API：
```bash
http://localhost:5000/fetcher_enable?name=爬取器名称&enable=0
```

### Q: 如何远程访问？
A: 将 `localhost` 替换为服务器 IP，并确保防火墙允许 5000 端口。

### Q: Docker 容器如何持久化数据？
A: 使用 `-v` 参数挂载数据目录：
```bash
docker run -p 5000:5000 -v /path/to/data:/proxy -d proxy_pool
```

### Q: 忘记密码怎么办？
A: 删除项目根目录下的 `users.json` 文件，重启服务会自动创建默认管理员账户。

### Q: 如何禁用登录认证？
A: 不建议禁用认证。如果确实需要，可以在 `api/api.py` 中移除需要保护接口的 `@token_required` 装饰器。

### Q: API 接口需要认证吗？
A: 
- **需要认证**：所有管理接口（代理状态、爬取器管理、添加代理等）
- **无需认证**：代理获取接口（`/fetch_*`、`/clash*`、`/v2ray`）和健康检查（`/ping`）

### Q: 支持哪些订阅格式？
A: 
- **Clash 订阅**：`/clash` - 返回 YAML 格式配置
- **V2Ray 订阅**：`/v2ray` - 返回 Base64 编码的代理链接
- **代理列表**：`/clash/proxies` - 仅返回 Clash 代理节点列表

### Q: 提示"检测到已有实例在运行"？
A: 系统具备单实例保护机制。如果确定没有其他实例运行，可以手动清理锁文件：
```bash
# Windows
del "%USERPROFILE%\.proxypoolwithui.pid"
del "%USERPROFILE%\.proxypoolwithui.lock"

# Linux/Mac
rm ~/.proxypoolwithui.pid
rm ~/.proxypoolwithui.lock
```

### Q: 如何修改 JWT 密钥？
A: 生产环境建议使用环境变量：
```bash
export JWT_SECRET_KEY="your-very-strong-secret-key"
python main.py
```

## 🛠️ 技术栈

**后端：**
- Python 3.6+
- Flask - Web 框架
- SQLite - 数据库
- Requests - HTTP 库
- PyYAML - Clash 配置生成
- PyJWT - JWT 认证
- psutil - 进程管理

**前端：**
- Nuxt 3 - Vue 框架
- Vue 3 - JavaScript 框架
- TypeScript - 类型安全
- Ant Design Vue - UI 组件库
- Vite - 构建工具
- Axios - HTTP 客户端

## 📝 开发贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- 感谢所有免费代理源提供者
- 感谢开源社区的贡献者

---

**版本**: 2.0.1  
**更新时间**: 2025-10-18  
**状态**: ✅ 生产就绪

## 🔄 更新日志

### v2.0.1 (2025-10-18)
- ✨ 新增 JWT Token 登录鉴权功能
- 🔐 所有管理接口添加认证保护
- 👤 用户管理：登录、修改密码
- 🎨 全新登录页面设计
- 🛡️ 自动 Token 刷新和过期处理
- 🔒 单实例运行保护机制
- 📝 完善的认证 API 文档
- 🧹 代码优化和文档合并

### v2.0.0
- 初始版本发布
