import socket
import json
from interfaces.mi_ant import mi_ant_lib

class mi_ant:
    def __init__(self, port):
        self.data_json = {
            name: {
                "value": getattr(mi_ant_lib, name).value,
                "byte_index": getattr(mi_ant_lib, name).byte_index,
                "bit_index": getattr(mi_ant_lib, name).bit_index
            } 
            for name in dir(mi_ant_lib)
            if isinstance(getattr(mi_ant_lib, name), type)}
        self.create_client(port)
    
    def create_client(self, port):
        self.socket_client = socket.socket()
        try:
            self.socket_client.connect(("localhost", port))
            self.mi_ant_status = True
        except Exception as e:
            print(f"连接失败: {e}")
            self.mi_ant_status = False
    
    def close_client(self):
        if self.socket_client is not None:
            self.socket_client.close()
    
    def write_signal(self, signal_name: classmethod, signal_value):
        if self.mi_ant_status:
            data_json = {
                signal_name.__name__:{
                    "value": signal_value,
                    "byte_index": signal_name.byte_index,
                    "bit_index": signal_name.bit_index,
                }
            }
            self.socket_client.send(json.dumps(data_json).encode("UTF-8"))
        else:
            print("mi_ant未连接")
    
    def read_signal(self, signal_name: classmethod):
        if self.mi_ant_status:
            recv_data = self.socket_client.recv(4096).decode("UTF-8")
            data_json = json.loads(recv_data)
            return data_json[signal_name.__name__]["value"]
        else:
            print("mi_ant未连接")


