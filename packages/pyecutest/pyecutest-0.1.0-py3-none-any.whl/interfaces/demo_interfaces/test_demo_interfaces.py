"""
Test script to demonstrate the usage of demo interfaces.
"""
from typing import Dict, Any
from message_interface import DemoMessageHandler, Message, MessageType
from rest_interface import DemoRestInterface, Resource
from can_interface import DemoCANInterface
from serial_interface import DemoSerialInterface
import time

def test_message_interface():
    """测试消息接口的功能"""
    print("\n测试消息接口:")
    
    # 创建消息处理器实例
    handler = DemoMessageHandler()
    
    # 定义消息处理函数
    def message_callback(message: Message):
        print(f"收到消息 - 类型: {message.type.value}, 内容: {message.content}")
        print(f"元数据: {message.metadata}")
    
    # 订阅消息
    handler.subscribe(message_callback)
    
    # 创建并发布消息
    test_message = Message(
        type=MessageType.INFO,
        content="这是一条测试消息",
        metadata={"timestamp": "2024-04-09", "source": "test"}
    )
    handler.publish(test_message)
    
    # 取消订阅
    handler.unsubscribe(message_callback)
    
    print("消息接口测试完成")

def test_rest_interface():
    """测试REST接口的功能"""
    print("\n测试REST接口:")
    
    # 创建REST接口实例
    rest = DemoRestInterface()
    
    # 测试创建资源
    test_data = {"name": "测试资源", "value": 123}
    resource = rest.create(test_data)
    print(f"创建资源: ID={resource.id}, 数据={resource.data}")
    
    # 测试读取资源
    read_resource = rest.read(resource.id)
    print(f"读取资源: ID={read_resource.id}, 数据={read_resource.data}")
    
    # 测试更新资源
    update_data = {"name": "更新后的资源", "value": 456}
    updated = rest.update(resource.id, update_data)
    print(f"更新资源: ID={updated.id}, 数据={updated.data}")
    
    # 测试删除资源
    deleted = rest.delete(resource.id)
    print(f"删除资源: {'成功' if deleted else '失败'}")
    
    # 测试读取已删除的资源
    deleted_resource = rest.read(resource.id)
    print(f"读取已删除的资源: {'不存在' if deleted_resource is None else '存在'}")
    
    print("REST接口测试完成")

def test_can_interface():
    """Test the demo CAN interface."""
    # Create CAN interface instance
    can = DemoCANInterface(channel=0, baudrate=500000)
    
    try:
        # Connect to CAN interface
        assert can.connect(), "Failed to connect to CAN interface"
        
        # Send some test messages
        test_messages = [
            (0x100, [0x01, 0x02, 0x03, 0x04]),
            (0x101, [0x05, 0x06, 0x07, 0x08]),
            (0x102, [0x09, 0x0A, 0x0B, 0x0C]),
        ]
        
        for msg_id, data in test_messages:
            assert can.send_message(msg_id, data), f"Failed to send message {msg_id}"
            time.sleep(0.1)  # Small delay between messages
            
        # Check message counts
        for msg_id, _ in test_messages:
            count = can.get_message_count(msg_id)
            print(f"Message 0x{msg_id:03X} was sent {count} times")
            
        # Try to receive messages
        for msg_id, _ in test_messages:
            received = can.receive_message(msg_id)
            if received:
                print(f"Received message 0x{msg_id:03X}: {received.hex()}")
            else:
                print(f"No message received for 0x{msg_id:03X}")
                
    finally:
        # Disconnect from CAN interface
        can.disconnect()

def test_serial_interface():
    """Test the demo serial interface."""
    # Create serial interface instance
    serial = DemoSerialInterface(port="COM1", baudrate=9600)
    
    try:
        # Connect to serial port
        assert serial.connect(), "Failed to connect to serial port"
        
        # Write some test data
        test_data = [
            b"Hello, World!",
            b"Test message 1",
            b"Test message 2",
        ]
        
        for data in test_data:
            bytes_written = serial.write(data)
            print(f"Wrote {bytes_written} bytes: {data}")
            time.sleep(0.1)  # Small delay between writes
            
        # Read some data
        for _ in range(3):
            data = serial.read(10)
            if data:
                print(f"Read data: {data}")
            else:
                print("No data received")
                
        # Read a line
        line = serial.readline()
        if line:
            print(f"Read line: {line}")
        else:
            print("No line received")
            
        # Check buffer size
        print(f"Buffer size: {serial.get_buffer_size()} bytes")
        
    finally:
        # Disconnect from serial port
        serial.disconnect()

if __name__ == "__main__":
    # 运行所有测试
    test_message_interface()
    test_rest_interface()
    
    print("\nTesting CAN Interface:")
    test_can_interface()
    
    print("\nTesting Serial Interface:")
    test_serial_interface() 