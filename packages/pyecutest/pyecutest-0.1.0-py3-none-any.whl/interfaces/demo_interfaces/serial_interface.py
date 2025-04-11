"""
Demo Serial interface implementation.
This is a mock implementation that simulates serial communication without requiring actual hardware.
"""
from typing import Optional, List
import time
import random
import string

class DemoSerialInterface:
    """A demo implementation of serial interface for testing."""
    
    def __init__(self):
        self.is_connected = True
        self._param_values = {
            0x1000: 0x55,
            0x2000: 0xAA
        }
        self._write_data = b""
        
    def write(self, data: bytes) -> int:
        """Write data to the serial port.
        
        Args:
            data: The data to write
            
        Returns:
            int: Number of bytes written
        """
        if not self.is_connected:
            return 0
            
        # Store the written data
        self._write_data = data
            
        # Print the data for debugging
        print(f"Writing to serial port: {data.hex()}")
        return len(data)
        
    def readline(self) -> bytes:
        """Read a line from the serial port.
        
        Returns:
            bytes: The read line or None if error
        """
        if not self.is_connected:
            return None
            
        # Handle different commands
        if b"READ VERSION" in self._write_data:
            return b"VERSION 1.0.0\n"
            
        elif b"READ PARAM" in self._write_data:
            # Extract parameter address from command
            try:
                param_addr = int(self._write_data.split(b"READ PARAM ")[1].strip().split(b"\r")[0], 16)
                if param_addr in self._param_values:
                    return f"VALUE={hex(self._param_values[param_addr])}\n".encode()
            except:
                pass
                
        return b"ERROR\n"
        
    def connect(self) -> bool:
        """
        Connect to the serial port.
        
        Returns:
            bool: True if connection was successful
        """
        if not self.is_connected:
            print(f"Connecting to serial port")
            self.is_connected = True
            return True
        return False
        
    def disconnect(self) -> bool:
        """
        Disconnect from the serial port.
        
        Returns:
            bool: True if disconnection was successful
        """
        if self.is_connected:
            print(f"Disconnecting from serial port")
            self.is_connected = False
            return True
        return False
        
    def read(self, size: int = 1) -> Optional[bytes]:
        """
        Read data from the serial port.
        
        Args:
            size: Number of bytes to read
            
        Returns:
            Optional[bytes]: Read data or None if timeout
        """
        if not self.is_connected:
            print("Error: Not connected to serial port")
            return None
            
        # Simulate parameter read response
        if any(b"READ PARAM" in msg for msg in self._write_data):
            param_value = random.randint(0, 255)
            return f"PARAM_VALUE=0x{param_value:02X}".encode()
            
        # Generate random data for other cases
        data = ''.join(random.choices(string.ascii_letters + string.digits, k=size))
        return data.encode()
        
    def flush(self):
        """Flush the serial buffer."""
        self._write_data = b""
        
    def get_buffer_size(self) -> int:
        """
        Get the current size of the input buffer.
        
        Returns:
            int: Number of bytes in the buffer
        """
        return sum(len(data) for data in self._write_data) 