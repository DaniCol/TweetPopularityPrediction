import argparse                   # To parse command line arguments
import configparser
import json                       # To parse and dump JSON
import pickle

import os 

from collections import OrderedDict
from kafka import KafkaConsumer   # Import Kafka consumer
from kafka import KafkaProducer   # Import Kafka producder

from src.predictor import Predictor

class MessageHandler:
    def __init__(self) -> None:
        pass
    @staticmethod
    def deserializer(v):
        try:
            return json.loads(v.decode('utf-8'))
        except UnicodeDecodeError:
            return pickle.loads(v)

def main(args):

    # Listen to the cascade_series topic 
    consumer = KafkaConsumer(bootstrap_servers = args.broker_list,                       # List of brokers passed from the command line
                            group_id='producer',
                            value_deserializer=lambda v: MessageHandler.deserializer(v), # How to deserialize the value from a binary buffer
                            key_deserializer= lambda v: v.decode()                       # How to deserialize the key (if any)
                            )
    # Subscribe to topics
    consumer.subscribe(['cascade_properties', 'models'])

    # Init the producer
    producer = KafkaProducer(
                            bootstrap_servers = args.broker_list,                     # List of brokers passed from the command line
                            value_serializer=lambda v: json.dumps(v).encode('utf-8'), # How to serialize the value to a binary buffer
                            key_serializer=str.encode                                 # How to serialize the key
                            )
    
    # Log producer
    producer_log = KafkaProducer(
                            bootstrap_servers = args.broker_list,                     # List of brokers passed from the command line
                            value_serializer=lambda v: json.dumps(v).encode('utf-8'), # How to serialize the value to a binary buffer
                            )

    # Create the dictionary that will store every estimators
    # One for each time window
    predictor = Predictor(producer=producer, producer_log=producer_log)

    # Get the times series 
    for msg in consumer:                            # Blocking call waiting for a new message
        # print (f"msg: ({msg.key}, {msg.value})")    # Write key and payload of the received message
        
        # Manage Learner messages
        if msg.topic == 'models':
            predictor.handle_model_msg(time_window=msg.key, value=msg.value)

        # Manage cascade properties messages
        elif msg.topic == 'cascade_properties':
            predictor.handle_properties_msg(time_window=msg.key, value=msg.value)

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

