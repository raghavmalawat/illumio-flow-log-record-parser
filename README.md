# FLOW LOG RECORD PARSER

### What is a flow log record?
A flow log record represents a network flow in a VPC. By default, each record captures a network internet protocol (IP) traffic flow (characterized by a 5-tuple on a per network interface basis) that occurs within an aggregation interval, also referred to as a capture window.

Each record is a string with fields separated by spaces. A record includes values for the different components of the IP flow, for example, the source, destination, and protocol.

When you create a flow log, you can use the [default format](https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html#flow-logs-default) for the flow log record, or you can specify a custom format.


For more information, [check](https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html) this out
