import argparse                   # To parse command line arguments
import json                       # To parse and dump JSON
import logging
import logging_loki

from kafka import KafkaConsumer   # Import Kafka consumer

def publish(logger, value):
    if value['level'] == 'DEBUG':
        logger.debug(
            msg=str(value['message']),
            extra={"tags": {"service": value['source']}},
        )
    elif value['level'] == 'INFO':
        logger.info(
            msg=str(value['message']),
            extra={"tags": {"service": value['source']}},
        )
    elif value['level'] == 'WARNING':
        logger.warning(
            msg=str(value['message']),
            extra={"tags": {"service": value['source']}},
        )
    elif value['level'] == 'ERROR':
        logger.error(
            msg=str(value['message']),
            extra={"tags": {"service": value['source']}},
        )
    elif value['level'] == 'CRITICAL':
        logger.critical(
            msg=str(value['message']),
            extra={"tags": {"service": value['source']}},
        )

def main(args):
    # Listen to the cascade_series topic 
    consumer = KafkaConsumer('logs',                                                     # Topic name
                            bootstrap_servers = args.broker_list,                        # List of brokers passed from the command line
                            value_deserializer=lambda v: json.loads(v.decode('utf-8')),  # How to deserialize the value from a binary buffer
                            )
    # Configure Loki logger
    logging_loki.emitter.LokiEmitter.level_tag = 'level'
    # Create a new logging handler
    handler = logging_loki.LokiHandler(
        url=f'http://{args.loki_url}:3100/loki/api/v1/push',
        version='1',
    )
    # Configure Python Logger
    logger = logging.getLogger('Tweetoscope')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    # Get the times series 
    for msg in consumer:                            # Blocking call waiting for a new message
        publish(logger=logger, value=msg.value)


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