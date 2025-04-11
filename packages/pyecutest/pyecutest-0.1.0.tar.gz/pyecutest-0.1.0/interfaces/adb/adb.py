import subprocess

class adb:
    def __init__(self, logger):
        self.logger = logger

    def adb_tap(self, x:int, y:int):
        subprocess.run(f'adb shell input tap {x} {y}')

    def adb_swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: int):
        """adb滑动"""
        subprocess.run(f'adb shell input swipe {start_x} {start_y} {end_x} {end_y} {duration}')
    
    def adb_input(self, text: str):
        """adb输入"""
        subprocess.run(f'adb shell input {text}')
    
    def adb_pull(self, remote_path: str, local_path: str):
        """adb拉取文件"""
        subprocess.run(f'adb pull {remote_path} resource/{local_path}')
    
    def adb_push(self, local_path: str, remote_path: str):
        """adb推送文件"""
        subprocess.run(f'adb push resource/{local_path} {remote_path}')
    
    def adb_devices(self):
        """获取adb设备列表"""
        return subprocess.run('adb devices', capture_output=True, text=True).stdout

    def adb_connect(self, device_id: str):
        """连接adb设备"""
        subprocess.run(f'adb connect {device_id}')

    def adb_disconnect(self, device_id: str):
        """断开adb设备"""
        subprocess.run(f'adb disconnect {device_id}')
    
    def adb_custom_command(self, command: str):
        """执行adb自定义命令"""
        subprocess.run(f'adb {command}')
