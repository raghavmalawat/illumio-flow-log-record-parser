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
        self.parser.parse()

        tag_counts = self.parser.tag_counts
        port_protocol_counts = self.parser.port_protocol_counts

        self.assertEqual(tag_counts['sv_P1'], 2)
        self.assertEqual(tag_counts['sv_P2'], 1)
        self.assertEqual(tag_counts['email'], 3)
        self.assertEqual(tag_counts['test'], 0)
        self.assertEqual(port_protocol_counts[(25, 6)], 1)
        self.assertEqual(port_protocol_counts[(68, 17)], 0) # not present in sample flow logs

    def test_store_output(self):
        self.parser.initialize()
        self.parser.parse()

        self.parser.store_output()

        with open(self.parser.output_file, 'r') as f:
            content = f.read()
            self.assertIn("Count of Matches for Each Tag", content)
            self.assertIn("Untagged, 8", content)
            self.assertIn("email, 3", content)
            self.assertNotIn("sv_P1, 3", content)

            self.assertIn("Count of Matches for Each Port/Protocol Combination", content)
            self.assertIn("49153, tcp, 1", content)
            self.assertIn("80, tcp, 1", content)
            self.assertIn("25, tcp, 1", content)
            self.assertNotIn("25, udp, 1", content)


if __name__ == '__main__':
    unittest.main()