from cases.common.Pwrmod import pwrmod
from cases.common.screen.Settings import Light
from cases.common.Steercontrol import steercontrol
from lib.a2llib import *
from lib.buslib import *
from core.executor import TestExecutor
import time
import pytest

class high_beam_switch:

    def test_high_beam_switch_ACC(self,executor:TestExecutor):

        # 电源模式ACC
        pwrmod(executor)
        time.sleep(0.5)

        #打开近光灯
        Light.exterior_light_switch('近光灯')
        time.sleep(0.5)

        #check近光灯状态
        lelobeamsts=executor.read_bus(StsOfLedLoBeamLe_HCML_can)
        rilobeamsts=executor.read_bus(StsOfLedLoBeamRi_HCMR_can)
        pytest.assume(lelobeamsts==1)
        pytest.assume(rilobeamsts==1)
        time.sleep(0.5)

        #外推远光拨杆打开远光灯
        steercontrol(1)
        time.sleep(0.5)

        #check远光灯状态
        lehibeamsts = executor.read_bus(StsOfLedHiBeamLe_HCML_can)
        rihibeamsts = executor.read_bus(StsOfLedHiBeamRi_HCMR_can)
        indcrhibeamsts = executor.read_bus(HiBeamIndcr_FZCU_can)
        pytest.assume(lehibeamsts == 1)
        pytest.assume(rihibeamsts == 1)
        pytest.assume(indcrhibeamsts == 1)
        time.sleep(0.5)

        #再次外推远光拨杆关闭远光灯
        steercontrol(1)
        time.sleep(0.5)

        #check 远光灯状态
        lehibeamsts = executor.read_bus(StsOfLedHiBeamLe_HCML_can)
        rihibeamsts = executor.read_bus(StsOfLedHiBeamRi_HCMR_can)
        indcrhibeamsts = executor.read_bus(HiBeamIndcr_FZCU_can)
        pytest.assume(lehibeamsts == 0)
        pytest.assume(rihibeamsts == 0)
        pytest.assume(indcrhibeamsts == 0)
        time.sleep(0.5)

        #外推远光拨杆打开远光灯
        steercontrol(1)
        time.sleep(0.5)

        #check远光灯状态
        lehibeamsts = executor.read_bus(StsOfLedHiBeamLe_HCML_can)
        rihibeamsts = executor.read_bus(StsOfLedHiBeamRi_HCMR_can)
        indcrhibeamsts = executor.read_bus(HiBeamIndcr_FZCU_can)
        pytest.assume(lehibeamsts == 1)
        pytest.assume(rihibeamsts == 1)
        pytest.assume(indcrhibeamsts == 1)
        time.sleep(0.5)

        #内拨动远光拨杆关闭远光灯
        steercontrol(2)
        time.sleep(0.5)

        #check 远光灯状态
        lehibeamsts = executor.read_bus(StsOfLedHiBeamLe_HCML_can)
        rihibeamsts = executor.read_bus(StsOfLedHiBeamRi_HCMR_can)
        indcrhibeamsts = executor.read_bus(HiBeamIndcr_FZCU_can)
        pytest.assume(lehibeamsts == 0)
        pytest.assume(rihibeamsts == 0)
        pytest.assume(indcrhibeamsts == 0)
        

    def test_high_beam_switch_RUN(executor):

        # 电源模式ACC
        pwrmod()
        time.sleep(0.5)

        #打开近光灯
        Light.exterior_light_switch('近光灯')
        time.sleep(0.5)

        #check近光灯状态
        lelobeamsts=executor.read_bus(StsOfLedLoBeamLe_HCML_can)
        rilobeamsts=executor.read_bus(StsOfLedLoBeamRi_HCMR_can)
        pytest.assume(lelobeamsts==1)
        pytest.assume(rilobeamsts==1)
        time.sleep(0.5)

        #外推远光拨杆打开远光灯
        steercontrol(1)
        time.sleep(0.5)

        #check远光灯状态
        lehibeamsts = executor.read_bus(StsOfLedHiBeamLe_HCML_can)
        rihibeamsts = executor.read_bus(StsOfLedHiBeamRi_HCMR_can)
        indcrhibeamsts = executor.read_bus(HiBeamIndcr_FZCU_can)
        pytest.assume(lehibeamsts == 1)
        pytest.assume(rihibeamsts == 1)
        pytest.assume(indcrhibeamsts == 1)
        time.sleep(0.5)

        #再次外推远光拨杆关闭远光灯
        steercontrol(1)
        time.sleep(0.5)

        #check 远光灯状态
        lehibeamsts = executor.read_bus(StsOfLedHiBeamLe_HCML_can)
        rihibeamsts = executor.read_bus(StsOfLedHiBeamRi_HCMR_can)
        indcrhibeamsts = executor.read_bus(HiBeamIndcr_FZCU_can)
        pytest.assume(lehibeamsts == 0)
        pytest.assume(rihibeamsts == 0)
        pytest.assume(indcrhibeamsts == 0)
        time.sleep(0.5)

        #外推远光拨杆打开远光灯
        steercontrol(1)
        time.sleep(0.5)

        #check远光灯状态
        lehibeamsts = executor.read_bus(StsOfLedHiBeamLe_HCML_can)
        rihibeamsts = executor.read_bus(StsOfLedHiBeamRi_HCMR_can)
        indcrhibeamsts = executor.read_bus(HiBeamIndcr_FZCU_can)
        pytest.assume(lehibeamsts == 1)
        pytest.assume(rihibeamsts == 1)
        pytest.assume(indcrhibeamsts == 1)
        time.sleep(0.5)

        #内拨动远光拨杆关闭远光灯
        steercontrol(2)
        time.sleep(0.5)

        #check 远光灯状态
        lehibeamsts = executor.read_bus(StsOfLedHiBeamLe_HCML_can)
        rihibeamsts = executor.read_bus(StsOfLedHiBeamRi_HCMR_can)
        indcrhibeamsts = executor.read_bus(HiBeamIndcr_FZCU_can)
        pytest.assume(lehibeamsts == 0)
        pytest.assume(rihibeamsts == 0)
        pytest.assume(indcrhibeamsts == 0)

               



    
    

    
    

