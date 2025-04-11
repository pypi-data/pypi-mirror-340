import pytest

from interfaces.socketio.client import SocketClient
import yaml
from lib import buslib
from lib import mappinglib_VCCD
from lib import a2llib
import json
import time


class TestClass:
    def setup_class(self):
        print("准备测试环境")
        self.client = SocketClient(host='localhost', port=8080)
        self.client.connect()
        
    def teardown_class(self):
        print("\n清理测试环境")
        if self.client:
            time.sleep(0.5)  # 等待数据处理完成
            self.client.disconnect()

