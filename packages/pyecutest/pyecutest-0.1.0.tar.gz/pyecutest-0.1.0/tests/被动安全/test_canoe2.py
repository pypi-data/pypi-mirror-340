import pytest
from interfaces.canoe.canoe import Canoe
from interfaces.inca.inca import Inca, IncaWrapper
from interfaces.veristand.veristand import VeriStand
import yaml
from lib import buslib
from lib import mappinglib_VCCD
from lib import a2llib
from core.executor import TestExecutor



import time


class TestClass:
    def setup_class(self):
        print("准备测试环境")

        self.canoe = Canoe()
        # self.CANOE.open(config['canoe']['project_file'])
        # self.CANOE.start_measurement()
        
        self.executor = TestExecutor()

        
        
    def teardown_class(self):
        print("\n清理测试环境")
        # self.INCA.CloseExperiment()
        # self.CANOE.stop_measurement()
        # self.VERISTAND.disconnect()
        

    def test_DEMO2(self):
        
        self.canoe.set_signal_value('CAN',1,'BCP_ZCUCANFD_0x150','ABAActv',1)
        
        signal_value = self.CANOE.get_signal_value('CAN',1,'BCP_ZCUCANFD_0x150','ABAActv')
        assert signal_value==1
        
        self.executor.write_bus(buslib.ABAActv, 1)
        
        self.executor.write_calibration(a2llib.DigKeyWPC_CalPwrModStsBPVal, a2llib.DigKeyWPC_CalPwrModStsBPVal.Enum_PwrModSts_OFF)
        



if __name__=='__main__':
    tester = TestClass()
    tester.test_DEMO()

        

            


        



        



        

        

        
    