# encoding: utf-8

"""
封装的数据库接口
"""

from config import DATABASE_PATH
from .Proxy import Proxy
from .Fetcher import Fetcher
import sqlite3
import datetime
import threading
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.ip_location import get_ip_location_cached

conn = sqlite3.connect(
    DATABASE_PATH, 
    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
    timeout=30.0,  # 增加數據庫連接超時時間到 30 秒
    check_same_thread=False  # 允許多線程訪問（配合鎖使用）
)
# 设置 WAL 模式，提高并发性能
conn.execute('PRAGMA journal_mode=WAL')
conn.execute('PRAGMA synchronous=NORMAL')  # 平衡性能和安全性
# 线程锁
conn_lock = threading.Lock()
# 进程锁
proc_lock = None

def set_proc_lock(proc_lock_sub):
    """
    设置进程锁
    proc_lock_sub : main中的进程锁
    """
    global proc_lock
    proc_lock = proc_lock_sub

def _acquire_locks():
    """
    获取所有必要的锁（线程锁和进程锁）
    """
    conn_lock.acquire()
    if proc_lock is not None:
        proc_lock.acquire()

def _release_locks():
    """
    释放所有锁
    """
    if proc_lock is not None:
        proc_lock.release()
    conn_lock.release()

def pushNewFetch(fetcher_name, protocol, ip, port, username=None, password=None, country=None, address=None):
    """
    爬取器新抓到了一个代理，调用本函数将代理放入数据库
    fetcher_name : 爬取器名称
    protocol : 代理协议
    ip : 代理IP地址
    port : 代理端口
    username : 代理账号（可选，爬取器爬到的）
    password : 代理密码（可选，爬取器爬到的）
    country : 国家（可选，爬取器爬到的）
    address : 地址（可选，爬取器爬到的）
    
    注意：如果爬取器提供了 country/address/username/password，直接写入
          如果没有提供，保持为 None，等验证成功后再获取
    """
    p = Proxy()
    p.fetcher_name = fetcher_name
    p.protocol = protocol
    p.ip = ip
    p.port = port
    p.username = username  # 由爬取器提供，可能为 None
    p.password = password  # 由爬取器提供，可能为 None
    p.country = country    # 由爬取器提供，可能为 None
    p.address = address    # 由爬取器提供，可能为 None
    
    _acquire_locks()
    
    try:
        c = conn.cursor()
        c.execute('BEGIN EXCLUSIVE TRANSACTION;')
        # 更新proxies表 - 避免重复添加
        c.execute('SELECT * FROM proxies WHERE protocol=? AND ip=? AND port=?', (p.protocol, p.ip, p.port))
        row = c.fetchone()
        if row is not None: # 已经存在(protocol, ip, port) - 不重复添加，只更新部分字段
            old_p = Proxy.decode(row)
            # 更新 fetcher_name, to_validate_date，如果爬取器提供了其他信息也一并更新
            update_fields = []
            update_values = []
            
            update_fields.append('fetcher_name=?')
            update_values.append(p.fetcher_name)
            
            update_fields.append('to_validate_date=?')
            update_values.append(min(datetime.datetime.now(), old_p.to_validate_date))
            
            # 如果提供了账号密码，更新
            if username is not None:
                update_fields.append('username=?')
                update_values.append(username)
            if password is not None:
                update_fields.append('password=?')
                update_values.append(password)
            
            # 如果提供了地理位置，更新
            if country is not None:
                update_fields.append('country=?')
                update_values.append(country)
            if address is not None:
                update_fields.append('address=?')
                update_values.append(address)
            
            update_values.extend([p.protocol, p.ip, p.port])
            
            sql = f"UPDATE proxies SET {','.join(update_fields)} WHERE protocol=? AND ip=? AND port=?"
            c.execute(sql, tuple(update_values))
        else:
            # 新代理，插入所有字段
            c.execute('INSERT INTO proxies VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', p.params())
        c.close()
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        _release_locks()

def getToValidate(max_count=1):
    """
    从数据库中获取待验证的代理，根据to_validate_date字段
    优先选取已经通过了验证的代理，其次是没有通过验证的代理
    max_count : 返回数量限制
    返回 : list[Proxy]
    """
    _acquire_locks()
    c = conn.cursor()
    c.execute('BEGIN EXCLUSIVE TRANSACTION;')
    c.execute('SELECT * FROM proxies WHERE to_validate_date<=? AND validated=? ORDER BY to_validate_date LIMIT ?', (
        datetime.datetime.now(),
        True,
        max_count
    ))
    proxies = [Proxy.decode(row) for row in c]
    c.execute('SELECT * FROM proxies WHERE to_validate_date<=? AND validated=? ORDER BY to_validate_date LIMIT ?', (
        datetime.datetime.now(),
        False,
        max_count - len(proxies)
    ))
    proxies = proxies + [Proxy.decode(row) for row in c]
    c.close()
    conn.commit()
    _release_locks()
    return proxies

def pushValidateResult(proxy, success, latency):
    """
    将验证器的一个结果添加进数据库中
    proxy : 代理
    success : True/False，验证是否成功
    latency : 本次验证所用的时间(单位毫秒)
    
    注意：IP可用（验证成功）且没有国家和地址信息时，会自动获取并更新
    """
    p = proxy
    should_remove = p.validate(success, latency)
    
    # 只有在验证成功（IP可用）且缺少地理位置信息时才获取
    need_update_location = False
    if success and not should_remove and (p.country is None or p.address is None):
        try:
            location = get_ip_location_cached(p.ip)
            p.country = location.get('country', '未知')
            p.address = location.get('address', '无法获取')
            need_update_location = True
            print(f"获取IP地理位置成功: {p.ip} -> {p.country}, {p.address}")
        except Exception as e:
            print(f"获取IP地理位置失败 {p.ip}: {e}")
            # 获取失败时不设置默认值，保持 None
    
    _acquire_locks()
    if should_remove:
        conn.execute('DELETE FROM proxies WHERE protocol=? AND ip=? AND port=?', (p.protocol, p.ip, p.port))
    else:
        # 如果需要更新地理位置信息，则包含 country 和 address
        if need_update_location:
            conn.execute("""
                UPDATE proxies
                SET fetcher_name=?,validated=?,latency=?,validate_date=?,to_validate_date=?,validate_failed_cnt=?,country=?,address=?
                WHERE protocol=? AND ip=? AND port=?
            """, (
                p.fetcher_name, p.validated, p.latency, p.validate_date, p.to_validate_date, p.validate_failed_cnt,
                p.country, p.address,
                p.protocol, p.ip, p.port
            ))
        else:
            # 不更新地理位置信息
            conn.execute("""
                UPDATE proxies
                SET fetcher_name=?,validated=?,latency=?,validate_date=?,to_validate_date=?,validate_failed_cnt=?
                WHERE protocol=? AND ip=? AND port=?
            """, (
                p.fetcher_name, p.validated, p.latency, p.validate_date, p.to_validate_date, p.validate_failed_cnt,
                p.protocol, p.ip, p.port
            ))
    conn.commit()
    _release_locks()

def getValidatedRandom(max_count):
    """
    从通过了验证的代理中，随机选择max_count个代理返回
    max_count<=0表示不做数量限制
    返回 : list[Proxy]
    """
    _acquire_locks()
    if max_count > 0:
        r = conn.execute('SELECT * FROM proxies WHERE validated=? ORDER BY RANDOM() LIMIT ?', (True, max_count))
    else:
        r = conn.execute('SELECT * FROM proxies WHERE validated=? ORDER BY RANDOM()', (True,))
    proxies = [Proxy.decode(row) for row in r]
    r.close()
    _release_locks()
    return proxies
    
    #新增方法
def get_by_protocol(protocol, max_count):
    """
    查询 protocol 字段为指定值的代理服务器记录
    max_count 表示返回记录的最大数量，如果为 0 或负数则返回所有记录
    返回 : list[Proxy]
    """
    _acquire_locks()
    if max_count > 0:
        r = conn.execute('SELECT * FROM proxies WHERE protocol=? AND validated=? ORDER BY RANDOM() LIMIT ?', (protocol, True, max_count))
    else:
        r = conn.execute('SELECT * FROM proxies WHERE protocol=? AND validated=? ORDER BY RANDOM()', (protocol, True))
    proxies = [Proxy.decode(row) for row in r]
    r.close()
    _release_locks()
    return proxies

def pushFetcherResult(name, proxies_cnt):
    """
    更新爬取器的状态，每次在完成一个网站的爬取之后，调用本函数
    name : 爬取器的名称
    proxies_cnt : 本次爬取到的代理数量
    """
    _acquire_locks()
    c = conn.cursor()
    c.execute('BEGIN EXCLUSIVE TRANSACTION;')
    c.execute('SELECT * FROM fetchers WHERE name=?', (name,))
    row = c.fetchone()
    if row is None:
        raise ValueError(f'ERRROR: can not find fetcher {name}')
    else:
        f = Fetcher.decode(row)
        f.last_proxies_cnt = proxies_cnt
        f.sum_proxies_cnt = f.sum_proxies_cnt + proxies_cnt
        f.last_fetch_date = datetime.datetime.now()
        c.execute('UPDATE fetchers SET sum_proxies_cnt=?,last_proxies_cnt=?,last_fetch_date=? WHERE name=?', (
            f.sum_proxies_cnt, f.last_proxies_cnt, f.last_fetch_date, f.name
        ))
    c.close()
    conn.commit()
    _release_locks()

def pushFetcherEnable(name, enable):
    """
    设置是否起用对应爬取器，被禁用的爬取器将不会被运行
    name : 爬取器的名称
    enable : True/False, 是否启用
    """
    _acquire_locks()
    c = conn.cursor()
    c.execute('BEGIN EXCLUSIVE TRANSACTION;')
    c.execute('SELECT * FROM fetchers WHERE name=?', (name,))
    row = c.fetchone()
    if row is None:
        raise ValueError(f'ERRROR: can not find fetcher {name}')
    else:
        f = Fetcher.decode(row)
        f.enable = enable
        c.execute('UPDATE fetchers SET enable=? WHERE name=?', (
            f.enable, f.name
        ))
    c.close()
    conn.commit()
    _release_locks()

def getAllFetchers():
    """
    获取所有的爬取器以及状态
    返回 : list[Fetcher]
    """
    _acquire_locks()
    r = conn.execute('SELECT * FROM fetchers')
    fetchers = [Fetcher.decode(row) for row in r]
    r.close()
    _release_locks()
    return fetchers

def getFetcher(name):
    """
    获取指定爬取器以及状态
    返回 : Fetcher
    """
    _acquire_locks()
    r = conn.execute('SELECT * FROM fetchers WHERE name=?', (name,))
    row = r.fetchone()
    r.close()
    _release_locks()
    if row is None:
        return None
    else:
        return Fetcher.decode(row)

def getProxyCount(fetcher_name):
    """
    查询在数据库中有多少个由指定爬取器爬取到的代理
    fetcher_name : 爬取器名称
    返回 : int
    """
    _acquire_locks()
    r = conn.execute('SELECT count(*) FROM proxies WHERE fetcher_name=?', (fetcher_name,))
    cnt = r.fetchone()[0]
    r.close()
    _release_locks()
    return cnt

def getProxyCountAll():
    """
    一次性查询所有爬取器在数据库中的代理数量
    返回 : dict {fetcher_name: count}
    """
    _acquire_locks()
    r = conn.execute('SELECT fetcher_name, count(*) FROM proxies GROUP BY fetcher_name')
    result = {row[0]: row[1] for row in r}
    r.close()
    _release_locks()
    return result

def getProxiesStatus():
    """
    获取代理状态，包括`全部代理数量`，`当前可用代理数量`，`等待验证代理数量`
    返回 : dict
    """
    _acquire_locks()
    r = conn.execute('SELECT count(*) FROM proxies')
    sum_proxies_cnt = r.fetchone()[0]
    r.close()

    r = conn.execute('SELECT count(*) FROM proxies WHERE validated=?', (True,))
    validated_proxies_cnt = r.fetchone()[0]
    r.close()

    r = conn.execute('SELECT count(*) FROM proxies WHERE to_validate_date<=?', (datetime.datetime.now(),))
    pending_proxies_cnt = r.fetchone()[0]
    r.close()
    _release_locks()
    return dict(
        sum_proxies_cnt=sum_proxies_cnt,
        validated_proxies_cnt=validated_proxies_cnt,
        pending_proxies_cnt=pending_proxies_cnt
    )

def pushClearFetchersStatus():
    """
    清空爬取器的统计信息，包括sum_proxies_cnt,last_proxies_cnt,last_fetch_date
    """
    _acquire_locks()
    c = conn.cursor()
    c.execute('BEGIN EXCLUSIVE TRANSACTION;')
    c.execute('UPDATE fetchers SET sum_proxies_cnt=?, last_proxies_cnt=?, last_fetch_date=?', (0, 0, None))
    c.close()
    conn.commit()
    _release_locks()
