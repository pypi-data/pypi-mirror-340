from lib.a2llib import *
from core.executor import TestExecutor
import time

def pwrmod(executor:TestExecutor,val:str):
    executor.write_calibration(PwrModMgrSafe_CalPwrModStsByPassVal_C,val)
    executor.write_calibration(PwrModMgrSafe_CalPwrModStsByPass_C,1)
    executor.write_calibration(PwrModMgrSafe_CalPwrModVldByPassVal_C,PwrModMgrSafe_CalPwrModVldByPassVal_C.Enum_PwrModVld_Valid)
    executor.write_calibration(PwrModMgrSafe_CalPwrModVldByPass_C,1)
    time.sleep(0.5)