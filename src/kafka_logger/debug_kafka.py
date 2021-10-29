import argparse                   # To parse command line arguments
import json                       # To parse and dump JSON
import sys
from kafka import KafkaConsumer   # Import Kafka consumer

default_broker_list = "localhost:9091,localhost:9092"
default_log_topic = "cascade_properties"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)
    parser.add_argument('--broker-list', type=str,
                        help="The broker list. It could be either \n"
                        " - a filepath : containing a comma separated list"
                        " of brokers\n"
                        " - a comma separated list of brokers, e.g. "
                        " localhost:9091,localhost:9092\n",
                        required=True)
    parser.add_argument('--logs_topic', type=str,
                        default=default_log_topic,
                        help='The topic for listening to logs')
    args = parser.parse_args()
    
    consumer = KafkaConsumer(args.logs_topic,
                             auto_offset_reset='latest',
                             bootstrap_servers=args.broker_list,
                             value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                             key_deserializer= lambda v: v.decode())

    try:
        for msg in consumer:
            print (f"msg: ({msg.key}, {msg.value})")
    except KeyboardInterrupt:
        sys.exit()
