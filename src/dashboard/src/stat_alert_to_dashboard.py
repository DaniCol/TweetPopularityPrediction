import argparse                   # To parse command line arguments
import json                       # To parse and dump JSON
import time

from collections import deque
from prometheus_client import Gauge, start_http_server
from kafka import KafkaConsumer   # Import Kafka consumer


class Stats:
    def __init__(self) -> None:
        self.ares = Gauge('ares', 'Absolute relative error', ["time_window", "type"])

    def handle_stat_msg(self, value):
        self.ares.labels(time_window=value['T_obs'], type='ARE_RF').set(value['ARE_RF'])
        self.ares.labels(time_window=value['T_obs'], type='ARE').set(value['ARE'])


class Alerts:
    def __init__(self, max_time=120) -> None:
        self.max_time = max_time
        self.n_supps = Gauge('n_supp', 'Predicted n_supp', ["time_window", "level"])
        self.tweet_id = Gauge('tweet_id', 'Tweet ID', ["time_window", "level"])
        
        self.time_windows = {}
        self.queue = deque()
        self.ordered_tweet = {}

    def handle_alert_msg(self, time_window, value):
        if time_window not in self.time_windows.keys():
            self.add_time_window(time_window)
        # Generate tweet msg
        tweet = {
            "tweet_id": value["cid"],
            "n_supp": value['n_supp_rf'],
            "time": time.time()
        }
        
        # Add tweet to the queue
        self.time_windows[time_window]['queue'].append(tweet)

        # Add tweet the the dict and ordered it
        self.time_windows[time_window]['ordered_tweet'][tweet['tweet_id']] = {
            "n_supp": tweet['n_supp'],
            'time': tweet['time']
        }
        self.time_windows[time_window]['ordered_tweet'] = dict(
            sorted(
                self.time_windows[time_window]['ordered_tweet'].items(),
                key=lambda item: item[1]['n_supp'],
                reverse=True
                )
            )
        
        # Look if tweet is too old
        current_time = time.time()
        while len(self.time_windows[time_window]['queue'])>0 and current_time - self.time_windows[time_window]['queue'][0]['time'] > self.max_time:
            elem = self.time_windows[time_window]['queue'].popleft()
            # print(elem)
            del self.time_windows[time_window]['ordered_tweet'][elem['tweet_id']]
            print('pop')

        # Update Gauge
        for i in range(5):
            try:
                n_supp_val = list(self.time_windows[time_window]['ordered_tweet'].values())[i]['n_supp']
                tweet_id_val = list(self.time_windows[time_window]['ordered_tweet'].keys())[i]
            except IndexError:
                n_supp_val = 0
                tweet_id_val = 0
            self.n_supps.labels(time_window=time_window, level=str(i+1)).set(n_supp_val)
            self.tweet_id.labels(time_window=time_window, level=str(i+1)).set(tweet_id_val)

    def add_time_window(self, time_window):
        self.time_windows[time_window] = {
            'queue': deque(),
            'ordered_tweet': {}
        }

def main(args):
    # Listen to the cascade_series topic 
    consumer = KafkaConsumer(bootstrap_servers = args.broker_list,                       # List of brokers passed from the command line
                            value_deserializer=lambda v: json.loads(v.decode('utf-8')),  # How to deserialize the value from a binary buffer
                            )
    consumer.subscribe(['alert', 'stat'])
    start_http_server(8000)
    stats_handler = Stats()
    alerts_handler = Alerts()
    # Get the times series 
    for msg in consumer: 
        # Manage Learner messages
        if msg.topic == 'alert':
            alerts_handler.handle_alert_msg(value=msg.value, time_window=msg.value['T_obs'])

        # Manage cascade properties messages
        elif msg.topic == 'stat':
            stats_handler.handle_stat_msg(value=msg.value)

if __name__ == "__main__":
    # Init the parser 
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--broker-list', type=str,
                        help="The broker list. It could be either \n"
                        " - a filepath : containing a comma separated list"
                        " of brokers\n"
                        " - a comma separated list of brokers, e.g. "
                        " localhost:9091,localhost:9092\n",
                        required=True)
    parser.add_argument('--loki-url', type=str,
                        default="localhost",
                        help="Loki url. If could be either \n"
                        " - localhost : if your are running every thing"
                        " on your machine \n"
                        " - loki : the name of the service in Docker or"
                        " Kubernetes\n")

    # Parse arguments
    args = parser.parse_args()  

    # Start the main loop 
    main(args)