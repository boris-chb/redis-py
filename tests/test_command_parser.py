import unittest
from commands import parse_command


class TestCommandParser(unittest.TestCase):
    def test_parse_command(self):
        self.assertEqual(parse_command("GET key"), ("GET", ["key"]))
        self.assertEqual(parse_command("SET key value"), ("SET", ["key", "value"]))


if __name__ == "__main__":
    unittest.main()
