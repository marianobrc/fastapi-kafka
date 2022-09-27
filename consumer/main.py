import json
from kafka import KafkaConsumer


# produce json messages
print("Connecting to the broker..")
consumer = KafkaConsumer(
    'geo-locations',  # Topic
    bootstrap_servers=['kafka:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='location-consumers',
)
print("Consuming messages..")
for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                         message.offset, message.key,
                                         message.value))
print("No more messages.")
