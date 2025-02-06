# FLOW LOG RECORD PARSER

### What is a flow log record?
A flow log record represents a network flow in a VPC. By default, each record captures a network internet protocol (IP) traffic flow (characterized by a 5-tuple on a per network interface basis) that occurs within an aggregation interval, also referred to as a capture window.

Each record is a string with fields separated by spaces. A record includes values for the different components of the IP flow, for example, the source, destination, and protocol.

When you create a flow log, you can use the [default format](https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html#flow-logs-default) for the flow log record, or you can specify a custom format.


For more information, [check](https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html) this out


### Task 

Write a program that can parse a file containing [flow log data](./static/sample_flow_logs.txt) and maps each row to a `tag` based on a [lookup table](./static/lookup_table.csv) (The `dstport` and `protocol` combination decide what `tag` can be applied)

### Installation
- Git clone the repo
- Go to source directory and run the parser as suggested below
    ```
    $ python3 src/parser.py             # to use the default input file ./static/sample_flow_logs.txt
    
    # to use the input file ./static/sample_flow_logs.txt
    $ python3 src/parser.py ./static/sample_flow_logs.txt 
    
    $ python3 src/test_parser.py        # to run the tests
    ```
- The output can be found in the `./static/output.txt` file
- In order to update inputs, either create a new file and pass it as an argument while running the parser or update the existing default file (`./static/sample_flow_logs.txt`)

### Testing
1. Unit tests (Followed Test Driven Development)


#### Expected Outputs

<ins>Count of Matches for Each Tag</ins>

| Tag      | Count |
|----------|-------|
| sv_P2    | 1     |
| sv_P1    | 2     |
| sv_P4    | 1     |
| email    | 3     |
| Untagged | 9     |

<ins>Count of Matches for Each Port/Protocol Combination</ins>

| Port  | Protocol | Count |
|-------|----------|-------|
| 22    | tcp      | 1     |
| 23    | tcp      | 1     |
| 25    | tcp      | 1     |
| 110   | tcp      | 1     |
| 143   | tcp      | 1     |
| 443   | tcp      | 1     |
| 993   | tcp      | 1     |
| 1024  | tcp      | 1     |
| 49158 | tcp      | 1     |
| 80    | tcp      | 1     |


### Analysis
Next set of features that can be added:

1. Error Handling (Files I/O, Unmacthed Protocols, Tags, etc)
2. Better logging for debugging
3. Pass input, output files as arguments via terminal
4. Add all protocol numbers to the map instead of hard coding (https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml)
5. Add support for custom flow log format
6. Build a simple UI using Streamlit
7. Using Locust to load test for the below constraints

### Assumptions
1. The flow logs are of deafult type (v2) and have all the mandatory 14 fields and [in order](https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html#flow-logs-fields`
2. The input file has only the `{'icmp': 1, 'tcp': 6, 'udp': 17}` protocols
3. This parser is not supported for custom flow log format
4. When wrong protocol codes are passed `OR` When a flow log doesn't follow the default format (v2)
    - We don't abort the execution. Instead, we just ignore that record and log it, while incrementing the `skipped` tag count (check `output.txt` and terminal output)
### Constraints

- Input file as well as the file containing tag mappings are plain text (ascii) files  
- The flow log file size can be up to `10 MB`
- The lookup file can have up to `10000` mappings 
- The tags can map to more than one port, protocol combinations.  for e.g. `sv_P1` and `sv_P2` as shown in the [sample lookup table](./static/lookup_table.csv). 
- The matches should be case insensitive 
