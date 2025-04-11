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
        
    
    def test_demo3(self, executor: TestExecutor):
        executor.write_bus(buslib.PwrModSts_FZCU_can,buslib.PwrModSts_FZCU_can.ACC)
        time.sleep(1)
        signal_value = executor.read_bus(buslib.PwrModSts_FZCU_can, expected_value=buslib.PwrModSts_FZCU_can.ACC)
        # pytest.assume(signal_value==buslib.PwrModSts_FZCU_can.ACC)

        executor.write_bus(buslib.PwrModSts_FZCU_can,buslib.PwrModSts_FZCU_can.Awake)
        time.sleep(1)
        signal_value = executor.read_bus(buslib.PwrModSts_FZCU_can, expected_value=buslib.PwrModSts_FZCU_can.Awake)
        # pytest.assume(signal_value==buslib.PwrModSts_FZCU_can.Awake)
        


if __name__=='__main__':
    tester = TestClass()
    tester.test_DEMO()