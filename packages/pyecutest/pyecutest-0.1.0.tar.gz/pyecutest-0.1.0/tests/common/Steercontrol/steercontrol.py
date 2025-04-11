from lib.buslib import *
from core.executor import TestExecutor
import time

class SteerContrl:

    def high_beam_lever(executor: TestExecutor, sts:str):
        '''
        远光拨杆
        '''
        executor.write_bus(SwtHiBeam_SWM_can, 0)
        time.sleep(0.2)
        executor.write_bus(SwtHiBeam_SWM_can, str)
        time.sleep(0.2)
        executor.write_bus(SwtHiBeam_SWM_can, 0)
        