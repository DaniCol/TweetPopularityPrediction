import sys 
import os 
import argparse  
import json  

from kafka import KafkaProducer   # Import Kafka producder

sys.path.append(os.path.abspath("/home/tweetoscope/src/hawkes_estimator"))
from src.fake_data import create_fake_data

def publish_fake_data(args):
    '''
    Publish simulated exp hawkes cascades to a cascade_series kafka topic

    args      -- broker list (default : localhost:9092)
    '''

    # Generate simulated data 
    data = create_fake_data()

    # Init the producer
    producer = KafkaProducer(
                            bootstrap_servers = args.broker_list,                     # List of brokers passed from the command line
                            value_serializer=lambda v: json.dumps(v).encode('utf-8'), # How to serialize the value to a binary buffer
                            key_serializer=str.encode                                 # How to serialize the key
                            )

    # Send the data to the cascade_series topic
    producer.send('cascade_series', key = data[0], value = data[1])
    producer.flush()


    

# Init the parser 
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

# Add broker list to the command line arguments 
parser.add_argument('--broker-list', type=str, default="localhost:9092", help="the broker list")

# Parse arguments
args = parser.parse_args()  

# Publish data 
for i in range(100000):
    publish_fake_data(args) 