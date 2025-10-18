# ProxyPool With UI

一个功能完善的代理池系统，带有现代化的 Web 管理界面，支持多种代理协议和 Clash 订阅。

![term](docs/term.png)

## ✨ 核心特性

- 🎯 **自动爬取** - 从 14+ 个免费代理源自动爬取代理
- ✅ **自动验证** - 实时验证代理可用性，只返回可用代理
- 🌐 **多协议支持** - HTTP、HTTPS、SOCKS4、SOCKS5
- 🎨 **现代化 UI** - 基于 Nuxt 3 + Vue 3 + Ant Design Vue
- ⚡ **Clash 订阅** - 一键导入 Clash，支持 50+ 国家节点筛选
- 🔄 **实时监控** - 代理状态、爬取器状态实时展示
- 📍 **地理位置** - 自动识别代理 IP 归属地（国家/城市）
- 🛠️ **手动添加** - 支持手动添加自有代理

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

## 📡 API 接口

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

**参数说明：**
- `c` - 按国家筛选（如：`c=CN,US,JP`）
- `nc` - 排除指定国家（如：`nc=CN`）
- `protocol` - 筛选协议类型（`http`/`https`/`socks5`）
- `limit` - 限制返回数量（如：`limit=50`）

**支持的国家代码：** CN、HK、TW、US、CA、JP、SG、AU、RU、CH、DE、FR、GB、NL 等 50+ 个

**使用示例：**
```bash
# 获取所有代理
http://localhost:5000/clash

# 仅获取美国和日本的代理，限制 50 个
http://localhost:5000/clash?c=US,JP&limit=50

# 排除中国大陆的代理
http://localhost:5000/clash?nc=CN

# 仅获取 SOCKS5 代理
http://localhost:5000/clash?protocol=socks5
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
├── db/               # 数据库封装（SQLite）
├── fetchers/         # 代理爬取器
├── proc/             # 爬取和验证进程
├── frontend/         # Web 前端（Nuxt 3 + Vue 3）
├── utils/            # 工具类（IP 定位等）
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

## 🔧 高级功能

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

## 🛠️ 技术栈

**后端：**
- Python 3.6+
- Flask - Web 框架
- SQLite - 数据库
- Requests - HTTP 库
- PyYAML - Clash 配置生成

**前端：**
- Nuxt 3 - Vue 框架
- Vue 3 - JavaScript 框架
- TypeScript - 类型安全
- Ant Design Vue - UI 组件库
- Vite - 构建工具

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

**版本**: 2.0.0  
**更新时间**: 2025-10-18  
**状态**: ✅ 生产就绪

