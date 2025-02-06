import unittest
from parser import FlowLogParser

class TestFlowLogParser(unittest.TestCase):
    def setUp(self):
        self.parser = FlowLogParser()

    def test_initialize(self):
        self.parser.initialize()

        self.assertIn((25, 6), self.parser.lookup_table.keys())
        self.assertIn((68, 17), self.parser.lookup_table.keys())

        self.assertEqual(self.parser.lookup_table[(25, 6)], 'sv_P1')
        self.assertEqual(self.parser.lookup_table[(68, 17)], 'sv_P2')

    def test_parse(self):
        self.parser.initialize()

        tag_counts, port_protocol_counts = self.parser.parse()

        self.assertEqual(tag_counts['sv_P1'], 2)
        self.assertEqual(tag_counts['sv_P2'], 1)
        self.assertEqual(tag_counts['email'], 3)
        self.assertEqual(tag_counts['test'], 0)
        self.assertEqual(port_protocol_counts[(25, 6)], 1)
        self.assertEqual(port_protocol_counts[(68, 17)], 0) # not present in sample flow logs



if __name__ == '__main__':
    unittest.main()