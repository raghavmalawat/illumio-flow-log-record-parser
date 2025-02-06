

class FlowLogParser:
    def __init__(self):
        self.input_file = './static/sample_flow_logs.txt'
        self.output_file = './output.txt'
        self.lookup_file = './static/lookup.csv'
        self.lookup_table = {}
        self.sample_flow_logs = []
        self.protocol_map = {'icmp': 1, 'tcp': 6, 'udp': 17} # https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml

    def initialize(self):
        #Populate lookup table
        # Format: dstport, protocol, tag 

        with open(self.lookup_file, 'r') as f:
            for line in f:
                dstport, protocol, tag  = line.strip().split(',')
                self.lookup_table[(dstport, self.protocol_map[protocol])] = tag




if __name__ == '__main__':
    parser = FlowLogParser()

    parser.initialize()
    print(parser.lookup_table)
    # parser.parse()
    # parser.store_output()
    