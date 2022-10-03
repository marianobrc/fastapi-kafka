import json
import time
from kafka import KafkaProducer, errors
from fastapi import FastAPI
from models import Location


# Connect to kafka broker
def connect_to_broker(broker_url: str):
    connected = False
    kafka_producer = None
    while not connected:
        try:
            print("Connecting to the broker..")
            kafka_producer = KafkaProducer(
                bootstrap_servers=[broker_url],
                value_serializer=lambda m: json.dumps(m).encode('utf-8'),
                retries=3
            )
        except errors.NoBrokersAvailable:
            print("Broker not available.")
            time.sleep(1)  # Retry 1 second later
        else:
            print("Connected.")
            connected = True
    return kafka_producer


producer = connect_to_broker('kafka-broker-local:9092')
app = FastAPI()


@app.get("/status/")
async def root():
    return {"status": "ok"}


@app.put("/locations/")
async def send_location(loc: Location):
    print("Sending a message..")
    message_dict = loc.dict(exclude_unset=True)
    producer.send(
        topic='geo-locations',
        value=message_dict
    )
    print("Message sent successfully.")
    return {"status": "Location sent successfully"}

