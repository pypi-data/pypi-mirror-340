import socket
import time

class SocketClient:
    def __init__(self, host='localhost', port=8080, buffer_size=8192):
        """初始化Socket客户端
        
        Args:
            host (str): 服务器地址，默认localhost
            port (int): 端口号，默认8080
            buffer_size (int): 接收缓冲区大小，默认8192字节
        """
        self.host = host
        self.port = port
        self.socket = None
        self.buffer_size = buffer_size
        
    def connect(self):
        """连接到服务器"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            return True
        except Exception as e:
            print(f"连接失败: {str(e)}")
            return False
            
    def disconnect(self):
        """断开连接"""
        if self.socket:
            try:
                self.socket.shutdown(socket.SHUT_RDWR)  # 正确关闭连接
                self.socket.close()
            except Exception:
                pass  # 忽略关闭时的错误
            finally:
                self.socket = None
            
    def send_command(self, command):
        """
        发送命令到服务器
        :param command: 要发送的命令
        :return: (success, response) 元组
        """
        if not self.socket:
            return False, "未连接到服务器"
        
        try:
            # 发送数据
            self.socket.send(command.encode('utf-8'))
            
            # 等待并接收响应
            response = self.socket.recv(self.buffer_size).decode('utf-8')
            return True, response
            
        except ConnectionError as e:
            self.socket = None
            return False, f"连接错误: {str(e)}"
        except Exception as e:
            return False, f"发送命令时出错: {str(e)}"


if __name__ == "__main__":
    client = SocketClient(host='localhost', port=8080)
    client.connect()
    client.send_command("hello")
    client.disconnect()

