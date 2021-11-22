import numpy as np
import argparse                   # To parse command line arguments
import json                       # To parse and dump JSON
import pickle
import sys 
import os 
import time

from kafka import KafkaConsumer   # Import Kafka consumer
from kafka import KafkaProducer   # Import Kafka producder

sys.path.append(os.path.abspath("/home/tweetoscope/src/learner"))
from estimator import Estimator


def main(args):
    # Listen to the cascade_series topic 
    consumer = KafkaConsumer('samples',                                                  # Topic name
                            bootstrap_servers = args.broker_list,                        # List of brokers passed from the command line
                            group_id='learner',
                            value_deserializer=lambda v: json.loads(v.decode('utf-8')),  # How to deserialize the value from a binary buffer
                            key_deserializer= lambda v: v.decode()                       # How to deserialize the key (if any)
                            )

    # Init the producer
    producer = KafkaProducer(
                            bootstrap_servers = args.broker_list,                     # List of brokers passed from the command line
                            value_serializer=lambda v: pickle.dumps(v),               # How to serialize the value to a binary buffer
                            key_serializer=str.encode                                 # How to serialize the key
                            )

    # Log producer
    producer_log = KafkaProducer(
                            bootstrap_servers = args.broker_list,                     # List of brokers passed from the command line
                            value_serializer=lambda v: json.dumps(v).encode('utf-8'), # How to serialize the value to a binary buffer
                            )

    # Create the dictionary that will store every estimators
    # One for each time window
    estimators_collection = {}

    # Get the times series 
    for msg in consumer:                            # Blocking call waiting for a new message
        # print (f"msg: ({msg.key}, {msg.value})")    # Write key and payload of the received message

        if msg.key not in estimators_collection.keys():
            estimators_collection[msg.key] = Estimator(key=msg.key, value=msg.value, producer_log=producer_log)

        has_been_fit = estimators_collection[msg.key].handle(msg.value)

        if has_been_fit:
            producer.send('models', key = msg.key, value = estimators_collection[msg.key].estimator)

            # Send log DEBUG : msg send to cascade_properties
            producer_log.send(
                topic='logs',
                value={
                    't': time.time(),
                    'level': 'DEBUG',
                    'source': 'learner',
                    'message': f'Model sent -> {"{"}Time window : {msg.key : >5}{"}"}'
                }
            )

    producer.flush() # Flush: force purging intermediate buffers before leaving

if __name__ == "__main__":
    # Init the parser 
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    # Add broker list to the command line arguments 
    parser.add_argument('--broker-list', type=str, required=True, help="the broker list")

    # Parse arguments
    args = parser.parse_args()  

    # Start the main loop 
    main(args)
