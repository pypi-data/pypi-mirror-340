import pytest
from core.executor import TestExecutor
from lib import channellib
from lib import a2llib
import time

def test_1(executor:TestExecutor):
    executor.write_veristand(channellib.AO5,0)
    time.sleep(1)
    signal_value = executor.read_measurement(a2llib.gIoHwDrv_u16AdcValue_[12])
    pytest.assume(abs(signal_value - 15.0) <=100)
    
    executor.write_veristand(channellib.AO5,3)
    time.sleep(1)
    signal_value = executor.read_measurement(a2llib.gIoHwDrv_u16AdcValue_[12])
    pytest.assume(abs(signal_value - 2457.0) <=100)
    
    executor.write_veristand(channellib.AO5,5)
    time.sleep(1)
    signal_value = executor.read_measurement(a2llib.gIoHwDrv_u16AdcValue_[12])
    pytest.assume(abs(signal_value - 4094.9999999999995) <=100)
    
    executor.write_veristand(channellib.AO5,0)
    time.sleep(1)

    