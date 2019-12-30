import unittest
import sys
sys.path.extend(['.', '../'])

from tests.test_pick_move import TestBasicSafety, TestAdvancedSafety
from tests.test_path_finding import TestPathFinding

if __name__ == "__main__":
    unittest.main()