# 添加项目根目录到系统路径
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from py_canoe import CANoe
import datetime
from threading import Lock
from config.config import config

class Canoe:
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Canoe, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        with self._lock:
            if not hasattr(self, '_init'):
                self._init = True
                print(config.get('canoe'))
                # 从配置文件中读取需要执行的CAPL函数列表
                self.user_capl_functions = config.get('canoe.capl_functions')
                # 删除空白和重复
                if self.user_capl_functions:
                    self.user_capl_functions = set(self.user_capl_functions)
                    self.user_capl_functions.discard("")
                    self.user_capl_functions = tuple(self.user_capl_functions) if self.user_capl_functions else tuple()
                else:
                    self.user_capl_functions = tuple()
                self.canoe_inst = CANoe(user_capl_functions=self.user_capl_functions)  # 初始化CANoe函数

                self.canoe_inst.open(
                    canoe_cfg=config.get('canoe.project_file'),
                    visible=True, 
                    auto_save=True, 
                    prompt_user=False, 
                    auto_stop=True
                )
                self.canoe_inst.start_measurement()

    def open(self,proj_path):
        self.canoe_inst.open(canoe_cfg=proj_path)   # open中自带get_application
        self.canoe_inst.get_canoe_version_info()


    def get_application(self):
        self.canoe_inst.get_application()

    def close(self):
        self.canoe_inst.quit()

    
    def start_measurement(self):
        self.canoe_inst.start_measurement()


    def stop_measurement(self):
        self.canoe_inst.stop_measurement()
        

    def finally_get_value(self, bus: str, channel: int, message: str, signal: str,expression_value, time, raw_value=False):
        begin_time = datetime.now().timestamp()
        while True:
            sig_val = self.canoe_inst.get_signal_value(bus, channel, message, signal, raw_value)
            if sig_val == expression_value:
                break
            if datetime.now().timestamp() - begin_time >= time:
                break
        return sig_val
    

    # sig_val = canoe_inst.get_signal_value('CAN', 1, 'VCCD_ZCUCANFD_0x110', 'PwrModSigGrpChks')
    def get_signal_value(self, bus: str, channel: int, message: str, signal: str, raw_value=False):
        sig_val = self.canoe_inst.get_signal_value(bus, channel, message, signal, raw_value)
        return sig_val
    

    def set_signal_value(self, bus: str, channel: int, message: str, signal: str, value: int, raw_value=False):
        self.canoe_inst.set_signal_value(bus, channel, message, signal, value, raw_value)  
        
        
    def get_sys_variable(self, variable_name: str):
        return self.canoe_inst.get_system_variable_value(variable_name)

    def set_sys_variable(self, variable_name: str, value: int):
        self.canoe_inst.set_system_variable_value(variable_name, value)

    def get_sys_variable_array(self, variable_name: str):
        return self.canoe_inst.get_system_variable_value(variable_name)

    def set_sys_variable_array(self, variable_name: str, value: list):
        self.canoe_inst.set_system_variable_array_values(variable_name, value)
        
    def execute_capl_function(self, function_name: str, *args) -> bool:
        """
        执行CAPL函数
        Args:
            function_name: CAPL函数名
            *args: 函数参数, 数量必须与CAPL函数参数数量一致,且CAPL函数参数类型只能为long,dword,double
        """
        # 调用CAPL函数
        self.canoe_inst.call_capl_function(function_name, *args)
        

            

canoe_inst = Canoe()
