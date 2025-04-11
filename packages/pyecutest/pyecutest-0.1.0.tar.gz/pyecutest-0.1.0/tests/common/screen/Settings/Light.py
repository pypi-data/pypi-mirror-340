import time
from core.executor import TestExecutor

class ExteriorLight:
    def __init__(self,executor: TestExecutor) :
        self.executor = executor

    def exterior_light_switch(self,sts:str):
        '''
        外灯开关
        '''
        self.executor.adb_tap_by_setting('灯光')
        self.executor.adb_tap_by_text('外灯', sts)
        pass
    
    def exterior_light_delay_off(self):
        '''
        外灯离车延时照明
        '''
        pass

    def adaptive_high_beam(self):
        '''
        自适应远光灯
        '''
        pass

class AmbientLight:

    def ambient_light_switch(self):
        '''
        氛围灯开关
        '''
        pass
    
    def ambient_light_mode(self):
        '''
        氛围灯模式
        '''
        pass

    def ambient_light_brightness(self):
        '''
        氛围灯亮度
        '''
        pass

    def ambient_light_color(self):
        '''
        氛围灯颜色
        '''
        pass

    def ambient_light_breath_ratebreath_rate(self):
        '''
        氛围灯呼吸频率
        '''
        pass

    def ambient_light_rhythm_effect(self):
        '''
        氛围灯律动效果
        '''
        pass

    def ambient_light_entry_exit_effect(self):
        '''
        上下车灯效
        '''
        pass

class ReadingLight:

    def reading_light_switch(self):
        '''
        阅读灯开关
        '''
        pass

class ButtonBrightness:

    def button_brightness_adjust(self):
        '''
        按键亮度
        '''
        pass





