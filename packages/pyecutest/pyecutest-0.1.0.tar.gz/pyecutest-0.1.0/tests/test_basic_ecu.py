import pytest
from interfaces.demo_interfaces.can_interface import DemoCANInterface
from interfaces.demo_interfaces.serial_interface import DemoSerialInterface

@pytest.fixture
def can_interface():
    """Fixture to provide a CAN interface instance."""
    interface = DemoCANInterface()
    return interface

@pytest.fixture
def serial_interface():
    """Fixture to provide a serial interface instance."""
    interface = DemoSerialInterface()
    return interface

def test_can_message_send(can_interface):
    """Test basic CAN message sending functionality."""
    # Send a simple diagnostic request
    message_id = 0x7DF
    message_data = [0x02, 0x10, 0x01]  # Standard diagnostic request
    
    # Send the message
    result = can_interface.send_message(message_id, message_data)
    
    # Verify the message was sent successfully
    assert result == True, "Failed to send CAN message"

def test_serial_communication(serial_interface):
    """Test basic serial communication."""
    # Send a simple command
    command = b"READ VERSION\r\n"
    
    # Write the command
    bytes_written = serial_interface.write(command)
    
    # Verify command was written successfully
    assert bytes_written == len(command), "Failed to write serial command"
    
    # Read the response
    response = serial_interface.readline()
    
    # Verify we got some response
    assert response is not None, "No response received"
    assert len(response) > 0, "Empty response received"

@pytest.mark.parametrize("param_address,param_value", [
    (0x1000, 0x55),
    (0x2000, 0xAA)
])
def test_parameter_read(serial_interface, param_address, param_value):
    """Test parameter reading with different values."""
    # Send parameter read command
    command = f"READ PARAM {hex(param_address)}\r\n".encode()
    serial_interface.write(command)
    
    # Read response
    response = serial_interface.readline()
    
    # Verify response format
    assert response is not None, "No response received"
    assert b"VALUE=" in response, "Invalid response format"
    
    # For demo interface, we expect it to echo back a simple response
    expected = f"VALUE={hex(param_value)}\n".encode()
    assert response == expected, f"Unexpected parameter value" 