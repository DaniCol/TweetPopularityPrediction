echo "create tweets topic"
$KAFKA_HOME/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --partitions 2 --config retention.ms=3600000 --topic tweets

echo "create cascade_series topic"
$KAFKA_HOME/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --partitions 1 --config retention.ms=3600000 --topic cascade_series

echo "create cascade_properties topic"
$KAFKA_HOME/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --partitions 1 --config retention.ms=3600000 --topic cascade_properties

echo "create samples topic"
$KAFKA_HOME/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --partitions 1 --config retention.ms=3600000 --topic samples

echo "create models topic"
$KAFKA_HOME/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --partitions 1 --config retention.ms=3600000 --topic models

echo "create logs topic"
$KAFKA_HOME/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --partitions 1 --config retention.ms=3600000 --topic logs
