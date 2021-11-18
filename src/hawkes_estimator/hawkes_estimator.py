import numpy as np
import scipy.optimize as optim
import argparse                   # To parse command line arguments
import json                       # To parse and dump JSON

from kafka import KafkaConsumer   # Import Kafka consumer
from kafka import KafkaProducer   # Import Kafka producder

from src.map import compute_MAP
from src.prediction import prediction


def main(args):
    # Listen to the cascade_series topic 
    consumer = KafkaConsumer('cascade_series',                                           # Topic name
                            bootstrap_servers = args.broker_list,                        # List of brokers passed from the command line
                            value_deserializer=lambda v: json.loads(v.decode('utf-8')),  # How to deserialize the value from a binary buffer
                            )

    # Init the producer
    producer = KafkaProducer(
                            bootstrap_servers = args.broker_list,                     # List of brokers passed from the command line
                            value_serializer=lambda v: json.dumps(v).encode('utf-8'), # How to serialize the value to a binary buffer
                            key_serializer=str.encode                                 # How to serialize the key
                            )

    # Get the times series 
    for msg in consumer:                            # Blocking call waiting for a new message
        print (f"msg: ({msg.key}, {msg.value})")    # Write key and payload of the received message

        # Get the data (here the key of the message is None so we don't care about it)
        _ , v = msg.key, msg.value

        # Get the history : [(t1,m1), (t2,m2), ....] --> np.array(n,2)
        history = np.array(v['tweets'])
        history[:,0] -= history[0,0]

        # Get the current time (end of the observation window)
        t = v['T_obs']

        # Init the parameters of the estimator
        alpha, mu = 2.4, 10

        # Compute the parameters of the cascade 
        f, params = compute_MAP(history, t, alpha, mu)

        # Predict the number of retweet with the estimated parameters
        _, G1, n_star = prediction(params, history, alpha, mu, t)

        # Build the message to send to the Kafka Topic
        value = {
            'type': 'parameters',
            'cid': v['cid'],
            'msg' : v['msg'],
            'n_obs': history.shape[0],
            'params': [params[1], n_star, G1]
        }

        # Send the message to the 'cascade_properties' topic 
        producer.send('cascade_properties', key = str(t), value = value)

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