from cases.common.Pwrmod.pwrmod import pwrmod
from cases.common.screen.Settings.Light import ExteriorLight
from cases.common.Steercontrol.steercontrol import SteerContrl
from core.executor import TestExecutor
from lib.a2llib import *
from lib.buslib import *
import time
import pytest

class TestHighBeamSwitchACC:


    def test_high_beam_switch_ACC(self,executor:TestExecutor):

        # 电源模式ACC
        pwrmod(executor,PwrModMgrSafe_CalPwrModStsByPassVal_C.Enum_PwrModSts_ACC)
        time.sleep(0.5)

        #打开近光灯
        ExteriorLight.exterior_light_switch('近光灯')
        time.sleep(0.5)

        # #check近光灯状态
        # lelobeamsts=executor.read_bus(StsOfLedLoBeamLe_HCML_can)
        # rilobeamsts=executor.read_bus(StsOfLedLoBeamRi_HCMR_can)
        # pytest.assume(lelobeamsts==1)
        # pytest.assume(rilobeamsts==1)
        # time.sleep(0.5)

        # #外推远光拨杆打开远光灯
        # SteerContrl.high_beam_lever(SwtHiBeam_SWM_can.Push)
        # time.sleep(0.5)

        # #check远光灯状态
        # executor.read_bus(StsOfLedHiBeamLe_HCML_can,StsOfLedHiBeamLe_HCML_can.On)
        # executor.read_bus(StsOfLedHiBeamRi_HCMR_can,StsOfLedHiBeamRi_HCMR_can.On)
        # executor.read_bus(HiBeamIndcr_FZCU_can,HiBeamIndcr_FZCU_can.BlueLamp_With_IHC_ON)
        # time.sleep(0.5)

        # #再次外推远光拨杆关闭远光灯
        # SteerContrl.high_beam_lever(SwtHiBeam_SWM_can.Push)
        # time.sleep(0.5)

        # #check 远光灯状态
        # executor.read_bus(StsOfLedHiBeamLe_HCML_can,StsOfLedHiBeamLe_HCML_can.Off)
        # executor.read_bus(StsOfLedHiBeamRi_HCMR_can,StsOfLedHiBeamRi_HCMR_can.Off)
        # executor.read_bus(HiBeamIndcr_FZCU_can,HiBeamIndcr_FZCU_can.Indicator_OFF)
        # time.sleep(0.5)

        # #外推远光拨杆打开远光灯
        # SteerContrl.high_beam_lever(SwtHiBeam_SWM_can.Push)
        # time.sleep(0.5)

        # #check远光灯状态
        # executor.read_bus(StsOfLedHiBeamLe_HCML_can,StsOfLedHiBeamLe_HCML_can.On)
        # executor.read_bus(StsOfLedHiBeamRi_HCMR_can,StsOfLedHiBeamRi_HCMR_can.On)
        # executor.read_bus(HiBeamIndcr_FZCU_can,HiBeamIndcr_FZCU_can.BlueLamp_With_IHC_ON)
        # time.sleep(0.5)

        # #内拨动远光拨杆关闭远光灯
        # SteerContrl.high_beam_lever(SwtHiBeam_SWM_can.Pull)
        # time.sleep(0.5)

        # #check 远光灯状态
        # executor.read_bus(StsOfLedHiBeamLe_HCML_can,StsOfLedHiBeamLe_HCML_can.Off)
        # executor.read_bus(StsOfLedHiBeamRi_HCMR_can,StsOfLedHiBeamRi_HCMR_can.Off)
        # executor.read_bus(HiBeamIndcr_FZCU_can,HiBeamIndcr_FZCU_can.Indicator_OFF)
        # time.sleep(0.5)

               



    
    

    
    

