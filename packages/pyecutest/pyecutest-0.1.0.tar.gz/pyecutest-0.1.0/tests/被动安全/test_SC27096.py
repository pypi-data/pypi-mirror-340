import pytest
from core.executor import TestExecutor
import time
from lib import a2llib, buslib

class TestClass:
    def setup_class(self):
        print("准备测试环境")
        self.executor = TestExecutor()
        
    def teardown_class(self):
        print("\n清理测试环境") 
        self.executor.close()

    def test_drvr_1st_alarm(self):
        '''
        主驾1级告警测试用例
        
        前置条件:
        1. 主驾驶座椅有人就坐
        2. 四门关闭
        3. 电源模式从OFF切换到ACC/RUN
        4. SSB开关打开
        5. 主驾驶安全带未系
        
        期望结果:
        1. 主驾驶安全带提醒信号为一级提醒(DrvrSeatBltRmnd=1)
        '''
        print("写标定，主驾有人就坐")
        self.executor.write_calibration(a2llib.SftyBltRmnd_CalDrvrOcupcyStsBPVal_C.Enum_OcupcySts_Occupied)
        time.sleep(0.5)
        
        print("写标定，四门关闭")
        self.executor.write_calibration(a2llib.SftyBltRmnd_CalDoorDrvrStsBPVal_C.Enum_DoorSts_Clsd)
        self.executor.write_calibration(a2llib.SftyBltRmnd_CalDoorPassStsBPVal_C.Enum_DoorSts_Clsd)
        self.executor.write_calibration(a2llib.SftyBltRmnd_CalDoorLeReStsBPVal_C.Enum_DoorSts_Clsd)
        self.executor.write_calibration(a2llib.SftyBltRmnd_CalDoorRiReStsBPVal_C.Enum_DoorSts_Clsd)
        time.sleep(0.5)

        print("写标定，设置powermode == OFF")
        self.executor.write_calibration(a2llib.PwrModMgrSafe_CalPwrModStsByPassVal_C.Enum_PwrModSts_OFF)
        self.executor.write_calibration(a2llib.DigKey_CalPwrModStsVal_C.Enum_PwrModSts_OFF)
        time.sleep(0.5)
        
        print("写标定，设置powermode == ACC")
        self.executor.write_calibration(a2llib.PwrModMgrSafe_CalPwrModStsByPassVal_C.Enum_PwrModSts_ACC)
        time.sleep(0.5)
        
        print("写标定，设置SSB开关打开")
        self.executor.write_calibration(a2llib.SftyBltRmnd_CalDrvActvStsBPVal_C.Enum_DrvActvSts_ON)
        time.sleep(0.5)
        
        print("写标定，主驾安全带未系")
        self.executor.write_calibration(a2llib.SftyBltRmnd_CalDrvrBucStsBPVal_C.Enum_BucSts_UnBuc)
        time.sleep(0.5)
        
        print("检查主驾安全带提醒信号为一级提醒")
        assert self.executor.read_measurement("DrvrSeatBltRmnd") == 1
