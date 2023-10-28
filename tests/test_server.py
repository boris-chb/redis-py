import unittest
from unittest.mock import Mock
from src.server import execute_command


class TestExecuteCommand(unittest.TestCase):
    def test_get_command(self):
        mock_socket = Mock()
        execute_command("GET", ["key"], mock_socket)
        mock_socket.sendall.assert_called_with(b"nil")

    def test_set_command(self):
        mock_socket = Mock()
        execute_command("SET", ["key", "value"], mock_socket)
        mock_socket.sendall.assert_called_with(b"OK")

    def test_set_command_wrong_args(self):
        mock_socket = Mock()
        execute_command("SET", ["key"], mock_socket)
        mock_socket.sendall.assert_called_with(b"ERR wrong number of arguments for SET")


if __name__ == "__main__":
    unittest.main()
