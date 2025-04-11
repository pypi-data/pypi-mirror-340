import pytest
from interfaces.canoe.canoe import Canoe
from interfaces.inca.inca import Inca, IncaWrapper
from interfaces.veristand.veristand import VeriStand
from lib import buslib
from lib import a2llib
from core.executor import TestExecutor
from logging import getLogger

import time


class TestClass:
    def setup_class(self):
        print("准备测试环境")

        self.executor = TestExecutor()
        self.logger = getLogger(__name__)
        
        
    def teardown_class(self):
        print("\n清理测试环境")
        # self.INCA.CloseExperiment()
        # self.CANOE.stop_measurement()
        # self.VERISTAND.disconnect()
        

    def test_FZCU(self):
        # 连接FZCU
        self.executor.write_sys_var('diagnostic::connect_FZCU',0)
        time.sleep(1)
        self.executor.write_sys_var('diagnostic::connect_FZCU',1)
        time.sleep(1)
        sys_variable = self.executor.read_sys_var('diagnostic::connect_FZCU')
        time.sleep(1)
        pytest.assume(sys_variable==1)

        # 进扩展模式
        set_point = [0x2,0x10,0x03,0,0,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::FZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(responseList[:2])
        pytest.assume(responseList[0:2]==(0x50,0x03))
        
        # 过安全访问
        self.executor.write_sys_var('diagnostic::FZCU_SecurityAccess_Level_RequestSeed',2)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        pytest.assume(responseList[0:2]==(0x67,0x03))
        '''
        if(responseList[2:]!=(0,0)):
            self.executor.write_sys_var('diagnostic::FZCU_SecurityAccess_Level_SendKey',2)
            time.sleep(1)
            responseList = self.executor.read_sys_var_array('diagnostic::responseList')
            pytest.assume(responseList[0:2]==(0x67,0x04))
        '''

        # 修改CarMode为normal
        set_point = [0x5,0x2F,0xD0,0x08,0x03,0x00,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::FZCU_customizedService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(responseList[:5])
        pytest.assume(responseList[0:5]==(0x6F,0xD0,0x08,0x03,0x00))

        # 确认当前CarMod为Normal
        set_point = [0x3,0x22,0xD0,0x08,0,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::FZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(responseList[:4])
        pytest.assume(responseList[0:4]==(0x62,0xD0,0x08,0x00))

        # 修改Pwrrmod为ACC
        set_point = [0x5,0x2F,0xD0,0x02,0x03,0x02,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::FZCU_customizedService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(responseList[:5])
        pytest.assume(responseList[0:5]==(0x6F,0xD0,0x02,0x03,0x02))

        # 确认当前Pwrmod
        set_point = [0x3,0x22,0xD0,0x02,0,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::FZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(responseList[:4])
        pytest.assume(responseList[0:4]==(0x62,0xD0,0x02,0x02))


    def test_LZCU(self):
        # 连接LZCU
        self.executor.write_sys_var('diagnostic::connect_LZCU',0)
        time.sleep(1)
        self.executor.write_sys_var('diagnostic::connect_LZCU',1)
        time.sleep(1)
        sys_variable = self.executor.read_sys_var('diagnostic::connect_LZCU')
        time.sleep(1)
        pytest.assume(sys_variable==1)
       
        # 进扩展模式
        set_point = [0x2,0x10,0x03,0,0,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(responseList[:2])
        pytest.assume(responseList[0:2]==(0x50,0x03))
       
        # 过安全访问
        self.executor.write_sys_var('diagnostic::LZCU_SecurityAccess_Level_RequestSeed',3)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        pytest.assume(responseList[0:2]==(0x67,0x05))
        '''
        if(responseList[2:]!=(0,0)):
            self.executor.write_sys_var('diagnostic::LZCU_SecurityAccess_Level_SendKey',3)
            time.sleep(1)
            responseList = self.executor.read_sys_var_array('diagnostic::responseList')
            pytest.assume(responseList[0:2]==(0x67,0x06))
        '''
   

    def test_main_driving_window_LZCU(self):
        # 触发主驾车窗自学习
        set_point = [0x9,0x31,0x01,0x43,0x85,0x00,0x00,0x00,0x00,0x00]
        self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        response_code = [hex(i) for i in responseList[:5]]
        self.logger.info(response_code)
        pytest.assume(responseList[0:5]==(0x71,0x01,0x43,0x85,0x02)),'响应码错误'     
        # 检查主驾车窗自学习状态
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查主驾车窗自学习状态：{ [hex(i) for i in responseList[:5]]}')
        count = 0
        self.logger.info(f'responselist: {responseList[4]}')
        while(responseList[4]!=0 and count<20):
            set_point = [0x4,0x31,0x03,0x43,0x85,0,0,0,0,0]
            self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
            time.sleep(1)
            count = count + 1
            responseList = self.executor.read_sys_var_array('diagnostic::responseList')
            self.logger.info(f"检查主驾车窗自学习：第{count}次循环,{[hex(i) for i in responseList[:5]]}")
            time.sleep(1)
        pytest.assume(responseList[:5]==(0x71,0x03,0x43,0x85,0x00))
        # 终止主驾车窗自学习
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'结束主驾车窗自学习：{[hex(i) for i in responseList[:5]]}')
        count = 0
        while(responseList[4]!=1 and count<20):
            set_point = [0x4,0x31,0x02,0x43,0x85,0,0,0,0,0]
            self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
            time.sleep(1)
            count = count + 1
            responseList = self.executor.read_sys_var_array('diagnostic::responseList')
            self.logger.info(f"结束主驾车窗自学习：第{count}次循环,{[hex(i) for i in responseList[:5]]}")
            time.sleep(1)
        pytest.assume(responseList[:5]==(0x71,0x02,0x43,0x85,0x01))


    def test_left_rear_window_LZCU(self):
        # 触发左后窗自学习
        set_point = [0x9,0x31,0x01,0x43,0x86,0x64,0x01,0x64,0x01,0x01]
        self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        response_code = [hex(i) for i in responseList[:5]]
        self.logger.info(response_code)
        assert(responseList[0:5]==(0x71,0x01,0x43,0x86,0x02)),'响应码错误'

        # 检查左后窗自学习状态
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查左后窗自学习状态：{ [hex(i) for i in responseList[:5]]}')
        count = 0
        self.logger.info(f'responselist: {responseList[4]}')
        while(responseList[4]!=0 and count<20):
            set_point = [0x4,0x31,0x03,0x43,0x86,0,0,0,0,0]
            self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
            time.sleep(1)
            count = count + 1
            responseList = self.executor.read_sys_var_array('diagnostic::responseList')
            self.logger.info(f"检查左后窗自学习：第{count}次循环,{[hex(i) for i in responseList[:5]]}")
            time.sleep(1)
        pytest.assume(responseList[:5]==(0x71,0x03,0x43,0x86,0x00))
        # 终止左后窗自学习
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'结束左后窗自学习：{[hex(i) for i in responseList[:5]]}')
        count = 0
        while(responseList[4]!=1 and count<20):
            set_point = [0x4,0x31,0x02,0x43,0x86,0,0,0,0,0]
            self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
            time.sleep(1)
            count = count + 1
            responseList = self.executor.read_sys_var_array('diagnostic::responseList')
            self.logger.info(f"结束左后窗自学习：第{count}次循环,{[hex(i) for i in responseList[:5]]}")
            time.sleep(1)
        pytest.assume(responseList[:5]==(0x71,0x02,0x43,0x86,0x01))


    def test_charge_cover_LZCU(self):
        # 触发充电口盖自学习
        set_point = [0x4,0x31,0x01,0x11,0x33,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        response_code = [hex(i) for i in responseList[:6]]
        self.logger.info(response_code)
        assert(responseList[0:6]==(0x71,0x01,0x11,0x33,0x00,0x00)),'响应码错误'
        # 检查充电口盖自学习状态
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查充电口盖自学习状态：{ [hex(i) for i in responseList[:5]]}')
        count = 0
        self.logger.info(f'responselist: {responseList[1]}')
        while(responseList[1]!=3 and count<20):
            set_point = [0x4,0x31,0x03,0x11,0x33,0,0,0,0,0]
            self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
            time.sleep(1)
            count = count + 1
            responseList = self.executor.read_sys_var_array('diagnostic::responseList')
            self.logger.info(f"检查充电口盖自学习：第{count}次循环,{[hex(i) for i in responseList[:5]]}")
            time.sleep(1)
        pytest.assume(responseList[:5]==(0x71,0x03,0x11,0x33,0x00))
        # 触发禁止关闭充电口盖
        set_point = [0x5,0x2F,0x05,0xA3,0x03,0x00,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        response_code = [hex(i) for i in responseList[:5]]
        self.logger.info(response_code)
        assert(responseList[0:5]==(0x6F,0x05,0xA3,0x03,0x01)),'响应码错误'
        # 确认禁止关闭充电口盖
        set_point = [0x3,0x22,0x05,0xA3,0,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'确认禁止关闭充电口盖：{ [hex(i) for i in responseList[:4]]}')
        pytest.assume(responseList[:4]==(0x62,0x05,0xA3,0x00))


    def test_front_rear_seat_LZCU(self):
        # 触发对前后排座椅同时进行自学习
        set_point = [0x4,0x31,0x01,0x43,0xA8,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        response_code = [hex(i) for i in responseList[:5]]
        self.logger.info(response_code)
        assert(responseList[0:5]==(0x71,0x01,0x43,0xA8,0x02)),'响应码错误'
        # 检查前后排座椅同时进行自学习状态
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查前后排座椅同时进行自学习状态：{ [hex(i) for i in responseList[:5]]}')
        count = 0
        self.logger.info(f'responselist: {responseList[1]}, {responseList[4]}')
        while((responseList[1]!=3 or responseList[4]!=0) and count<20):
            set_point = [0x4,0x31,0x03,0x43,0xA8,0,0,0,0,0]
            self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
            time.sleep(1)
            count = count + 1
            responseList = self.executor.read_sys_var_array('diagnostic::responseList')
            self.logger.info(f"检查前后排座椅同时进行自学习：第{count}次循环,{[hex(i) for i in responseList[:5]]}")
            time.sleep(1)
        pytest.assume(responseList[:5]==(0x71,0x03,0x43,0xA8,0x00))
        # 终止前后排座椅同时进行自学习
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'结束前后排座椅同时进行自学习：{[hex(i) for i in responseList[:5]]}')
        count = 0
        while((responseList[1]!=2 or responseList[4]!=1) and count<20):
            set_point = [0x4,0x31,0x02,0x43,0xA8,0,0,0,0,0]
            self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
            time.sleep(1)
            count = count + 1
            responseList = self.executor.read_sys_var_array('diagnostic::responseList')
            self.logger.info(f"结束前后排座椅同时进行自学习：第{count}次循环,{[hex(i) for i in responseList[:5]]}")
            time.sleep(1)
        pytest.assume(responseList[:5]==(0x71,0x02,0x43,0xA8,0x01))


    def test_main_door_handle_LZCU(self):    
        # 触发主驾门把手位置自学习
        # 请求清除主驾门把手位置
        set_point = [0x4,0x31,0x01,0x43,0x78,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        response_code = [hex(i) for i in responseList[:5]]
        self.logger.info(response_code)
        assert(responseList[0:5]==(0x71,0x01,0x43,0x78,0x02)),'响应码错误'
        # 检查主驾门把手位置清除状态
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查主驾门把手位置清除状态：{ [hex(i) for i in responseList[:5]]}')
        count = 0
        self.logger.info(f'responselist: {responseList[1]}, {responseList[4]}')
        while((responseList[1]!=3 or responseList[4]!=0) and count<20):
            set_point = [0x4,0x31,0x03,0x43,0x78,0,0,0,0,0]
            self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
            time.sleep(1)
            count = count + 1
            responseList = self.executor.read_sys_var_array('diagnostic::responseList')
            self.logger.info(f"检查主驾门把手位置清除：第{count}次循环,{[hex(i) for i in responseList[:5]]}")
            time.sleep(1)
        pytest.assume(responseList[:5]==(0x71,0x03,0x43,0x78,0x00))
        # 请求主驾门把手位置学习
        set_point = [0x4,0x31,0x01,0x43,0x77,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        response_code = [hex(i) for i in responseList[:6]]
        self.logger.info(response_code)
        assert(responseList[0:6]==(0x71,0x01,0x43,0x77,0x02,0x00)),'响应码错误'
        # 检查主驾门把手位置学习状态
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查主驾门把手位置学习状态：{ [hex(i) for i in responseList[:5]]}')
        count = 0
        self.logger.info(f'responselist: {responseList[1]}, {responseList[4]}')
        while((responseList[1]!=3 or responseList[4]!=0) and count<20):
            set_point = [0x4,0x31,0x03,0x43,0x77,0,0,0,0,0]
            self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
            time.sleep(1)
            count = count + 1
            responseList = self.executor.read_sys_var_array('diagnostic::responseList')
            self.logger.info(f"检查主驾门把手位置学习：第{count}次循环,{[hex(i) for i in responseList[:6]]}")
            time.sleep(1)
        pytest.assume(responseList[:6]==(0x71,0x03,0x43,0x77,0x00,0x00))
        # 主驾门把手位置回0位
        set_point = [0x4,0x31,0x01,0x43,0x79,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'主驾门把手位置回0位: { [hex(i) for i in responseList[:6]]}')
        pytest.assume(responseList[:6]==(0x71,0x01,0x43,0x79,0x02,0x00))
        # 检查主驾门把手位置回0位状态
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查主驾门把手位置回0位状态: { [hex(i) for i in responseList[:6]]}')
        count = 0
        self.logger.info(f'responselist: {responseList[1]}, {responseList[4]}')
        while((responseList[1]!=3 or responseList[4]!=0) and count<20):
            set_point = [0x4,0x31,0x03,0x43,0x79,0,0,0,0,0]
            self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
            time.sleep(1)
            count = count + 1
            responseList = self.executor.read_sys_var_array('diagnostic::responseList')
            self.logger.info(f"检查主驾门把手位置回0位: 第{count}次循环,{[hex(i) for i in responseList[:6]]}")
            time.sleep(1)
        pytest.assume(responseList[:6]==(0x71,0x03,0x43,0x79,0x00,0x00))


    def test_left_rear_door_handle_LZCU(self):   
        # 左后门把手位置自学习
        # 请求清除左后门把手位置
        set_point = [0x4,0x31,0x01,0x43,0x7B,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        response_code = [hex(i) for i in responseList[:5]]
        self.logger.info(response_code)
        assert(responseList[0:5]==(0x71,0x01,0x43,0x7B,0x02)),'响应码错误'
        # 检查左后门把手位置清除状态
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查左后门把手位置清除状态：{ [hex(i) for i in responseList[:5]]}')
        count = 0
        self.logger.info(f'responselist: {responseList[1]}, {responseList[4]}')
        while((responseList[1]!=3 or responseList[4]!=0) and count<20):
            set_point = [0x4,0x31,0x03,0x43,0x7B,0,0,0,0,0]
            self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
            time.sleep(1)
            count = count + 1
            responseList = self.executor.read_sys_var_array('diagnostic::responseList')
            self.logger.info(f"检查左后门把手位置清除：第{count}次循环,{[hex(i) for i in responseList[:5]]}")
            time.sleep(1)
        pytest.assume(responseList[:5]==(0x71,0x03,0x43,0x7B,0x00))
        # 请求左后门把手位置学习
        set_point = [0x4,0x31,0x01,0x43,0x7A,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        response_code = [hex(i) for i in responseList[:6]]
        self.logger.info(response_code)
        assert(responseList[0:6]==(0x71,0x01,0x43,0x7A,0x02,0x00)),'响应码错误'
        # 检查左后门把手位置学习状态
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查左后门把手位置学习状态：{ [hex(i) for i in responseList[:6]]}')
        count = 0
        self.logger.info(f'responselist: {responseList[1]}, {responseList[4]}')
        while((responseList[1]!=3 or responseList[4]!=0) and count<20):
            set_point = [0x4,0x31,0x03,0x43,0x7A,0,0,0,0,0]
            self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
            time.sleep(1)
            count = count + 1
            responseList = self.executor.read_sys_var_array('diagnostic::responseList')
            self.logger.info(f"检查左后门把手位置学习：第{count}次循环,{[hex(i) for i in responseList[:6]]}")
            time.sleep(1)
        pytest.assume(responseList[:6]==(0x71,0x03,0x43,0x7A,0x00,0x00))
        # 左后门把手位置回0位
        set_point = [0x4,0x31,0x01,0x43,0x7C,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'左后门把手位置回0位: { [hex(i) for i in responseList[:6]]}')
        pytest.assume(responseList[:6]==(0x71,0x01,0x43,0x7C,0x02,0x00))
        # 检查左后门把手位置回0位状态
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查左后门把手位置回0位状态: { [hex(i) for i in responseList[:6]]}')
        count = 0
        self.logger.info(f'responselist: {responseList[1]}, {responseList[4]}')
        while((responseList[1]!=3 or responseList[4]!=0) and count<20):
            set_point = [0x4,0x31,0x03,0x43,0x7C,0,0,0,0,0]
            self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
            time.sleep(1)
            count = count + 1
            responseList = self.executor.read_sys_var_array('diagnostic::responseList')
            self.logger.info(f"检查左后门把手位置回0位: 第{count}次循环,{[hex(i) for i in responseList[:6]]}")
            time.sleep(1)
        pytest.assume(responseList[:6]==(0x71,0x03,0x43,0x7C,0x00,0x00))


    def test_main_seat_heating_LZCU(self):
        # 打开主驾座椅加热（50%）
        # 请求主驾座椅加热（50%）
        set_point = [0x8,0x2F,0x3A,0x77,0x03,0x01,0x50,0x00,0xFF,0]
        self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        response_code = [hex(i) for i in responseList[:7]]
        self.logger.info(response_code)
        assert(responseList[0:7]==(0x6F,0x3A,0x77,0x03,0x00,0x00,0x00)),'响应码错误'
        # 检查主驾座椅加热（50%）
        set_point = [0x3,0x22,0x3A,0x77,0,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查主驾座椅加热(50%): { [hex(i) for i in responseList[:6]]}')
        pytest.assume(responseList[:6]==(0x62,0x3A,0x77,0x01,0x50,0x00))
        # 停止主驾座椅加热
        set_point = [0x5,0x2F,0x3A,0x77,0x00,0xFF,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'停止主驾座椅加热(50%): { [hex(i) for i in responseList[:7]]}')
        pytest.assume(responseList[:7]==(0x6F,0x3A,0x77,0x00,0x01,0x50,0x00))       


    def test_left_rear_seat_heating_LZCU(self):
        # 打开左后座椅加热（50%）
        # 请求左后座椅加热（50%）
        set_point = [0x8,0x2F,0x3E,0x28,0x03,0x01,0x50,0x00,0xFF,0]
        self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        response_code = [hex(i) for i in responseList[:7]]
        self.logger.info(response_code)
        assert(responseList[0:7]==(0x6F,0x3E,0x28,0x03,0x00,0x00,0x00)),'响应码错误'
        # 检查左后座椅加热（50%）
        set_point = [0x3,0x22,0x3E,0x28,0,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查左后座椅加热(50%): { [hex(i) for i in responseList[:6]]}')
        pytest.assume(responseList[:6]==(0x62,0x3E,0x28,0x01,0x50,0x00))
        # 停止左后座椅加热
        set_point = [0x5,0x2F,0x3E,0x28,0x00,0xFF,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'停止左后座椅加热(50%): { [hex(i) for i in responseList[:7]]}')
        pytest.assume(responseList[:7]==(0x6F,0x3E,0x28,0x00,0x01,0x50,0x00))


    def test_steering_wheel_heating_LZCU(self):
        # 打开方向盘加热（50%）
        # 请求打开方向盘加热（50%）
        set_point = [0x8,0x2F,0x3A,0x3F,0x03,0x01,0x50,0x00,0xFF,0]
        self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        response_code = [hex(i) for i in responseList[:7]]
        self.logger.info(response_code)
        assert(responseList[0:7]==(0x6F,0x3A,0x3F,0x03,0x00,0x00,0x00)),'响应码错误'
        # 检查方向盘加热（50%）
        set_point = [0x3,0x22,0x3A,0x3F,0,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查方向盘加热(50%): { [hex(i) for i in responseList[:6]]}')
        pytest.assume(responseList[:6]==(0x62,0x3A,0x3F,0x01,0x50,0x00))
        # 停止方向盘加热
        set_point = [0x5,0x2F,0x3A,0x3F,0x00,0xFF,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'停止方向盘加热(50%): { [hex(i) for i in responseList[:7]]}')
        pytest.assume(responseList[:7]==(0x6F,0x3A,0x3F,0x00,0x01,0x50,0x00))


    def test_steering_wheel_position_LZCU(self):
        # 方向盘管柱位置自学习
        # 请求方向盘管柱位置自学习
        set_point = [0x4,0x31,0x01,0x43,0x9C,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'请求方向盘管柱位置自学习: { [hex(i) for i in responseList[:5]]}')
        pytest.assume(responseList[:5]==(0x71,0x01,0x43,0x9C,0x02))
        # 检查方向盘管柱位置自学习状态
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查方向盘管柱位置自学习状态: { [hex(i) for i in responseList[:6]]}')
        count = 0
        while((responseList[1]!=3 or responseList[4]!=0) and count<20):
            set_point = [0x4,0x31,0x03,0x43,0x9C,0,0,0,0,0]
            self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
            time.sleep(1)
            count = count + 1
            responseList = self.executor.read_sys_var_array('diagnostic::responseList')
            self.logger.info(f"检查方向盘管柱位置自学习: 第{count}次循环,{[hex(i) for i in responseList[:6]]}")
            time.sleep(1)
        pytest.assume(responseList[:6]==(0x71,0x03,0x43,0x9C,0x00,0x02))
        # 读取方向盘管柱位置自学习状态
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'读取方向盘管柱位置自学习状态: { [hex(i) for i in responseList[:4]]}')
        set_point = [0x3,0x22,0x3A,0x17,0,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'读取方向盘管柱位置自学习状态: { [hex(i) for i in responseList[:4]]}')
        pytest.assume(responseList[:4]==(0x62,0x3A,0x17,0x02))


    def test_left_mirror_heating_LZCU(self):
        # 打开左后视镜加热
        # 请求打开左后视镜加热
        set_point = [0x5,0x2F,0x3A,0x1E,0x03,0x01,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'请求打开左后视镜加热: { [hex(i) for i in responseList[:5]]}')
        pytest.assume(responseList[:5]==(0x6F,0x3A,0x1E,0x03,0x00))
        # 检查左后视镜加热状态
        set_point = [0x3,0x22,0x3A,0x1E,0,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查左后视镜加热状态: { [hex(i) for i in responseList[:4]]}')
        pytest.assume(responseList[:4]==(0x62,0x3A,0x1E,0x01))
        # 停止左后视镜加热
        set_point = [0x4,0x2F,0x3A,0x1E,0x00,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'停止左后视镜加热: { [hex(i) for i in responseList[:5]]}')
        pytest.assume(responseList[:5]==(0x6F,0x3A,0x1E,0x00,0x00))


    def test_external_mirror_driving_condition_LZCU(self):
        # 检查外后视镜驱动条件是否具备
        # 请求检查外后视镜驱动条件是否具备
        set_point = [0x4,0x31,0x01,0x11,0x32,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'请求检查外后视镜驱动条件是否具备: { [hex(i) for i in responseList[:6]]}')
        pytest.assume(responseList[:6]==(0x71,0x01,0x11,0x32,0x02,0x01))
        # 检查外后视镜驱动条件是否具备状态
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查外后视镜驱动条件是否具备状态: { [hex(i) for i in responseList[:6]]}')
        count = 0
        while((responseList[1]!=3 or responseList[4]!=0) and count<20):
            set_point = [0x4,0x31,0x03,0x11,0x32,0,0,0,0,0]
            self.executor.write_sys_var_array('diagnostic::LZCU_customizeService',set_point)
            time.sleep(1)
            count = count + 1
            responseList = self.executor.read_sys_var_array('diagnostic::responseList')
            self.logger.info(f"检查外后视镜驱动条件是否具备: 第{count}次循环,{[hex(i) for i in responseList[:6]]}")
            time.sleep(1)
        pytest.assume(responseList[:6]==(0x71,0x03,0x11,0x32,0x00,0x00))


    def test_RZCU(self):
        # 连接RZCU
        self.executor.write_sys_var('diagnostic::connect_RZCU',0)
        time.sleep(1)
        self.executor.write_sys_var('diagnostic::connect_RZCU',1)
        time.sleep(1)
        sys_variable = self.executor.read_sys_var('diagnostic::connect_RZCU')
        time.sleep(1)
        pytest.assume(sys_variable==1)

        # 进扩展模式
        set_point = [0x2,0x10,0x03,0,0,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(responseList[:2])
        pytest.assume(responseList[0:2]==(0x50,0x03))

        # 过安全访问
        self.executor.write_sys_var('diagnostic::RZCU_SecurityAccess_Level_RequestSeed',3)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        pytest.assume(responseList[0:2]==(0x67,0x05))
        '''
        if(responseList[2:]!=(0,0)):
            self.executor.write_sys_var('diagnostic::RZCU_SecurityAccess_Level_SendKey',3)
            time.sleep(1)
            responseList = self.executor.read_sys_var_array('diagnostic::responseList')
            pytest.assume(responseList[0:2]==(0x67,0x06))
        '''


    def test_electric_rear_tailgate_RZCU(self):
        # 电动尾门自学习
        # 请求电动尾门自学习
        set_point = [0x4,0x31,0x01,0x43,0xE5,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'请求电动尾门自学习: { [hex(i) for i in responseList[:6]]}')
        pytest.assume(responseList[:6]==(0x71,0x01,0x43,0xE5,0x02,0x00))
        # 检查电动尾门自学习状态
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查电动尾门自学习状态: { [hex(i) for i in responseList[:6]]}')
        count = 0
        while((responseList[1]!=3 or responseList[4]!=0) and count<20):
            set_point = [0x4,0x31,0x03,0x43,0xE5,0,0,0,0,0]
            self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
            time.sleep(1)
            count = count + 1
            responseList = self.executor.read_sys_var_array('diagnostic::responseList')
            self.logger.info(f"检查电动尾门自学习: 第{count}次循环,{[hex(i) for i in responseList[:6]]}")
            time.sleep(1)
        pytest.assume(responseList[:6]==(0x71,0x03,0x43,0xE5,0x00,0x00))


    def test_passenger_driving_window_RZCU(self):
        # 副驾车窗自学习
        # 请求副驾车窗自学习
        set_point = [0x9,0x31,0x01,0x43,0x35,0x00,0x00,0x00,0x00,0x00]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'请求副驾车窗自学习: { [hex(i) for i in responseList[:5]]}')
        pytest.assume(responseList[:5]==(0x71,0x01,0x43,0x35,0x02))
        # 检查副驾车窗自学习状态
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查副驾车窗自学习状态: { [hex(i) for i in responseList[:5]]}')
        count = 0
        while((responseList[1]!=3 or responseList[4]!=0) and count<20):
            set_point = [0x4,0x31,0x03,0x43,0x35,0,0,0,0,0]
            self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
            time.sleep(1)
            count = count + 1
            responseList = self.executor.read_sys_var_array('diagnostic::responseList')
            self.logger.info(f"检查副驾车窗自学习: 第{count}次循环,{[hex(i) for i in responseList[:5]]}")
            time.sleep(1)
        pytest.assume(responseList[:5]==(0x71,0x03,0x43,0x35,0x00))


    def test_right_rear_window_RZCU(self):
        # 右后车窗自学习
        # 请求右后车窗自学习
        set_point = [0x9,0x31,0x01,0x43,0x36,0x00,0x00,0x00,0x00,0x00]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'请求右后车窗自学习: { [hex(i) for i in responseList[:5]]}')
        pytest.assume(responseList[:5]==(0x71,0x01,0x43,0x36,0x02))
        # 检查右后车窗自学习状态
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查右后车窗自学习状态: { [hex(i) for i in responseList[:5]]}')
        count = 0
        while((responseList[1]!=3 or responseList[4]!=0) and count<20):
            set_point = [0x4,0x31,0x03,0x43,0x36,0,0,0,0,0]
            self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
            time.sleep(1)
            count = count + 1
            responseList = self.executor.read_sys_var_array('diagnostic::responseList')
            self.logger.info(f"检查右后车窗自学习: 第{count}次循环,{[hex(i) for i in responseList[:5]]}")
            time.sleep(1)
        pytest.assume(responseList[:5]==(0x71,0x03,0x43,0x36,0x00))


    def test_front_rear_seat_RZCU(self):
        # 对前后排座椅同时进行自学习
        # 请求对前后排座椅同时进行自学习
        set_point = [0x4,0x31,0x01,0x43,0x60,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'请求对前后排座椅同时进行自学习: { [hex(i) for i in responseList[:5]]}')
        pytest.assume(responseList[:5]==(0x71,0x01,0x43,0x60,0x02))
        # 检查对前后排座椅同时进行自学习状态
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查对前后排座椅同时进行自学习状态: { [hex(i) for i in responseList[:5]]}')
        count = 0
        while((responseList[1]!=3 or responseList[4]!=0) and count<20):
            set_point = [0x4,0x31,0x03,0x43,0x60,0,0,0,0,0]
            self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
            time.sleep(1)
            count = count + 1
            responseList = self.executor.read_sys_var_array('diagnostic::responseList')
            self.logger.info(f"检查对前后排座椅同时进行自学习: 第{count}次循环,{[hex(i) for i in responseList[:5]]}")
            time.sleep(1)
        pytest.assume(responseList[:5]==(0x71,0x03,0x43,0x60,0x00))


    def test_passenger_seat_heating_RZCU(self):
        # 打开副驾座椅加热（50%）
        # 请求打开副驾座椅加热（50%）
        set_point = [0x8,0x2F,0x3E,0x26,0x03,0x01,0x50,0x00,0xFF,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'请求打开副驾座椅加热(50%): { [hex(i) for i in responseList[:7]]}')
        pytest.assume(responseList[:7]==(0x6F,0x3E,0x26,0x03,0x00,0x00,0x00))
        # 检查副驾座椅加热（50%）
        set_point = [0x3,0x22,0x3E,0x26,0,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查副驾座椅加热(50%): { [hex(i) for i in responseList[:6]]}')
        pytest.assume(responseList[:6]==(0x62,0x3E,0x26,0x01,0x50,0x00))
        # 停止副驾座椅加热
        set_point = [0x5,0x2F,0x3E,0x26,0x00,0xFF,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'停止副驾座椅加热(50%): { [hex(i) for i in responseList[:7]]}')
        pytest.assume(responseList[:7]==(0x6F,0x3E,0x26,0x00,0x01,0x50,0x00))


    def test_passenger_seat_ventilation_RZCU(self):
        # 打开副驾座椅通风（50%）
        # 请求打开副驾座椅通风（50%）
        set_point = [0x7,0x2F,0x3E,0x27,0x03,0x50,0x00,0xFF,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'请求打开副驾座椅通风(50%): { [hex(i) for i in responseList[:6]]}')
        pytest.assume(responseList[:6]==(0x6F,0x3E,0x27,0x03,0x00,0x00))
        # 检查副驾座椅通风（50%）
        set_point = [0x3,0x22,0x3E,0x27,0,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查副驾座椅通风(50%): { [hex(i) for i in responseList[:5]]}')
        pytest.assume(responseList[:5]==(0x62,0x3E,0x27,0x50,0x01))
        # 停止副驾座椅通风
        set_point = [0x5,0x2F,0x3E,0x27,0x00,0xFF,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'停止副驾座椅通风(50%): { [hex(i) for i in responseList[:7]]}')
        pytest.assume(responseList[:7]==(0x6F,0x3E,0x27,0x00,0x01,0x50,0x01))


    def test_middle_seat_heating_RZCU(self):
        # 打开后排中间座椅加热（50%）
        # 请求打开后排中间座椅加热（50%）
        set_point = [0x8,0x2F,0x3E,0x02,0x03,0x01,0x50,0x00,0xFF,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'请求打开后排中间座椅加热(50%): { [hex(i) for i in responseList[:7]]}')
        pytest.assume(responseList[:7]==(0x6F,0x3E,0x02,0x03,0x00,0x00,0x00))
        # 检查后排中间座椅加热（50%）
        set_point = [0x3,0x22,0x3E,0x02,0,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查后排中间座椅加热(50%): { [hex(i) for i in responseList[:6]]}')
        pytest.assume(responseList[:6]==(0x62,0x3E,0x02,0x01,0x50,0x00))
        # 停止后排中间座椅加热
        set_point = [0x5,0x2F,0x3E,0x02,0x00,0xFF,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'停止后排中间座椅加热(50%): { [hex(i) for i in responseList[:7]]}')
        pytest.assume(responseList[:7]==(0x6F,0x3E,0x02,0x00,0x01,0x50,0x00))


    def test_right_rear_seat_heating_RZCU(self):
        # 打开右后座椅加热（50%）
        # 请求打开右后座椅加热（50%）
        set_point = [0x8,0x2F,0x3E,0x2A,0x03,0x01,0x50,0x00,0xFF,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'请求打开右后座椅加热(50%): { [hex(i) for i in responseList[:7]]}')
        pytest.assume(responseList[:7]==(0x6F,0x3E,0x2A,0x03,0x00,0x00,0x00))
        # 检查右后座椅加热（50%）
        set_point = [0x3,0x22,0x3E,0x2A,0,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查右后座椅加热(50%): { [hex(i) for i in responseList[:6]]}')
        pytest.assume(responseList[:6]==(0x62,0x3E,0x2A,0x01,0x50,0x00))
        # 停止右后座椅加热
        set_point = [0x5,0x2F,0x3E,0x2A,0x00,0xFF,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'停止右后座椅加热(50%): { [hex(i) for i in responseList[:7]]}')
        pytest.assume(responseList[:7]==(0x6F,0x3E,0x2A,0x00,0x01,0x50,0x00))


    def test_right_mirror_heating_RZCU(self):
        # 右后视镜加热
        # 请求右后视镜加热
        set_point = [0x5,0x2F,0x3E,0x1D,0x03,0x01,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'请求右后视镜加热: { [hex(i) for i in responseList[:5]]}')
        pytest.assume(responseList[:5]==(0x6F,0x3E,0x1D,0x03,0x00))
        # 检查右后视镜加热状态
        set_point = [0x3,0x22,0x3E,0x1D,0,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查右后视镜加热状态: { [hex(i) for i in responseList[:4]]}')
        pytest.assume(responseList[:4]==(0x62,0x3E,0x1D,0x01))    
        # 停止右后视镜加热
        set_point = [0x4,0x2F,0x3E,0x1D,0x00,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'停止右后视镜加热: { [hex(i) for i in responseList[:5]]}')
        pytest.assume(responseList[:5]==(0x6F,0x3E,0x1D,0x00,0x01))


    def test_right_inner_EC_mirror_driving_condition_RZCU(self):
        # 驱动右内EC镜
        # 请求驱动右内EC镜
        set_point = [0x5,0x2F,0x3E,0x1E,0x03,0x01,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'请求驱动右内EC镜: { [hex(i) for i in responseList[:5]]}')
        pytest.assume(responseList[:5]==(0x6F,0x3E,0x1E,0x03,0x00))
        # 读取右内EC镜状态
        set_point = [0x3,0x22,0x3E,0x1E,0,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'读取右内EC镜状态: { [hex(i) for i in responseList[:4]]}')
        pytest.assume(responseList[:4]==(0x62,0x3E,0x1E,0x01))
        # 停止驱动右内EC镜
        set_point = [0x4,0x2F,0x3E,0x1E,0x00,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'停止驱动右内EC镜: { [hex(i) for i in responseList[:5]]}')
        pytest.assume(responseList[:5]==(0x6F,0x3E,0x1E,0x00,0x01))


    def test_right_inner_EC_mirror_close_RZCU(self):
        # 关闭右内EC镜
        # 请求关闭右内EC镜
        set_point = [0x5,0x2F,0x3E,0x1E,0x03,0x00,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'请求关闭右内EC镜: { [hex(i) for i in responseList[:5]]}')
        pytest.assume(responseList[:5]==(0x6F,0x3E,0x1E,0x03,0x00)) 
        # 读取右内EC镜状态
        set_point = [0x3,0x22,0x3E,0x1E,0,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'读取右内EC镜状态: { [hex(i) for i in responseList[:4]]}')
        pytest.assume(responseList[:4]==(0x62,0x3E,0x1E,0x00))
        # 停止驱动右内EC镜
        set_point = [0x4,0x2F,0x3E,0x1E,0x00,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'停止驱动右内EC镜: { [hex(i) for i in responseList[:5]]}')
        pytest.assume(responseList[:5]==(0x6F,0x3E,0x1E,0x00,0x00))


    def test_rear_windshield_heating_RZCU(self):
        # 打开后风挡加热（电阻丝）
        # 请求打开后风挡加热（电阻丝）
        set_point = [0x5,0x2F,0x3A,0xA8,0x03,0x01,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'请求打开后风挡加热(电阻丝): { [hex(i) for i in responseList[:5]]}')
        pytest.assume(responseList[:5]==(0x6F,0x3A,0xA8,0x03,0x00))
        # 读取后风挡加热状态
        set_point = [0x3,0x22,0x3A,0xA8,0,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'读取后风挡加热状态: { [hex(i) for i in responseList[:4]]}')
        pytest.assume(responseList[:4]==(0x62,0x3A,0xA8,0x01))
        # 停止后风挡加热
        set_point = [0x4,0x2F,0x3A,0xA8,0x00,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'停止后风挡加热: { [hex(i) for i in responseList[:5]]}')
        pytest.assume(responseList[:5]==(0x6F,0x3A,0xA8,0x00,0x01))


    def test_passenger_door_handle_RZCU(self):
        # 副驾驶门把手自学习
        # 副驾驶门把手位置清除
        set_point = [0x4,0x31,0x01,0x43,0x38,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'副驾驶门把手位置清除: { [hex(i) for i in responseList[:5]]}')
        pytest.assume(responseList[:5]==(0x71,0x01,0x43,0x38,0x02))
        # 检查副驾门把手位置清除状态
        set_point = [0x4,0x31,0x03,0x43,0x38,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查副驾门把手位置清除状态: { [hex(i) for i in responseList[:5]]}')
        pytest.assume(responseList[:5]==(0x71,0x03,0x43,0x38,0x00))
        # 请求副驾门把手位置学习
        set_point = [0x4,0x31,0x01,0x43,0x37,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'请求副驾门把手位置学习: { [hex(i) for i in responseList[:6]]}')
        pytest.assume(responseList[:6]==(0x71,0x01,0x43,0x37,0x02,0x00))
        # 检查副驾门把手位置学习状态
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查副驾门把手位置学习状态: { [hex(i) for i in responseList[:6]]}')
        count = 0
        while(responseList[1]!=3 or responseList[4]!=0 and count<20):
            set_point = [0x4,0x31,0x03,0x43,0x37,0,0,0,0,0]
            self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
            time.sleep(1)
            count = count + 1
            responseList = self.executor.read_sys_var_array('diagnostic::responseList')
            self.logger.info(f"检查副驾门把手位置学习状态: 第{count}次循环,{[hex(i) for i in responseList[:6]]}")
            time.sleep(1)
        pytest.assume(responseList[:6]==(0x71,0x03,0x43,0x37,0x00,0x00))
        # 副驾门把手位置回0位
        set_point = [0x4,0x31,0x01,0x43,0x41,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'副驾门把手位置回0位: { [hex(i) for i in responseList[:6]]}')
        pytest.assume(responseList[:6]==(0x71,0x01,0x43,0x41,0x02,0x00))
        # 检查副驾门把手位置回0位状态
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查副驾门把手位置回0位状态: { [hex(i) for i in responseList[:6]]}')
        count = 0
        while(responseList[1]!=3 or responseList[4]!=0 and count<20):
            set_point = [0x4,0x31,0x03,0x43,0x41,0,0,0,0,0]
            self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
            time.sleep(1)
            count = count + 1
            responseList = self.executor.read_sys_var_array('diagnostic::responseList')
            self.logger.info(f"检查副驾门把手位置回0位状态: 第{count}次循环,{[hex(i) for i in responseList[:6]]}")
            time.sleep(1)
        pytest.assume(responseList[:6]==(0x71,0x03,0x43,0x41,0x00,0x00))


    def test_right_rear_door_handle_RZCU(self):
        # 右后门把手自学习
        # 右后门把手位置清除
        set_point = [0x4,0x31,0x01,0x43,0x4B,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'右后门把手位置清除: { [hex(i) for i in responseList[:5]]}')
        pytest.assume(responseList[:5]==(0x71,0x01,0x43,0x4B,0x02))
        # 检查右后门把手位置清除状态
        set_point = [0x4,0x31,0x03,0x43,0x4B,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查右后门把手位置清除状态: { [hex(i) for i in responseList[:5]]}')
        pytest.assume(responseList[:5]==(0x71,0x03,0x43,0x4B,0x00))
        # 请求右后门把手位置学习
        set_point = [0x4,0x31,0x01,0x43,0x49,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'请求右后门把手位置学习: { [hex(i) for i in responseList[:6]]}')
        pytest.assume(responseList[:6]==(0x71,0x01,0x43,0x49,0x02,0x00))
        # 检查右后门把手位置学习状态
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查右后门把手位置学习状态: { [hex(i) for i in responseList[:6]]}')
        count = 0
        while(responseList[1]!=3 or responseList[4]!=0 and count<20):
            set_point = [0x4,0x31,0x03,0x43,0x49,0,0,0,0,0]
            self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
            time.sleep(1)
            count = count + 1
            responseList = self.executor.read_sys_var_array('diagnostic::responseList')
            self.logger.info(f"检查右后门把手位置学习状态: 第{count}次循环,{[hex(i) for i in responseList[:6]]}")
            time.sleep(1)
        pytest.assume(responseList[:6]==(0x71,0x03,0x43,0x49,0x00,0x00))
        # 右后门把手位置回0位
        set_point = [0x4,0x31,0x01,0x43,0x4C,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'右后门把手位置回0位: { [hex(i) for i in responseList[:6]]}')
        pytest.assume(responseList[:6]==(0x71,0x01,0x43,0x4C,0x02,0x00))
        # 检查右后门把手位置回0位状态
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查右后门把手位置回0位状态: { [hex(i) for i in responseList[:6]]}')
        count = 0
        while(responseList[1]!=3 or responseList[4]!=0 and count<20):
            set_point = [0x4,0x31,0x03,0x43,0x4C,0,0,0,0,0]
            self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
            time.sleep(1)
            count = count + 1
            responseList = self.executor.read_sys_var_array('diagnostic::responseList')
            self.logger.info(f"检查右后门把手位置回0位状态: 第{count}次循环,{[hex(i) for i in responseList[:6]]}")
            time.sleep(1)
        pytest.assume(responseList[:6]==(0x71,0x03,0x43,0x4C,0x00,0x00))


    def test_external_mirror_driving_condition_RZCU(self):
        # 检查外后视镜驱动条件是否具备
        # 请求检查外后视镜驱动条件是否具备
        set_point = [0x4,0x31,0x01,0x43,0x30,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'请求检查外后视镜驱动条件是否具备: { [hex(i) for i in responseList[:6]]}')
        pytest.assume(responseList[:6]==(0x71,0x01,0x43,0x30,0x02,0x00))
        # 检查外后视镜驱动条件是否具备状态
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查外后视镜驱动条件是否具备状态: { [hex(i) for i in responseList[:6]]}')
        count = 0
        while(responseList[1]!=3 or responseList[4]!=0 and count<20):
            set_point = [0x4,0x31,0x03,0x43,0x30,0,0,0,0,0]
            self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
            time.sleep(1)
            count = count + 1
            responseList = self.executor.read_sys_var_array('diagnostic::responseList')
            self.logger.info(f"检查外后视镜驱动条件是否具备状态: 第{count}次循环,{[hex(i) for i in responseList[:6]]}")
            time.sleep(1)
        pytest.assume(responseList[:6]==(0x71,0x03,0x43,0x30,0x00,0x00))


    def test_electric_front_tailgate_RZCU(self):
        # 电动前舱盖位置学习
        # 请求电动前舱盖位置学习
        set_point = [0x4,0x31,0x01,0x43,0x5A,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'请求电动前舱盖位置学习: { [hex(i) for i in responseList[:6]]}')
        pytest.assume(responseList[:6]==(0x71,0x01,0x43,0x5A,0x02,0x00))
        # 检查电动前舱盖位置学习状态
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查电动前舱盖位置学习状态: { [hex(i) for i in responseList[:6]]}')
        count = 0
        while(responseList[1]!=3 or responseList[4]!=0 and count<20):
            set_point = [0x4,0x31,0x03,0x43,0x5A,0,0,0,0,0]
            self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
            time.sleep(1)
            count = count + 1
            responseList = self.executor.read_sys_var_array('diagnostic::responseList')
            self.logger.info(f"检查电动前舱盖位置学习状态: 第{count}次循环,{[hex(i) for i in responseList[:6]]}")
            time.sleep(1)
        pytest.assume(responseList[:6]==(0x71,0x03,0x43,0x5A,0x00,0x00))
        # 请求关闭电动前舱盖
        set_point = [0x4,0x31,0x01,0x43,0x5C,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'请求关闭电动前舱盖: { [hex(i) for i in responseList[:6]]}')
        pytest.assume(responseList[:6]==(0x71,0x01,0x43,0x5C,0x02,0x00))
        # 检查关闭电动前舱盖状态
        set_point = [0x4,0x31,0x03,0x43,0x5C,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::RZCU_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(f'检查关闭电动前舱盖状态: { [hex(i) for i in responseList[:6]]}')
        pytest.assume(responseList[:6]==(0x71,0x03,0x43,0x5C,0x00,0x00))


    def test_HCML(self):
        # 连接HCML
        self.executor.write_sys_var('diagnostic::connectHCML',0)
        time.sleep(1)
        self.executor.write_sys_var('diagnostic::connectHCML',1)
        time.sleep(1)
        sys_variable = self.executor.read_sys_var('diagnostic::connectHCML')
        time.sleep(1)
        pytest.assume(sys_variable==1)

        # 进扩展模式
        set_point = [0x2,0x10,0x03,0,0,0,0,0,0,0]
        self.executor.write_sys_var_array('diagnostic::HCML_customizeService',set_point)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        self.logger.info(responseList[:2])
        pytest.assume(responseList[0:2]==(0x50,0x03))

        # 过安全访问
        self.executor.write_sys_var('diagnostic::HCML_SecurityAccess_Level_RequestSeed',3)
        time.sleep(1)
        responseList = self.executor.read_sys_var_array('diagnostic::responseList')
        pytest.assume(responseList[0:2]==(0x67,0x05)) 
        '''
        if(responseList[2:]!=(0,0)):
            self.executor.write_sys_var('diagnostic::HCML_SecurityAccess_Level_SendKey',3)
            time.sleep(1)
            responseList = self.executor.read_sys_var_array('diagnostic::responseList')
            pytest.assume(responseList[0:2]==(0x67,0x06))
        '''

        # 左大灯标定
        # 关闭HB
        # 关闭LB+SBL
        # 点亮LB+SBL
        # 点亮HB
        # 关闭HB
        # 关闭LB+SBL
        # 停止控制HB
        # 关闭ADB




        # 恢复为默认模式

    


if __name__=='__main__':
    tester = TestClass()
    tester.test_DEMO()

        

            


        



        



        

        

        
    