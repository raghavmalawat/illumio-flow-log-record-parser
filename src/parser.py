import sys
from collections import defaultdict

class FlowLogParser:
    def __init__(self, input_file, output_file, lookup_file):
        self.input_file = input_file
        self.output_file = output_file
        self.lookup_file = lookup_file
        self.lookup_table = {}
        self.protocol_map = {'icmp': 1, 'tcp': 6, 'udp': 17} # https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
        self.tag_counts = defaultdict(int)
        self.port_protocol_counts = defaultdict(int)

    def initialize(self):
        """
        Populate lookup table (Lookup Table Format: (dstport, protocol, tag))
        """
        try:
            with open(self.lookup_file, 'r') as f:
                for line in f:
                    dstport, protocol, tag  = line.strip().split(',')
                    self.lookup_table[(int(dstport), self.protocol_map[protocol])] = tag
        except FileNotFoundError as e:
            error_message = f"Error: The lookup file '{self.lookup_file}' was not found."
            raise FileNotFoundError(error_message) from e


    def parse(self):
        """
        Parse the the flow logs from input file and return below 2 outputs
        1. Count of Matches for Each Tag
        2. Count of Matches for Each Port/Protocol Combination
        """
        try:
            with open(self.input_file, 'r') as f:
                for line in f:
                    fields = line.strip().split(' ')
                    dstport, protocol = int(fields[6]), int(fields[7])
                    key = (dstport, protocol)

                    tag = self.lookup_table.get(key, "Untagged")

                    self.tag_counts[tag] += 1
                    self.port_protocol_counts[key] += 1
        except FileNotFoundError as e:
            error_message = f"Error: The input file '{self.input_file}' was not found."
            raise FileNotFoundError(error_message) from e
        
    def store_output(self):
        inv_protocol_map = dict((v, k) for k, v in self.protocol_map.items())

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
                    f.write(f"{port}, {inv_protocol_map[protocol]}, {count}\n")
        except IOError as e:
            error_message = f"Error: Could not write to the output file '{self.output_file}': {e}"
            raise IOError(error_message) from e

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