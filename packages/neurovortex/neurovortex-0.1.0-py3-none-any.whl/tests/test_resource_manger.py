import unittest
from neurovortex.resource_manager import ResourceManager

class TestResourceManager(unittest.TestCase):
    def test_cpu_usage(self):
        cpu_usage = ResourceManager.get_cpu_usage()
        self.assertIsInstance(cpu_usage, float)

if __name__ == "__main__":
    unittest.main()