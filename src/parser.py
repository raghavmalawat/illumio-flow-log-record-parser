import sys
from collections import defaultdict

class FlowLogParser:
    DEFAULT_INPUT_FILE = './static/sample_flow_logs.txt'
    DEFAULT_OUTPUT_FILE = './static/output.txt'
    DEFAULT_LOOKUP_FILE = './static/lookup.csv'
    PROTOCOL_MAP = {1: 'icmp', 6: 'tcp', 17: 'udp'} # https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml

    def __init__(self, input_file=DEFAULT_INPUT_FILE, output_file=DEFAULT_OUTPUT_FILE, lookup_file=DEFAULT_LOOKUP_FILE):
        self.input_file = input_file
        self.output_file = output_file
        self.lookup_file = lookup_file
        self.lookup_table = {}
        self.tag_counts = defaultdict(int)
        self.port_protocol_counts = defaultdict(int)

    def read_file(self, file_path):
        """Utility function to read a file and handle errors."""
        try:
            return open(file_path, 'r')
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: The file '{file_path}' was not found.")

    def initialize(self):
        """
        Populate lookup table (Lookup Table Format: (dstport, protocol, tag))
        """
        with self.read_file(self.lookup_file) as f:
            for line in f:
                dstport, protocol, tag = line.strip().split(',')
                self.lookup_table[(int(dstport), protocol.lower())] = tag

    def parse(self):
        """
        Parse the the flow logs from input file and return below 2 outputs
        1. Count of Matches for Each Tag
        2. Count of Matches for Each Port/Protocol Combination
        """
        with self.read_file(self.input_file) as f:
            for line in f:
                fields = line.strip().split(' ')
                dstport, protocol = int(fields[6]), int(fields[7])
                key = (dstport, self.PROTOCOL_MAP[protocol])

                tag = self.lookup_table.get(key, "Untagged")

                self.tag_counts[tag] += 1
                self.port_protocol_counts[key] += 1
        
    def store_output(self):
        try:
            with open(self.output_file, 'w') as f:
                f.write("Count of Matches for Each Tag\n\n")
                f.write("Tag, Count\n\n")
                for tag, count in self.tag_counts.items():
                    f.write(f"{tag}, {count}\n")
                f.write("\n\n")
                f.write("Count of Matches for Each Port/Protocol Combination\n\n")
                f.write("Port, Protocol, Count\n\n")
                for key, count in self.port_protocol_counts.items():
                    port, protocol = key
                    f.write(f"{port}, {protocol}, {count}\n")  # Use the flipped map
        except IOError as e:
            raise IOError(f"Error: Could not write to the output file '{self.output_file}': {e}")

if __name__ == '__main__':
    try:
        input_file = sys.argv[1] if len(sys.argv) > 1 else './static/sample_flow_logs.txt'
        output_file = './static/output.txt'
        lookup_file = './static/lookup.csv'

        parser = FlowLogParser(input_file, output_file, lookup_file)
        parser.initialize()
        parser.parse()
        parser.store_output()
    except FileNotFoundError as e:
        print(e)
    except IOError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")