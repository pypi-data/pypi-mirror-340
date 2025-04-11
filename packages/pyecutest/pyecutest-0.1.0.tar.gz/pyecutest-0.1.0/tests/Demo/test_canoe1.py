import pytest
from lib import buslib
from lib import a2llib
from core.executor import TestExecutor
import time


class TestClass:
    def setup_class(self):
        print("准备测试环境")

        # self.executor = TestExecutor()
        
        
        
    def teardown_class(self):
        print("\n清理测试环境")
        # self.INCA.CloseExperiment()
        # self.CANOE.stop_measurement()
        # self.VERISTAND.disconnect()
        

    def test_demo1(self, executor: TestExecutor):

        sys_variable = executor.read_sys_var('IL::Klemme15', expected_value=1)
        
        # pytest.assume(sys_variable==1)
 
    def test_demo2(self, executor: TestExecutor):
        executor.write_sys_var('IL::Klemme30',1)#写环境变量
        sys_variable = executor.read_sys_var('IL::Klemme30', expected_value=1) #读环境变量

        # pytest.assume(sys_variable==1)


if __name__=='__main__':
    tester = TestClass()
    tester.test_DEMO()