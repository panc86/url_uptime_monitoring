from kafka import KafkaConsumer
import json

# The consumer retrieves logs from the producer
# and creates an entry into a RDBMS
consumer = KafkaConsumer(
    'test',
    bootstrap_servers=['172.17.0.1:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group'
)

# TODO: Connect to RDBMS

# Create entries
for m in consumer:
    print(m.value)
