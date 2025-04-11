from cases.common.Pwrmod import pwrmod
from cases.common.screen.Settings import Light
from cases.common.Steercontrol import steercontrol
from lib.a2llib import *
from lib.buslib import *
import time
import pytest


def test_high_beam_switch_ACC(executor):

    # 电源模式ACC
    pwrmod()
    time.sleep(0.5)

    #屏幕点击打开近光灯
    Light.exterior_light_switch('近光灯')
    time.sleep(0.5)

    #check近光灯状态
    lelobeamsts=executor.read_bus(StsOfLedLoBeamLe_HCML_can)
    rilobeamsts=executor.read_bus(StsOfLedLoBeamRi_HCMR_can)
    lowbeamindcrsts = executor.read_bus(LoBeamIndcr_FZCU_can)
    pytest.assume(lelobeamsts==1)
    pytest.assume(rilobeamsts==1)
    pytest.assume(lowbeamindcrsts==1)
    time.sleep(0.5)

    #屏幕点击关闭近光灯
    Light.exterior_light_switch('关闭')
    time.sleep(0.5)

    #check近光灯状态
    lelobeamsts=executor.read_bus(StsOfLedLoBeamLe_HCML_can)
    rilobeamsts=executor.read_bus(StsOfLedLoBeamRi_HCMR_can)
    lowbeamindcrsts = executor.read_bus(LoBeamIndcr_FZCU_can)
    pytest.assume(lelobeamsts==0)
    pytest.assume(rilobeamsts==0)
    pytest.assume(lowbeamindcrsts==0)
    time.sleep(0.5)          



    
    

    
    

