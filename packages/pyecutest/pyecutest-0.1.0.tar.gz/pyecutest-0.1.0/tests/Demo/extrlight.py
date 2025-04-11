import pytest
import time
from core.executor import TestExecutor
from logging import getLogger
from lib import buslib
from lib import mappinglib_VCCD
from lib import a2llib

class TestClass:
    def setup_class(self):
        print("准备测试环境")
        self.executor = TestExecutor()
        
    def teardown_class(self):
        print("\n清理测试环境")
        
    def test_demo(self):
        """
        测试用例模板
        """
        self.executor.write_bus(buslib.RlsLiSwtReqLin_RZCU_LIN2_RLS_lin,1)
        time.sleep(0.5)
        pytest.assume(self.executor.read_bus(buslib.StsOfLedLoBeamLe_HCML_can) == 1)
        pytest.assume(self.executor.read_bus(buslib.StsOfLedLoBeamRi_HCMR_can) == 1)


        assert True  # 使用pytest进行简单的断言

if __name__=='__main__':
    tester = TestClass()
    tester.test_dome()
