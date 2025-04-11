"""
配置管理器 - 线程安全的单例模式
用于管理全局配置
创建时间：2024-12-24
作者：夏灿
"""
import os
import yaml
import threading
from pathlib import Path
from typing import Dict, Any, Optional

class _ConfigManager:
    """私有的配置管理器类"""
    _instance = None
    _lock = threading.Lock()
    _config_lock = threading.RLock()  # 使用RLock允许同一线程多次获取锁
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance
            
    def __init__(self):
        if not hasattr(self, '_initialized'):
            with self._lock:
                if not hasattr(self, '_initialized'):
                    self._config: Dict[str, Any] = {}
                    self._load_config()
                    self._initialized = True
        
    def _load_config(self):
        """加载配置文件"""
        with self._config_lock:
            try:
                root_dir = Path(__file__).resolve().parent
                config_path = root_dir / "conf.yaml"
                
                with open(config_path, 'r', encoding='utf-8') as f:
                    self._config = yaml.safe_load(f)
                    
            except Exception as e:
                print(f"加载配置文件失败: {str(e)}")
                self._config = {}
            
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项"""
        with self._config_lock:
            try:
                value = self._config
                for k in key.split('.'):
                    value = value[k]
                return value
            except (KeyError, TypeError):
                return default
            
    def set(self, key: str, value: Any) -> bool:
        """设置配置项"""
        with self._config_lock:
            try:
                keys = key.split('.')
                current = self._config
                
                for k in keys[:-1]:
                    if k not in current:
                        current[k] = {}
                    current = current[k]
                    
                current[keys[-1]] = value
                return True
                
            except Exception as e:
                print(f"设置配置项失败: {str(e)}")
                return False
    
    def delete(self, key: str) -> bool:
        """删除配置项"""
        with self._config_lock:
            try:
                keys = key.split('.')
                current = self._config
                for k in keys[:-1]:
                    current = current[k]
                del current[keys[-1]]
                return True
            except Exception as e:
                print(f"删除配置项失败: {str(e)}")
                return False
            
    def save(self) -> bool:
        """保存配置到文件"""
        with self._config_lock:
            try:
                root_dir = Path(__file__).resolve().parent
                config_path = root_dir / "conf.yaml"
                
                with open(config_path, 'w', encoding='utf-8') as f:
                    yaml.safe_dump(self._config, f, allow_unicode=True, sort_keys=False)
                return True
                
            except Exception as e:
                print(f"保存配置文件失败: {str(e)}")
                return False
            
    def reload(self) -> bool:
        """重新加载配置文件"""
        with self._config_lock:
            try:
                self._load_config()
                return True
            except Exception as e:
                print(f"重新加载配置失败: {str(e)}")
                return False
            
    @property
    def config(self) -> Dict[str, Any]:
        """获取完整配置"""
        with self._config_lock:
            return self._config.copy()

# 创建全局配置管理器实例
config = _ConfigManager()

if __name__ == "__main__":
    # 测试读写配置
    config.set('test.key', 'test_value')
    print(config.get('test.key'))
    config.save()
    config.reload()
    print(config.get('test.key'))

    # 测试多线程
    def test_thread(thread_id):
        print(f"Thread {thread_id}: {config.get('test.key')}")
        config.set(f'test.thread_{thread_id}', f'test_value_{thread_id}')

    threads = [threading.Thread(target=test_thread, args=(i,)) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # 删除测试数据
    config.delete('test.key')
    config.save()
    config.reload()
    print(config.get('test.key'))

    # 测试删除配置项
    for i in range(10):
        config.delete(f'test.thread_{i}')
    config.save()
    config.reload()
    print(config.get('test.thread_0'))

    # 验证删除的配置项是否存在
    for i in range(10):
        assert config.get(f'test.thread_{i}') is None
    print("测试完成")
