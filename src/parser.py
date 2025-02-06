from collections import defaultdict

class FlowLogParser:
    def __init__(self):
        self.input_file = './static/sample_flow_logs.txt'
        self.output_file = './output.txt'
        self.lookup_file = './static/lookup.csv'
        self.lookup_table = {}
        self.sample_flow_logs = []
        self.protocol_map = {'icmp': 1, 'tcp': 6, 'udp': 17} # https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml

    def initialize(self):
        """
        Populate lookup table (Lookup Table Format: (dstport, protocol, tag))
        """

        with open(self.lookup_file, 'r') as f:
            for line in f:
                dstport, protocol, tag  = line.strip().split(',')
                self.lookup_table[(int(dstport), self.protocol_map[protocol])] = tag

    def parse(self):
        """
        Parse the the flow logs from input file and return below 2 outputs
        1. Count of Matches for Each Tag
        2. Count of Matches for Each Port/Protocol Combination
        """

        tag_counts = defaultdict(int)
        port_protocol_counts = defaultdict(int)

        with open(self.input_file, 'r') as f:
            for line in f:
                fields = line.strip().split(' ')
                dstport, protocol = int(fields[6]), int(fields[7])
                key = (dstport, protocol)

                tag = self.lookup_table.get(key, "Untagged")

                tag_counts[tag] += 1
                port_protocol_counts[key] += 1
        
        return tag_counts, port_protocol_counts


if __name__ == '__main__':
    parser = FlowLogParser()

    parser.initialize()
    tag_counts, port_protocol_counts = parser.parse()

    # parser.store_output()
    