import unittest
from parser import FlowLogParser
from unittest.mock import patch, mock_open

class TestFlowLogParser(unittest.TestCase):
    def setUp(self):
        input_file = './static/sample_flow_logs.txt'
        output_file = './static/output.txt'
        lookup_file = './static/lookup.csv'
        self.parser = FlowLogParser(input_file, output_file, lookup_file)

    def test_initialize(self):
        self.parser.initialize()

        self.assertIn((25, 'tcp'), self.parser.lookup_table.keys())
        self.assertIn((68, 'udp'), self.parser.lookup_table.keys())

        self.assertEqual(self.parser.lookup_table[(25, 'tcp')], 'sv_P1')
        self.assertEqual(self.parser.lookup_table[(68, 'udp')], 'sv_P2')
    
    def test_initialize_file_not_found(self):
        lookup_file = './static/missing_file.txt'
        parser = FlowLogParser('', '', lookup_file)
        with self.assertRaises(FileNotFoundError) as context:
            parser.initialize()
        self.assertEqual(str(context.exception), f"Error: The file '{lookup_file}' was not found.")


    def test_parse(self):
        self.parser.initialize()
        self.parser.parse()

        tag_counts = self.parser.tag_counts
        port_protocol_counts = self.parser.port_protocol_counts

        self.assertEqual(tag_counts['sv_P1'], 2)
        self.assertEqual(tag_counts['sv_P2'], 1)
        self.assertEqual(tag_counts['email'], 3)
        self.assertEqual(tag_counts['test'], 0)
        self.assertEqual(port_protocol_counts[(25, 'tcp')], 1)
        self.assertEqual(port_protocol_counts[(68, 'udp')], 0) # not present in sample flow logs

    def test_parse_file_not_found(self):
        lookup_file = './static/lookup.csv'
        parser = FlowLogParser('./static/missing_input.txt', '', lookup_file)
        parser.initialize()

        with self.assertRaises(FileNotFoundError) as context:
            parser.initialize()
            parser.parse()
        
        self.assertEqual(str(context.exception), f"Error: The file '{parser.input_file}' was not found.")

    def test_store_output(self):
        self.parser.initialize()
        self.parser.parse()

        self.parser.store_output()

        with open(self.parser.output_file, 'r') as f:
            content = f.read()
            self.assertIn("Count of Matches for Each Tag", content)
            self.assertIn("untagged, 8", content)
            self.assertIn("email, 3", content)
            self.assertNotIn("sv_P1, 3", content)

            self.assertIn("Count of Matches for Each Port/Protocol Combination", content)
            self.assertIn("49153, tcp, 1", content)
            self.assertIn("80, tcp, 1", content)
            self.assertIn("25, tcp, 1", content)
            self.assertNotIn("25, udp, 1", content)
    
    def test_store_output_write_error(self):
        self.parser.tag_counts = {'sv_P1': 2}
        self.parser.port_protocol_counts = {(25, 'tcp'): 2}
        
        with patch('builtins.open', new_callable=mock_open) as mock_file:
            mock_file.side_effect = IOError("File write error")
            with self.assertRaises(IOError) as context:
                self.parser.store_output()
            
            self.assertEqual(str(context.exception), "Error: Could not write to the output file './static/output.txt': File write error")


if __name__ == '__main__':
    unittest.main()