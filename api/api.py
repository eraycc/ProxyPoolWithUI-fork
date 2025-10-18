# encoding: utf-8

import os
import logging
import yaml
import sqlite3
import datetime
from flask import Flask
from flask import jsonify, request, redirect, send_from_directory, Response

log = logging.getLogger('werkzeug')
log.disabled = True

try:
    from db import conn
except:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from db import conn

STATIC_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'frontend', 'deployment', 'public')

app = Flask(
    __name__,
    static_url_path='/web',
    static_folder=STATIC_FOLDER
)

############# 以下API可用于获取代理 ################

# 可用于测试API状态
@app.route('/ping', methods=['GET'])
def ping():
    return 'API OK'

# 随机获取一个可用代理，如果没有可用代理则返回空白
@app.route('/fetch_random', methods=['GET'])
def fetch_random():
    proxies = conn.getValidatedRandom(1)
    if len(proxies) > 0:
        p = proxies[0]
        return f'{p.protocol}://{p.ip}:{p.port}'
    else:
        return ''

############# 新增加接口int ################        

#api 获取协议为http的一条结果
@app.route('/fetch_http', methods=['GET'])
def fetch_http():
    proxies =conn.get_by_protocol('http', 1)
    if len(proxies) > 0:
        p = proxies[0]
        return f'{p.protocol}://{p.ip}:{p.port}'
    else:
        return ''

#api 获取协议为http的全部结果
@app.route('/fetch_http_all', methods=['GET'])
def fetch_http_all():
    proxies = conn.get_by_protocol('http', -1)
    if len(proxies) == 1:
        p = proxies[0]
        return f'{p.protocol}://{p.ip}:{p.port}'
    elif len(proxies) > 1:
        proxy_list = []
        for p in proxies:
            proxy_list.append(f'{p.protocol}://{p.ip}:{p.port}')
        return ','.join(proxy_list)
    else:
        return ''
        
#api 获取协议为https的一条结果
@app.route('/fetch_https', methods=['GET'])
def fetch_https():
    proxies =conn.get_by_protocol('https', 1)
    if len(proxies) > 0:
        p = proxies[0]
        return f'{p.protocol}://{p.ip}:{p.port}'
    else:
        return ''

#api 获取协议为https的全部结果
@app.route('/fetch_https_all', methods=['GET'])
def fetch_https_all():
    proxies = conn.get_by_protocol('https', -1)
    if len(proxies) == 1:
        p = proxies[0]
        return f'{p.protocol}://{p.ip}:{p.port}'
    elif len(proxies) > 1:
        proxy_list = []
        for p in proxies:
            proxy_list.append(f'{p.protocol}://{p.ip}:{p.port}')
        return ','.join(proxy_list)
    else:
        return ''
                
#api 获取协议为http的一条结果
@app.route('/fetch_socks4', methods=['GET'])
def fetch_socks4():
    proxies =conn.get_by_protocol('socks4', 1)
    if len(proxies) > 0:
        p = proxies[0]
        return f'{p.protocol}://{p.ip}:{p.port}'
    else:
        return ''

#api 获取协议为http的全部结果
@app.route('/fetch_socks4_all', methods=['GET'])
def fetch_socks4_all():
    proxies = conn.get_by_protocol('socks4', -1)
    if len(proxies) == 1:
        p = proxies[0]
        return f'{p.protocol}://{p.ip}:{p.port}'
    elif len(proxies) > 1:
        proxy_list = []
        for p in proxies:
            proxy_list.append(f'{p.protocol}://{p.ip}:{p.port}')
        return ','.join(proxy_list)
    else:
        return ''
        
#api 获取协议为https的一条结果
@app.route('/fetch_socks5', methods=['GET'])
def fetch_socks5():
    proxies =conn.get_by_protocol('socks5', 1)
    if len(proxies) > 0:
        p = proxies[0]
        return f'{p.protocol}://{p.ip}:{p.port}'
    else:
        return ''

#api 获取协议为https的全部结果
@app.route('/fetch_socks5_all', methods=['GET'])
def fetch_socks5_all():
    proxies = conn.get_by_protocol('socks5', -1)
    if len(proxies) == 1:
        p = proxies[0]
        return f'{p.protocol}://{p.ip}:{p.port}'
    elif len(proxies) > 1:
        proxy_list = []
        for p in proxies:
            proxy_list.append(f'{p.protocol}://{p.ip}:{p.port}')
        return ','.join(proxy_list)
    else:
        return ''
                        
############# 新增加接口end ################    

# 获取所有可用代理，如果没有可用代理则返回空白
@app.route('/fetch_all', methods=['GET'])
def fetch_all():
    proxies = conn.getValidatedRandom(-1)
    proxies = [f'{p.protocol}://{p.ip}:{p.port}' for p in proxies]
    return ','.join(proxies)

############# Clash 订阅接口 ################

# Clash 订阅接口 - 完整配置
@app.route('/clash', methods=['GET'])
def clash_subscribe():
    """
    返回 Clash 订阅配置（YAML 格式）
    支持参数：
    - c: 按国家筛选，多个国家用逗号分隔 (如: c=CN,US)
    - nc: 排除指定国家 (如: nc=CN)
    - protocol: 筛选协议类型（http/https/socks5）
    - limit: 限制代理数量，默认返回全部
    """
    try:
        # 获取查询参数
        countries = request.args.get('c', '').upper().split(',') if request.args.get('c') else None
        exclude_countries = request.args.get('nc', '').upper().split(',') if request.args.get('nc') else None
        protocol = request.args.get('protocol', None)
        limit = request.args.get('limit', -1, type=int)
        
        print(f"[clash] 请求参数: countries={countries}, exclude={exclude_countries}, protocol={protocol}, limit={limit}")
        
        # 从数据库获取代理
        if protocol:
            proxies = conn.get_by_protocol(protocol, limit)
        else:
            proxies = conn.getValidatedRandom(limit)
        
        # 按国家筛选
        if countries and countries != ['']:
            # 简单的国家代码映射
            country_map = {
                'CN': '中国', 'HK': '香港', 'TW': '台湾',
                'US': '美国', 'CA': '加拿大',
                'JP': '日本', 'SG': '新加坡',
                'AU': '澳大利亚', 'RU': '俄罗斯',
                'CH': '瑞士', 'DE': '德国', 'FR': '法国',
                'GB': '英国', 'NL': '荷兰'
            }
            country_names = [country_map.get(c, c) for c in countries if c]
            proxies = [p for p in proxies if p.country in country_names]
            print(f"[clash] 国家筛选后: {len(proxies)} 个代理")
        
        # 排除指定国家
        if exclude_countries and exclude_countries != ['']:
            country_map = {
                'CN': '中国', 'HK': '香港', 'TW': '台湾',
                'US': '美国', 'CA': '加拿大',
                'JP': '日本', 'SG': '新加坡',
                'AU': '澳大利亚', 'RU': '俄罗斯',
                'CH': '瑞士', 'DE': '德国', 'FR': '法国',
                'GB': '英国', 'NL': '荷兰'
            }
            exclude_names = [country_map.get(c, c) for c in exclude_countries if c]
            proxies = [p for p in proxies if p.country not in exclude_names]
            print(f"[clash] 排除国家后: {len(proxies)} 个代理")
        
        if not proxies:
            return Response('# 暂无可用代理\nproxies: []\n', mimetype='text/yaml; charset=utf-8')
        
        # 构建完整的 Clash 配置
        clash_config = {
            'port': 7890,
            'socks-port': 7891,
            'allow-lan': False,
            'mode': 'rule',
            'log-level': 'info',
            'external-controller': '127.0.0.1:9090',
            'proxies': []
        }
        
        # 将代理转换为 Clash 格式
        proxy_names = []
        
        # 扩展的国家 emoji 映射表
        country_emoji_map = {
            '中国': '🇨🇳', '香港': '🇭🇰', '台湾': '🇹🇼',
            '美国': '🇺🇸', '加拿大': '🇨🇦',
            '日本': '🇯🇵', '新加坡': '🇸🇬',
            '澳大利亚': '🇦🇺', '俄罗斯': '🇷🇺', '俄罗斯联邦': '🇷🇺',
            '瑞士': '🇨🇭', '德国': '🇩🇪', '法国': '🇫🇷',
            '英国': '🇬🇧', '荷兰': '🇳🇱',
            '韩国': '🇰🇷', '印度': '🇮🇳', '泰国': '🇹🇭',
            '越南': '🇻🇳', '菲律宾': '🇵🇭', '印尼': '🇮🇩', '印度尼西亚': '🇮🇩',
            '马来西亚': '🇲🇾', '巴西': '🇧🇷', '阿根廷': '🇦🇷',
            '墨西哥': '🇲🇽', '智利': '🇨🇱', '哥伦比亚': '🇨🇴',
            '西班牙': '🇪🇸', '意大利': '🇮🇹', '波兰': '🇵🇱',
            '土耳其': '🇹🇷', '以色列': '🇮🇱', '阿联酋': '🇦🇪',
            '南非': '🇿🇦', '埃及': '🇪🇬', '尼日利亚': '🇳🇬',
            '乌克兰': '🇺🇦', '罗马尼亚': '🇷🇴', '捷克': '🇨🇿',
            '希腊': '🇬🇷', '葡萄牙': '🇵🇹', '瑞典': '🇸🇪',
            '挪威': '🇳🇴', '丹麦': '🇩🇰', '芬兰': '🇫🇮',
            '奥地利': '🇦🇹', '比利时': '🇧🇪', '爱尔兰': '🇮🇪',
            '阿尔巴尼亚': '🇦🇱', '保加利亚': '🇧🇬', '塞尔维亚': '🇷🇸',
            '克罗地亚': '🇭🇷', '匈牙利': '🇭🇺', '斯洛伐克': '🇸🇰',
            '斯洛文尼亚': '🇸🇮', '立陶宛': '🇱🇹', '拉脱维亚': '🇱🇻',
            '爱沙尼亚': '🇪🇪', '乌拉圭': '🇺🇾', '巴拉圭': '🇵🇾',
            '新西兰': '🇳🇿', '巴基斯坦': '🇵🇰', '孟加拉国': '🇧🇩'
        }
        
        for p in proxies:
            # 生成代理名称
            if p.country and p.country.strip() and p.country.strip() != '未知':
                # 有国家信息：显示国旗+国家+IP
                country_name = p.country.strip()
                country_emoji = country_emoji_map.get(country_name, '🌍')
                proxy_name = f'{country_emoji} {country_name}_{p.ip}'
            else:
                # 没有国家信息：只显示IP+端口
                proxy_name = f'{p.ip}_{p.port}'
            
            if p.protocol in ['http', 'https']:
                proxy_node = {
                    'name': proxy_name,
                    'type': 'http',
                    'server': p.ip,
                    'port': p.port
                }
                if p.username and p.password:
                    proxy_node['username'] = p.username
                    proxy_node['password'] = p.password
                    
            elif p.protocol == 'socks5':
                proxy_node = {
                    'name': proxy_name,
                    'type': 'socks5',
                    'server': p.ip,
                    'port': p.port
                }
                if p.username and p.password:
                    proxy_node['username'] = p.username
                    proxy_node['password'] = p.password
            else:
                continue
            
            clash_config['proxies'].append(proxy_node)
            proxy_names.append(proxy_name)
        
        if not clash_config['proxies']:
            return Response('# 暂无支持的代理类型（需要 http/https/socks5）\nproxies: []\n', 
                          mimetype='text/yaml; charset=utf-8')
        
        # 添加代理组
        clash_config['proxy-groups'] = [
            {
                'name': '全局选择',
                'type': 'select',
                'proxies': ['延迟最低', '负载均衡', '失败切换'] + proxy_names[:50]  # 只显示前50个以避免太长
            },
            {
                'name': '延迟最低',
                'type': 'url-test',
                'proxies': proxy_names,
                'url': 'http://www.gstatic.com/generate_204',
                'interval': 300
            },
            {
                'name': '负载均衡',
                'type': 'load-balance',
                'proxies': proxy_names,
                'url': 'http://www.gstatic.com/generate_204',
                'interval': 300
            },
            {
                'name': '失败切换',
                'type': 'fallback',
                'proxies': proxy_names,
                'url': 'http://www.gstatic.com/generate_204',
                'interval': 300
            }
        ]
        
        # 添加基本规则
        clash_config['rules'] = [
            'DOMAIN-SUFFIX,local,DIRECT',
            'IP-CIDR,127.0.0.0/8,DIRECT',
            'IP-CIDR,192.168.0.0/16,DIRECT',
            'IP-CIDR,10.0.0.0/8,DIRECT',
            'IP-CIDR,172.16.0.0/12,DIRECT',
            'GEOIP,CN,DIRECT',
            'MATCH,全局选择'
        ]
        
        # 转换为 YAML 格式
        yaml_content = yaml.dump(clash_config, 
                                allow_unicode=True, 
                                default_flow_style=False,
                                sort_keys=False)
        
        # 添加注释头
        header = f"""# ProxyPool Clash 订阅配置
# 生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# 代理数量: {len(clash_config['proxies'])}
# 项目地址: https://github.com/huppugo1/ProxyPoolWithUI

"""
        
        print(f"[clash] 成功生成配置，包含 {len(clash_config['proxies'])} 个代理")
        return Response(header + yaml_content, mimetype='text/yaml; charset=utf-8')
        
    except Exception as e:
        import traceback
        error_msg = f'# 生成 Clash 配置失败: {str(e)}\n'
        print(f"[clash] 错误: {e}")
        print(traceback.format_exc())
        return Response(error_msg, mimetype='text/yaml; charset=utf-8', status=500)

# Clash 订阅接口 - 仅代理列表
@app.route('/clash/proxies', methods=['GET'])
def clash_proxies():
    """
    返回 Clash 代理节点列表（YAML 格式）
    支持参数：
    - c: 按国家筛选，多个国家用逗号分隔 (如: c=CN,US)
    - nc: 排除指定国家 (如: nc=CN)
    - protocol: 筛选协议类型（http/https/socks5）
    - limit: 限制代理数量，默认返回全部
    """
    try:
        # 获取查询参数
        countries = request.args.get('c', '').upper().split(',') if request.args.get('c') else None
        exclude_countries = request.args.get('nc', '').upper().split(',') if request.args.get('nc') else None
        protocol = request.args.get('protocol', None)
        limit = request.args.get('limit', -1, type=int)
        
        print(f"[clash/proxies] 请求参数: countries={countries}, exclude={exclude_countries}, protocol={protocol}, limit={limit}")
        
        # 从数据库获取代理
        if protocol:
            proxies = conn.get_by_protocol(protocol, limit)
        else:
            proxies = conn.getValidatedRandom(limit)
        
        # 按国家筛选
        if countries and countries != ['']:
            country_map = {
                'CN': '中国', 'HK': '香港', 'TW': '台湾',
                'US': '美国', 'CA': '加拿大',
                'JP': '日本', 'SG': '新加坡',
                'AU': '澳大利亚', 'RU': '俄罗斯',
                'CH': '瑞士', 'DE': '德国', 'FR': '法国',
                'GB': '英国', 'NL': '荷兰'
            }
            country_names = [country_map.get(c, c) for c in countries if c]
            proxies = [p for p in proxies if p.country in country_names]
            print(f"[clash/proxies] 国家筛选后: {len(proxies)} 个代理")
        
        # 排除指定国家
        if exclude_countries and exclude_countries != ['']:
            country_map = {
                'CN': '中国', 'HK': '香港', 'TW': '台湾',
                'US': '美国', 'CA': '加拿大',
                'JP': '日本', 'SG': '新加坡',
                'AU': '澳大利亚', 'RU': '俄罗斯',
                'CH': '瑞士', 'DE': '德国', 'FR': '法国',
                'GB': '英国', 'NL': '荷兰'
            }
            exclude_names = [country_map.get(c, c) for c in exclude_countries if c]
            proxies = [p for p in proxies if p.country not in exclude_names]
            print(f"[clash/proxies] 排除国家后: {len(proxies)} 个代理")
        
        if not proxies:
            return Response('# 暂无可用代理\nproxies: []\n', mimetype='text/yaml; charset=utf-8')
        
        # 构建代理列表
        proxy_list = []
        
        # 扩展的国家 emoji 映射表
        country_emoji_map = {
            '中国': '🇨🇳', '香港': '🇭🇰', '台湾': '🇹🇼',
            '美国': '🇺🇸', '加拿大': '🇨🇦',
            '日本': '🇯🇵', '新加坡': '🇸🇬',
            '澳大利亚': '🇦🇺', '俄罗斯': '🇷🇺', '俄罗斯联邦': '🇷🇺',
            '瑞士': '🇨🇭', '德国': '🇩🇪', '法国': '🇫🇷',
            '英国': '🇬🇧', '荷兰': '🇳🇱',
            '韩国': '🇰🇷', '印度': '🇮🇳', '泰国': '🇹🇭',
            '越南': '🇻🇳', '菲律宾': '🇵🇭', '印尼': '🇮🇩', '印度尼西亚': '🇮🇩',
            '马来西亚': '🇲🇾', '巴西': '🇧🇷', '阿根廷': '🇦🇷',
            '墨西哥': '🇲🇽', '智利': '🇨🇱', '哥伦比亚': '🇨🇴',
            '西班牙': '🇪🇸', '意大利': '🇮🇹', '波兰': '🇵🇱',
            '土耳其': '🇹🇷', '以色列': '🇮🇱', '阿联酋': '🇦🇪',
            '南非': '🇿🇦', '埃及': '🇪🇬', '尼日利亚': '🇳🇬',
            '乌克兰': '🇺🇦', '罗马尼亚': '🇷🇴', '捷克': '🇨🇿',
            '希腊': '🇬🇷', '葡萄牙': '🇵🇹', '瑞典': '🇸🇪',
            '挪威': '🇳🇴', '丹麦': '🇩🇰', '芬兰': '🇫🇮',
            '奥地利': '🇦🇹', '比利时': '🇧🇪', '爱尔兰': '🇮🇪',
            '阿尔巴尼亚': '🇦🇱', '保加利亚': '🇧🇬', '塞尔维亚': '🇷🇸',
            '克罗地亚': '🇭🇷', '匈牙利': '🇭🇺', '斯洛伐克': '🇸🇰',
            '斯洛文尼亚': '🇸🇮', '立陶宛': '🇱🇹', '拉脱维亚': '🇱🇻',
            '爱沙尼亚': '🇪🇪', '乌拉圭': '🇺🇾', '巴拉圭': '🇵🇾',
            '新西兰': '🇳🇿', '巴基斯坦': '🇵🇰', '孟加拉国': '🇧🇩'
        }
        
        for p in proxies:
            # 生成代理名称
            if p.country and p.country.strip() and p.country.strip() != '未知':
                # 有国家信息：显示国旗+国家+IP
                country_name = p.country.strip()
                country_emoji = country_emoji_map.get(country_name, '🌍')
                proxy_name = f'{country_emoji} {country_name}_{p.ip}'
            else:
                # 没有国家信息：只显示IP+端口
                proxy_name = f'{p.ip}_{p.port}'
            
            if p.protocol in ['http', 'https']:
                proxy_node = {
                    'name': proxy_name,
                    'type': 'http',
                    'server': p.ip,
                    'port': p.port
                }
                if p.username and p.password:
                    proxy_node['username'] = p.username
                    proxy_node['password'] = p.password
                    
            elif p.protocol == 'socks5':
                proxy_node = {
                    'name': proxy_name,
                    'type': 'socks5',
                    'server': p.ip,
                    'port': p.port
                }
                if p.username and p.password:
                    proxy_node['username'] = p.username
                    proxy_node['password'] = p.password
            else:
                continue
            
            proxy_list.append(proxy_node)
        
        if not proxy_list:
            return Response('# 暂无支持的代理类型（需要 http/https/socks5）\nproxies: []\n', 
                          mimetype='text/yaml; charset=utf-8')
        
        # 转换为 YAML 格式
        yaml_content = yaml.dump({'proxies': proxy_list}, 
                                allow_unicode=True, 
                                default_flow_style=False,
                                sort_keys=False)
        
        # 添加注释头
        header = f"""# ProxyPool Clash 代理列表
# 生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# 代理数量: {len(proxy_list)}

"""
        
        print(f"[clash/proxies] 成功生成代理列表，包含 {len(proxy_list)} 个代理")
        return Response(header + yaml_content, mimetype='text/yaml; charset=utf-8')
        
    except Exception as e:
        import traceback
        error_msg = f'# 生成 Clash 代理列表失败: {str(e)}\nproxies: []\n'
        print(f"[clash/proxies] 错误: {e}")
        print(traceback.format_exc())
        return Response(error_msg, mimetype='text/yaml; charset=utf-8', status=500)

############# Clash 订阅接口 end ################

############# 以下API主要给网页使用 ################

@app.route('/')
def index():
    return redirect('/web')

# 网页：首页
@app.route('/web', methods=['GET'])
@app.route('/web/', methods=['GET'])
def page_index():
    return send_from_directory(STATIC_FOLDER, 'index.html')

# 网页：爬取器状态
@app.route('/web/fetchers', methods=['GET'])
@app.route('/web/fetchers/', methods=['GET'])
def page_fetchers():
    return send_from_directory(STATIC_FOLDER, 'fetchers/index.html')

# 获取代理状态
@app.route('/proxies_status', methods=['GET'])
def proxies_status():
    try:
        # 添加超时保护和限制
        import time
        start_time = time.time()
        
        # 限制返回的代理数量，避免数据过大导致超时
        max_proxies = int(request.args.get('limit', 1000))  # 默认最多返回 1000 个
        
        print(f"[proxies_status] 开始查询，限制={max_proxies}")
        
        proxies = conn.getValidatedRandom(max_proxies)
        elapsed1 = time.time() - start_time
        print(f"[proxies_status] 查询代理完成: {len(proxies)} 个 ({elapsed1:.2f}秒)")
        
        proxies = sorted(proxies, key=lambda p: f'{p.protocol}://{p.ip}:{p.port}', reverse=True)
        proxies = [p.to_dict() for p in proxies]
        
        elapsed2 = time.time() - start_time
        print(f"[proxies_status] 数据转换完成 ({elapsed2:.2f}秒)")

        status = conn.getProxiesStatus()
        
        elapsed3 = time.time() - start_time
        print(f"[proxies_status] 状态统计完成 ({elapsed3:.2f}秒)")
        print(f"[proxies_status] 总耗时: {elapsed3:.2f}秒")

        return jsonify(dict(
            success=True,
            proxies=proxies,
            **status
        ))
    except Exception as e:
        import traceback
        print(f"[proxies_status] 错误: {e}")
        print(traceback.format_exc())
        return jsonify(dict(
            success=False,
            message=f'获取代理状态失败: {str(e)}',
            proxies=[],
            sum_proxies_cnt=0,
            validated_proxies_cnt=0,
            pending_proxies_cnt=0
        )), 500

# 获取爬取器状态
@app.route('/fetchers_status', methods=['GET'])
def fetchers_status():
    # 优化：一次性获取所有需要的数据，避免多次锁竞争
    fetchers = conn.getAllFetchers()
    fetchers = [f.to_dict() for f in fetchers]
    
    # 获取所有可用代理用于统计
    proxies = conn.getValidatedRandom(-1)
    
    # 统计每个fetcher的validated_cnt
    validated_cnt_map = {}
    for p in proxies:
        if p.fetcher_name not in validated_cnt_map:
            validated_cnt_map[p.fetcher_name] = 0
        validated_cnt_map[p.fetcher_name] += 1
    
    # 一次性获取所有fetcher的in_db_cnt
    in_db_cnt_map = conn.getProxyCountAll()
    
    for f in fetchers:
        f['validated_cnt'] = validated_cnt_map.get(f['name'], 0)
        f['in_db_cnt'] = in_db_cnt_map.get(f['name'], 0)
    
    return jsonify(dict(
        success=True,
        fetchers=fetchers
    ))

# 清空爬取器状态
@app.route('/clear_fetchers_status', methods=['GET'])
def clear_fetchers_status():
    conn.pushClearFetchersStatus()
    return jsonify(dict(success=True))

# 设置是否启用特定爬取器,?name=str,enable=0/1
@app.route('/fetcher_enable', methods=['GET'])
def fetcher_enable():
    name = request.args.get('name')
    enable = request.args.get('enable')
    if enable == '1':
        conn.pushFetcherEnable(name, True)
    else:
        conn.pushFetcherEnable(name, False)
    return jsonify(dict(success=True))

# 手动添加代理
@app.route('/add_proxy', methods=['POST'])
def add_proxy():
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['fetcher_name', 'protocol', 'ip', 'port']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify(dict(success=False, message=f'缺少必填字段: {field}')), 400
        
        fetcher_name = data['fetcher_name']
        protocol = data['protocol'].lower()
        ip = data['ip'].strip()
        
        # 验证端口
        try:
            port = int(data['port'])
            if port < 1 or port > 65535:
                return jsonify(dict(success=False, message='端口范围必须在 1-65535 之间')), 400
        except ValueError:
            return jsonify(dict(success=False, message='端口必须是数字')), 400
        
        # 验证协议
        valid_protocols = ['http', 'https', 'socks4', 'socks5']
        if protocol not in valid_protocols:
            return jsonify(dict(success=False, message=f'协议必须是以下之一: {", ".join(valid_protocols)}')), 400
        
        # 可选字段
        username = data.get('username', '').strip() or None
        password = data.get('password', '').strip() or None
        country = data.get('country', '').strip() or None
        address = data.get('address', '').strip() or None
        
        print(f"[手动添加代理] {protocol}://{ip}:{port} 来源={fetcher_name}")
        
        # 添加代理到数据库
        conn.pushNewFetch(
            fetcher_name=fetcher_name,
            protocol=protocol,
            ip=ip,
            port=port,
            username=username,
            password=password,
            country=country,
            address=address
        )
        
        print(f"[手动添加代理] 成功添加: {protocol}://{ip}:{port}")
        return jsonify(dict(success=True, message='代理添加成功，等待验证'))
    
    except sqlite3.IntegrityError as e:
        error_msg = '该代理已存在（相同协议、IP和端口）'
        print(f"[手动添加代理] 错误: {error_msg}")
        return jsonify(dict(success=False, message=error_msg)), 400
    
    except Exception as e:
        import traceback
        error_msg = str(e)
        print(f"[手动添加代理] 异常: {error_msg}")
        print(traceback.format_exc())
        return jsonify(dict(success=False, message=f'添加失败: {error_msg}')), 500

############# 其他 ################

# 跨域支持，主要是在开发网页端的时候需要使用
def after_request(resp):
    ALLOWED_ORIGIN = ['0.0.0.0', '127.0.0.1', 'localhost']
    origin = request.headers.get('origin', None)
    if origin is not None:
        for item in ALLOWED_ORIGIN:
            if item in origin:
                resp.headers['Access-Control-Allow-Origin'] = origin
                resp.headers['Access-Control-Allow-Credentials'] = 'true'
                resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
                resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
                resp.headers['Access-Control-Max-Age'] = '3600'
    return resp

# 处理 OPTIONS 预检请求
@app.before_request
def handle_preflight():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        ALLOWED_ORIGIN = ['0.0.0.0', '127.0.0.1', 'localhost']
        origin = request.headers.get('origin', None)
        if origin is not None:
            for item in ALLOWED_ORIGIN:
                if item in origin:
                    response.headers['Access-Control-Allow-Origin'] = origin
                    response.headers['Access-Control-Allow-Credentials'] = 'true'
                    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
                    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
                    response.headers['Access-Control-Max-Age'] = '3600'
                    break
        return response

app.after_request(after_request)

def main(proc_lock):
    if proc_lock is not None:
        conn.set_proc_lock(proc_lock)
    # 因为默认sqlite3中，同一个数据库连接不能在多线程环境下使用，所以这里需要禁用flask的多线程
    app.run(host='0.0.0.0', port=5000, threaded=False)

if __name__ == '__main__':
    main(None)
