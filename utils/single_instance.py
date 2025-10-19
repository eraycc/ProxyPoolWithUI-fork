# encoding: utf-8

"""
单实例运行管理器
确保系统只能运行一个实例，防止多个实例同时运行导致的数据冲突
"""

import os
import sys
import time
import signal
import socket
import psutil
import subprocess
import platform
from pathlib import Path

class SingleInstanceManager:
    """单实例管理器"""
    
    def __init__(self, app_name="ProxyPoolWithUI", port=5000):
        self.app_name = app_name
        self.port = port
        self.is_windows = platform.system().lower() == 'windows'
        
        # 跨平台文件路径
        if self.is_windows:
            # Windows: 使用用户目录
            self.pid_file = Path.home() / f".{app_name.lower()}.pid"
            self.lock_file = Path.home() / f".{app_name.lower()}.lock"
        else:
            # Linux/Unix: 使用 /tmp 目录
            self.pid_file = Path("/tmp") / f"{app_name.lower()}.pid"
            self.lock_file = Path("/tmp") / f"{app_name.lower()}.lock"
        
        # 打印系统信息（调试用）
        print(f"系统平台: {platform.system()} {platform.release()}")
        print(f"PID文件路径: {self.pid_file}")
        print(f"锁文件路径: {self.lock_file}")
        
    def is_port_in_use(self):
        """检查端口是否被占用"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex(('localhost', self.port))
                return result == 0
        except Exception:
            return False
    
    def get_process_by_port(self):
        """根据端口获取占用进程的PID"""
        try:
            for conn in psutil.net_connections():
                if conn.laddr.port == self.port and conn.status == 'LISTEN':
                    try:
                        process = psutil.Process(conn.pid)
                        # 检查进程名是否包含我们的应用名
                        if self.app_name.lower() in process.name().lower() or 'python' in process.name().lower():
                            return conn.pid
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
        except Exception:
            pass
        return None
    
    def is_process_running(self, pid):
        """检查指定PID的进程是否正在运行"""
        try:
            process = psutil.Process(pid)
            return process.is_running()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False
    
    def check_existing_instance(self):
        """检查是否已有实例在运行"""
        # 方法1: 检查端口占用
        if self.is_port_in_use():
            port_pid = self.get_process_by_port()
            if port_pid:
                print(f"检测到端口 {self.port} 已被进程 PID {port_pid} 占用")
                return port_pid
        
        # 方法2: 检查PID文件
        if self.pid_file.exists():
            try:
                with open(self.pid_file, 'r') as f:
                    pid = int(f.read().strip())
                
                if self.is_process_running(pid):
                    print(f"检测到已有实例正在运行 (PID: {pid})")
                    return pid
                else:
                    # PID文件存在但进程不存在，清理PID文件
                    print(f"清理无效的PID文件 (PID: {pid})")
                    self.pid_file.unlink()
            except (ValueError, FileNotFoundError):
                # PID文件损坏或不存在，清理
                self.pid_file.unlink()
        
        # 方法3: 检查锁文件
        if self.lock_file.exists():
            try:
                with open(self.lock_file, 'r') as f:
                    lock_data = f.read().strip().split('\n')
                    if len(lock_data) >= 2:
                        pid = int(lock_data[0])
                        lock_time = float(lock_data[1])
                        
                        # 检查锁文件是否过期（超过5分钟认为过期）
                        if time.time() - lock_time > 300:
                            print(f"清理过期的锁文件 (PID: {pid})")
                            self.lock_file.unlink()
                        elif self.is_process_running(pid):
                            print(f"检测到锁文件，实例可能正在运行 (PID: {pid})")
                            return pid
                        else:
                            print(f"清理无效的锁文件 (PID: {pid})")
                            self.lock_file.unlink()
            except (ValueError, FileNotFoundError, PermissionError):
                # 锁文件损坏、不存在或权限不足，尝试清理
                try:
                    self.lock_file.unlink()
                except:
                    pass
        
        return None
    
    def create_lock_files(self):
        """创建锁文件"""
        current_pid = os.getpid()
        current_time = time.time()
        
        # 创建PID文件
        with open(self.pid_file, 'w') as f:
            f.write(str(current_pid))
        
        # 创建锁文件（包含PID和时间戳）
        with open(self.lock_file, 'w') as f:
            f.write(f"{current_pid}\n{current_time}")
        
        print(f"创建锁文件成功 (PID: {current_pid})")
        return current_pid
    
    def force_cleanup_processes(self):
        """强制清理Python进程和锁文件"""
        print("开始强制清理进程和锁文件...")
        
        try:
            # 1. 终止Python进程（跨平台）
            print("正在终止Python进程...")
            if self.is_windows:
                # Windows: 使用 taskkill
                result = subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                                      capture_output=True, text=True, shell=True)
            else:
                # Linux/Unix: 使用 pkill
                result = subprocess.run(['pkill', '-f', 'python.*main.py'], 
                                      capture_output=True, text=True)
            
            if result.returncode == 0:
                print("Python进程清理成功")
            else:
                print(f"Python进程清理结果: {result.stderr}")
        except Exception as e:
            print(f"清理Python进程失败: {e}")
        
        try:
            # 2. 删除锁文件
            print("正在删除锁文件...")
            if self.lock_file.exists():
                self.lock_file.unlink()
                print("锁文件删除成功")
            else:
                print("锁文件不存在")
        except Exception as e:
            print(f"删除锁文件失败: {e}")
        
        try:
            # 3. 删除PID文件
            if self.pid_file.exists():
                self.pid_file.unlink()
                print("PID文件删除成功")
        except Exception as e:
            print(f"删除PID文件失败: {e}")
        
        # 4. 等待一下让进程完全终止
        print("等待进程完全终止...")
        time.sleep(2)
        
        # 5. 再次检查端口是否释放
        if not self.is_port_in_use():
            print("端口已释放，清理完成")
            return True
        else:
            print("端口仍被占用，清理可能不完整")
            return False

    def cleanup_lock_files(self):
        """清理锁文件"""
        try:
            if self.pid_file.exists():
                self.pid_file.unlink()
                print("清理PID文件成功")
        except Exception as e:
            print(f"清理PID文件失败: {e}")
        
        try:
            if self.lock_file.exists():
                self.lock_file.unlink()
                print("清理锁文件成功")
        except Exception as e:
            print(f"清理锁文件失败: {e}")
    
    def signal_handler(self, signum, frame):
        """信号处理器，用于优雅退出"""
        print(f"\n收到信号 {signum}，正在优雅退出...")
        self.cleanup_lock_files()
        sys.exit(0)
    
    def acquire_lock(self):
        """获取单实例锁"""
        print(f"检查是否已有实例运行...")
        
        existing_pid = self.check_existing_instance()
        if existing_pid:
            print(f"检测到已有实例正在运行 (PID: {existing_pid})")
            print("=" * 60)
            print("请手动执行以下清理命令：")
            print("=" * 60)
            
            if self.is_windows:
                print("Windows 清理命令：")
                print(f"  taskkill /f /im python.exe")
                print(f"  del \"{self.pid_file}\"")
                print(f"  del \"{self.lock_file}\"")
            else:
                print("Linux/Unix 清理命令：")
                print(f"  pkill -f python.*main.py")
                print(f"  rm -f \"{self.pid_file}\"")
                print(f"  rm -f \"{self.lock_file}\"")
            
            print("=" * 60)
            print("或者直接终止进程：")
            print(f"  kill {existing_pid}")
            print("=" * 60)
            return False
        
        # 创建锁文件
        current_pid = self.create_lock_files()
        
        # 注册信号处理器
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        print(f"单实例锁获取成功，当前PID: {current_pid}")
        return True
    
    def release_lock(self):
        """释放单实例锁"""
        self.cleanup_lock_files()
        print("单实例锁已释放")

def check_single_instance(app_name="ProxyPoolWithUI", port=5000):
    """
    检查单实例的便捷函数
    返回 SingleInstanceManager 实例，如果获取锁失败则返回 None
    """
    manager = SingleInstanceManager(app_name, port)
    if manager.acquire_lock():
        return manager
    return None

if __name__ == "__main__":
    # 测试单实例管理器
    print("测试单实例管理器...")
    
    manager = check_single_instance()
    if manager:
        print("单实例测试成功")
        print("按 Ctrl+C 退出...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            manager.release_lock()
    else:
        print("单实例测试失败")