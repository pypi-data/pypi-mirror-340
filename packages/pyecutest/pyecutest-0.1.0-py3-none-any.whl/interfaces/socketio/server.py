import socket
import threading
import json
import logging

class SocketServer:
    def __init__(self, host='localhost', port=8080, buffer_size=8192):
        """
        初始化Socket服务器
        :param host: 服务器地址
        :param port: 服务器端口
        :param buffer_size: 接收缓冲区大小，默认8192字节
        """
        self.host = host
        self.port = port
        self.server = None
        self.clients = []
        self.running = False
        self.buffer_size = buffer_size
        
        # 配置日志
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('SocketServer')

    def start(self):
        """
        启动服务器
        """
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host, self.port))
            self.server.listen(5)
            self.running = True
            
            self.logger.info(f"服务器启动成功 - {self.host}:{self.port}")
            
            # 启动接收客户端连接的线程
            accept_thread = threading.Thread(target=self._accept_connections)
            accept_thread.daemon = True
            accept_thread.start()
            
            return True
        except Exception as e:
            self.logger.error(f"服务器启动失败: {str(e)}")
            return False

    def stop(self):
        """
        停止服务器
        """
        self.running = False
        if self.server:
            self.server.close()
        for client in self.clients:
            client.close()
        self.clients = []
        self.logger.info("服务器已停止")

    def _accept_connections(self):
        """
        接受客户端连接的循环
        """
        while self.running:
            try:
                client_socket, address = self.server.accept()
                self.clients.append(client_socket)
                self.logger.info(f"新客户端连接: {address}")
                
                # 为每个客户端创建一个处理线程
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()
            except Exception as e:
                if self.running:
                    self.logger.error(f"接受连接时出错: {str(e)}")

    def _handle_client(self, client_socket, address):
        """
        处理单个客户端连接
        :param client_socket: 客户端socket对象
        :param address: 客户端地址
        """
        while self.running:
            try:
                # 接收数据
                data = client_socket.recv(self.buffer_size).decode('utf-8')
                if not data:
                    self.logger.info(f"客户端 {address} 正常断开连接")
                    break
                
                self.logger.info(f"收到来自 {address} 的数据: {data}")
                
                # 处理命令
                response = self._process_command(data)
                
                # 发送响应
                try:
                    client_socket.send(json.dumps(response).encode('utf-8'))
                except ConnectionError:
                    self.logger.info(f"客户端 {address} 连接已断开，无法发送响应")
                    break
                
            except ConnectionError as e:
                self.logger.info(f"客户端 {address} 连接已断开: {str(e)}")
                break
            except Exception as e:
                self.logger.error(f"处理客户端 {address} 数据时出错: {str(e)}")
                break
        
        # 清理连接
        try:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            client_socket.close()
        except Exception as e:
            self.logger.error(f"清理客户端 {address} 连接时出错: {str(e)}")
        
        self.logger.info(f"客户端断开连接: {address}")

    def _process_command(self, command):
        """
        处理接收到的命令
        :param command: 接收到的命令字符串
        :return: 处理结果
        """
        try:
            # 这里可以根据实际需求实现不同命令的处理逻辑
            if command == "TEST_COMMAND":
                return {
                    "status": "success",
                    "message": "测试命令执行成功",
                    "data": None
                }
            else:
                return {
                    "status": "error",
                    "message": f"未知命令: {command}",
                    "data": None
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"命令处理出错: {str(e)}",
                "data": None
            }

if __name__ == "__main__":
    # 服务器使用示例
    server = SocketServer()
    server.start()
    
    try:
        # 保持主线程运行
        while True:
            pass
    except KeyboardInterrupt:
        server.stop()
