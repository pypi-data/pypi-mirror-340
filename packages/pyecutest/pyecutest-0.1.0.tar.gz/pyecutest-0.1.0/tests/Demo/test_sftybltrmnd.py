import pytest,time
from core.executor import TestExecutor
from lib import buslib
from lib import a2llib
from lib import channel_lib



class TestClass:
    def setup_class(self):
        print("准备测试环境")
        self.excutor = TestExecutor()
        
    def teardown_class(self):
        print("\n清理测试环境")
        

    def test_demo1(self):
        # 设置占座
        self.excutor.write_bus(buslib.DrvrOcupcySts,1)
        time.sleep(1)   
        # 重置车速
        self.excutor.write_bus(buslib.VehSpd,0)
        self.excutor.write_bus(buslib.VehSpdVld,1)
        time.sleep(1)
        # 设置Powermode==ACC/ACC 
        self.excutor.write_bus(buslib.PwrModSts,2)

        # 四门全关
        # self.excutor.write_bus(buslib.DoorDrvrSts_ZCUCANFD,1)
        # self.excutor.

        # 设置SSB==ON
        self.excutor.write_bus(buslib.DrvActvSts, 1)

        # 解开安全带
        self.excutor.write_bus(buslib.DrvrBucSts,1)
        time.sleep(1)
        
        # 期望结果
        pytest.assume(self.excutor.read_measurement(a2llib.SftyBltRmnd_DrvrSeatBltRmnd_out_M)
                      ==a2llib.SftyBltRmnd_CalDrvrSeatBltRmndBPVal_C.Enum_FSeatBltRmnd_Level1reminder)

 

        

            


        



        



        

        

        
    