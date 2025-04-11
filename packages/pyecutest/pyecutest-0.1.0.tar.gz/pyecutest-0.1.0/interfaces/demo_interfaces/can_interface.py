"""
Demo CAN interface implementation.
This is a mock implementation that simulates CAN communication without requiring actual hardware.
"""
from typing import List, Dict, Optional
import time
import random

class DemoCANInterface:
    """A demo implementation of CAN interface for testing."""
    
    def __init__(self):
        self.is_connected = True
        
    def send_message(self, message_id: int, data: list) -> bool:
        """Send a CAN message.
        
        Args:
            message_id: The CAN message ID
            data: List of data bytes to send
            
        Returns:
            bool: True if message was sent successfully
        """
        if not self.is_connected:
            return False
            
        # Print the message for debugging
        print(f"Sending CAN message: ID={hex(message_id)}, Data={[hex(x) for x in data]}")
        return True
        
    def receive_message(self, message_id: int, timeout: float = 1.0) -> bytes:
        """Receive a CAN message.
        
        Args:
            message_id: The CAN message ID to receive
            timeout: Timeout in seconds
            
        Returns:
            bytes: Received message data or None if timeout
        """
        if not self.is_connected:
            return None
            
        # For demo, just return a simple response
        if message_id == 0x7E8:  # Standard diagnostic response ID
            return b"\x03\x50\x01"  # Positive response to session control
        return None
        
    def connect(self) -> bool:
        """
        Connect to the CAN interface.
        
        Returns:
            bool: True if connection was successful
        """
        if not self.is_connected:
            print(f"Connecting to CAN channel {self.channel} at {self.baudrate} bps")
            self.is_connected = True
            return True
        return False
        
    def disconnect(self) -> bool:
        """
        Disconnect from the CAN interface.
        
        Returns:
            bool: True if disconnection was successful
        """
        if self.is_connected:
            print(f"Disconnecting from CAN channel {self.channel}")
            self.is_connected = False
            return True
        return False
        
    def get_message_count(self, message_id: int) -> int:
        """
        Get the number of times a message has been sent.
        
        Args:
            message_id: CAN message ID
            
        Returns:
            int: Number of times the message has been sent
        """
        return len(self.message_history.get(message_id, []))
        
    def clear_message_history(self) -> None:
        """Clear the message history."""
        self.message_history.clear() 