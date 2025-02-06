import sys
from collections import defaultdict

class FlowLogParser:
    PROTOCOL_MAP = {1: 'icmp', 6: 'tcp', 17: 'udp'} # https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml

    def __init__(self, input_file,output_file, lookup_file):
        """
        Initializes the FlowLogParser with the specified input, output, and lookup files.

        Args:
            input_file (str): The path to the input flow log file.
            output_file (str): The path to the output file.
            lookup_file (str): The path to the lookup table CSV file.
        """
        self.input_file = input_file
        self.output_file = output_file
        self.lookup_file = lookup_file
        self.lookup_table = {}
        self.tag_counts = defaultdict(int)
        self.port_protocol_counts = defaultdict(int)

    def read_file(self, file_path):
        """
        Utility function to read a file and handle errors.

        Args:
            file_path (str): The path to the file to be read.

        Returns:
            file object: The opened file object.

        Raises:
            FileNotFoundError: If the specified file cannot be found.
        """
        try:
            return open(file_path, 'r')
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: The file '{file_path}' was not found.")

    def initialize(self):
        """
        Populates the lookup table from the lookup CSV file.

        The lookup table maps (dstport, protocol) tuples to tags based on the contents of the lookup file.

        Raises:
            FileNotFoundError: If the lookup file cannot be found.
        """
        with self.read_file(self.lookup_file) as f:
            for line in f:
                dstport, protocol, tag = line.strip().split(',')
                self.lookup_table[(int(dstport), protocol.lower())] = tag

    def parse(self):
        """
        Parses the flow logs from the input file.

        Counts the occurrences of each tag and the number of matches for each port/protocol combination.

        Raises:
            FileNotFoundError: If the input file cannot be found.
        """
        with self.read_file(self.input_file) as f:
            for line in f:
                fields = line.strip().split(' ')
                dstport, protocol = int(fields[6]), int(fields[7])
                key = (dstport, self.PROTOCOL_MAP[protocol])

                tag = self.lookup_table.get(key, "untagged")

                self.tag_counts[tag] += 1
                self.port_protocol_counts[key] += 1
        
    def store_output(self):
        """
        Writes the counts of tags and port/protocol combinations to the output file.

        Raises:
            IOError: If there is an issue writing to the output file.
        """
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