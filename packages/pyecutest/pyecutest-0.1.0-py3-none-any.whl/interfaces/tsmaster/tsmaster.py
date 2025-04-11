import time

import pythoncom
import win32com.client


class TSMaster:
    def __init__(self):
        self.formMan = None
        self.app = None
        self.com = None
        pythoncom.CoInitialize()  # enable multithread
        self.open()
        self.start_measurement()

    def open(self):
        self.app = win32com.client.Dispatch("TSMaster.TSApplication")
        self.com = self.app.TSCOM()  # win32com.client.Dispatch("TSMaster.TSCOM")
        self.formMan = self.app.TSFormManager()
        # self.formMan.show_main_form()

    def close(self):
        del self.app
        del self.com
        del self.formMan

    def start_measurement(self):
        self.app.connect()  # 启动
        self.com.fifo_enable_receive_fifo()  # 允许接收缓存

    def stop_measurement(self):
        self.app.disconnect()

    def get_signal_value(self, channel: int, network: str, nodename: str, messagename: str, signalname: str, value: float):
        sig_val = self.com.can_rbs_get_signal_value_by_element(channel, network, nodename, messagename, signalname, value)
        return sig_val

    def set_signal_value(self, channel: int, network: str, nodename: str, messagename: str, signalname: str, value: float):
        self.com.can_rbs_set_signal_value_by_element(channel, network, nodename, messagename, signalname, value)


if __name__ == '__main__':
    ts = TSMaster()
    ts.open()
    time.sleep(5)
    ts.start_measurement()
    ts.app.wait(2000)
    res = ts.get_signal_value(2, "ChassisFusionCANFD", "XCD", "EPS_ChassisFusion_0xB5", "EPSMotTqCmd",1)
    print(res)
    ts.app.wait(1000)
    ts.set_signal_value(2, "ChassisFusionCANFD", "XCD", "EPS_ChassisFusion_0xB5", "EPSMotTqCmd",1)
    res = ts.get_signal_value(2, "ChassisFusionCANFD", "XCD", "EPS_ChassisFusion_0xB5", "EPSMotTqCmd",1)
    print(res)
    ts.app.wait(2000)
    ts.stop_measurement()
    ts.app.wait(2000)
    ts.close()
