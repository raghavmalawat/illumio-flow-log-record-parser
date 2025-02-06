import unittest
from parser import FlowLogParser

class TestFlowLogParser(unittest.TestCase):
    def setUp(self):
        self.parser = FlowLogParser()

    def test_initialize(self):
        self.parser.initialize()

        self.assertIn(('25', 6), self.parser.lookup_table.keys())
        self.assertIn(('68', 17), self.parser.lookup_table.keys())

        self.assertEqual(self.parser.lookup_table[('25', 6)], 'sv_P1')
        self.assertEqual(self.parser.lookup_table[('68', 17)], 'sv_P2')


if __name__ == '__main__':
    unittest.main()