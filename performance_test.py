import timeit
from src.parser import FlowLogParser

def run_parser():
    parser = FlowLogParser('./static/performance_test_flow_logs.txt', './static/performance_output.txt', './static/lookup.csv', log_skipped=False)
    parser.initialize()
    parser.parse()
    parser.store_output()

if __name__ == '__main__':
    execution_time = timeit.timeit(run_parser, number=1)  # Run the parser once
    print(f"Execution time: {execution_time * 1000:.2f} milliseconds")  # Convert to milliseconds