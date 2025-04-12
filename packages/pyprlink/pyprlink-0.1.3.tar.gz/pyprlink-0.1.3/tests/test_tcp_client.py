from unittest.mock import Mock, patch
from pyprlink.tcp_client import ask_PV, read_until_done, PORT
import os
import pytest

def test_timeout_error():
    with patch('socket.socket') as mock_socket:
        mock_sock = Mock()
        mock_socket.return_value = mock_sock
        mock_sock.connect.side_effect = TimeoutError("Connection timed out")
        # The function should handle the timeout gracefully
        ask_PV("-gmp", "x")
        # No exception should be raised

def test_port_is_convertible_to_int():
    """Test that PORT string from .env can be converted to an integer"""
    port_str = PORT
    assert port_str is not None, "PORT should be defined in .env"
    try:
        port_int = int(port_str)
        assert port_int > 0, "PORT should be a positive number"
    except ValueError:
        pytest.fail(f"PORT value '{port_str}' cannot be converted to integer")

