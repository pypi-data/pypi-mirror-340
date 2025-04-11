import pytest,time
from lib import channellib,buslib,a2llib
from core import executor
from logging import getLogger


class TestAllDoors():
    def setup_class(self):
        self.executor = executor.TestExecutor()
        self.logger = getLogger(__name__)

    def teardown_class(self):
        pass

    def test_all_doors(self):
        '''
        四门三盖关闭
        '''
        # 主驾门全关
        self.executor.write_veristand(channellib.PWMOUT7_DO7,0)
        self.logger.info("")
        self.executor.read_bus()


