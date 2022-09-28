import json
from kafka import KafkaProducer
from fastapi import FastAPI
from models import Location


# produce json messages
print("Connecting to the broker..")
producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda m: json.dumps(m).encode('utf-8')
)

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

