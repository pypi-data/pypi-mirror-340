"""
Test case for ECU communication using PyECUTest.
"""
import pytest
from interfaces.demo_interfaces.can_interface import DemoCANInterface
from interfaces.demo_interfaces.serial_interface import DemoSerialInterface

@pytest.fixture(scope="module")
def can_interface():
    """Fixture to provide CAN interface."""
    can = DemoCANInterface(channel=0, baudrate=500000)
    can.connect()
    yield can
    can.disconnect()

@pytest.fixture(scope="module")
def serial_interface():
    """Fixture to provide serial interface."""
    serial = DemoSerialInterface(port="COM1", baudrate=9600)
    serial.connect()
    yield serial
    serial.disconnect()

def test_ecu_diagnostic_request(can_interface):
    """Test sending diagnostic request to ECU."""
    # Send diagnostic request (0x7DF is the broadcast address for diagnostic requests)
    request_data = [0x02, 0x10, 0x01]  # UDS request for diagnostic session control
    assert can_interface.send_message(0x7DF, request_data), "Failed to send diagnostic request"
    
    # Wait for response
    response = can_interface.receive_message(0x7E8)  # 0x7E8 is the typical response address
    assert response is not None, "No response received from ECU"
    assert len(response) >= 3, "Response too short"
    assert response[0] == 0x03, "Invalid response length"
    assert response[1] == 0x50, "Invalid response service ID"
    assert response[2] == 0x01, "Invalid response subfunction"

def test_ecu_parameter_read(serial_interface):
    """Test reading parameter from ECU via serial interface."""
    # Send parameter read command
    command = b"READ PARAM 0x1000\r\n"  # Example parameter address
    bytes_written = serial_interface.write(command)
    assert bytes_written == len(command), "Failed to write command"
    
    # Read response
    response = serial_interface.readline()
    print(f"Parameter read response: {response}")
    assert response is not None, "No response received"
    assert b"VALUE=" in response, "Invalid response format"

def test_ecu_communication_sequence(can_interface, serial_interface):
    """Test a complete ECU communication sequence."""
    # Step 1: Send diagnostic request
    request_data = [0x02, 0x10, 0x01]
    assert can_interface.send_message(0x7DF, request_data), "Failed to send diagnostic request"
    
    # Step 2: Verify diagnostic session
    response = can_interface.receive_message(0x7E8)
    print(f"Diagnostic response: {response}")
    assert response is not None, "No diagnostic response"
    assert response[1] == 0x50, "Invalid diagnostic response"
    
    # Step 3: Read parameter via serial
    command = b"READ PARAM 0x1000\r\n"
    bytes_written = serial_interface.write(command)
    assert bytes_written == len(command), "Failed to write parameter read command"
    
    # Step 4: Verify parameter value
    response = serial_interface.readline()
    print(f"Parameter read response: {response}")
    assert response is not None, "No parameter response"
    assert b"VALUE=" in response, "Invalid parameter response"
    
    # Step 5: Send parameter update
    update_command = b"WRITE PARAM 0x1000 0x55\r\n"
    bytes_written = serial_interface.write(update_command)
    assert bytes_written == len(update_command), "Failed to write parameter update command"
    
    # Step 6: Verify update response
    response = serial_interface.readline()
    print(f"Parameter write response: {response}")
    assert response is not None, "No update response"
    assert b"UPDATE_OK" in response, "Parameter update failed"

@pytest.mark.parametrize("param_id,expected_value", [
    (0x1000, 0x55),
    (0x1001, 0xAA),
    (0x1002, 0xFF),
])
def test_ecu_parameter_values(serial_interface, param_id, expected_value):
    """Test reading multiple parameter values."""
    command = f"READ PARAM 0x{param_id:04X}\r\n".encode()
    bytes_written = serial_interface.write(command)
    assert bytes_written == len(command), f"Failed to write command for parameter 0x{param_id:04X}"
    
    response = serial_interface.readline()
    print(f"Parameter read response for 0x{param_id:04X}: {response}")
    assert response is not None, f"No response for parameter 0x{param_id:04X}"
    assert f"VALUE=0x{expected_value:02X}".encode() in response, f"Invalid value for parameter 0x{param_id:04X}" 