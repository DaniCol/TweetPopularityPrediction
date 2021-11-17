import random as rd
from time import time
import numpy as np
import sys 
import os 
import argparse  
import json  

from kafka import KafkaProducer   # Import Kafka producder


def main(args):
    # Init the producer
    producer = KafkaProducer(
                            bootstrap_servers = args.broker_list,                     # List of brokers passed from the command line
                            value_serializer=lambda v: json.dumps(v).encode('utf-8'), # How to serialize the value to a binary buffer
                            key_serializer=str.encode                                 # How to serialize the key
                            )

    n_obs = {
    600: 30,
    1200: 52,
    1800: 65,
    2400: 71
    }

    stage = {1: [1, 2, 3, 4, 5], 2: [6, 7, 8, 9, 10]}

    for i in stage.keys():
        for time_window in [600, 1200, 1800, 2400]:
            for cid in stage[i]:
                value = { 
                    'type': 'parameters',
                    'cid': cid,
                    'msg' : 'blah blah',
                    'n_obs': n_obs[time_window],
                    'params': [124.312, np.random.random(), 72]
                }
                print(f'publish_parameter : time_window : {time_window}, cid {cid}')
                producer.send('cascade_properties', key = str(time_window), value = value)

        for cid in stage[i]:
            for time_window in [600, 1200, 1800, 2400]:
                value = { 
                    'type': 'size',
                    'cid': cid,
                    'n_tot': 127,
                    't_end': 4329
                }
                print(f'publish_size : time_window : {time_window}, cid {cid}')
                producer.send('cascade_properties', key = str(time_window), value = value)

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