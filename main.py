import os
import time
import pandas as pd
from datetime import datetime, timedelta
import json
import pytz
from datetime import timezone

from config import TAG_PAIRS, FETCH_INTERVAL, API_KEY
from fetcher import fetch_sensor_data

from logger_config import setup_logger

import asyncio
from avassa_client import approle_login
from avassa_client.volga import Producer, Topic, CreateOptions

role_id = os.getenv("ROLE_ID")
secret_id = os.getenv("SECRET_ID")
topic_name = os.getenv("VOLGA_TOPIC")

class VolgaPublisher:
    def __init__(self, role_id, secret_id, topic_name):
        self.role_id = role_id
        self.secret_id = secret_id
        self.topic_name = topic_name
        self.session = None
        self.producer = None

    async def setup(self):
        self.session = approle_login(
            host='https://api.internal:4646',
            role_id=self.role_id,
            secret_id=self.secret_id
        )
        topic = Topic.local(self.topic_name)
        opts = CreateOptions.create(fmt='json', persistence='disk', replication_factor=1)
        self.producer = await Producer(
            session=self.session,
            topic=topic,
            producer_name="inline-anomaly-publisher",
            on_no_exists=opts
        ).__aenter__()

    async def publish(self, payload_dict):
        await self.producer.produce(payload_dict)
        logger.info(f"Published to Volga: {payload_dict}")



logger = setup_logger(__name__)

BUFFER_HOURS = int(os.getenv("BUFFER_HOURS", 4))

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

def publish_sensor_data(data):
    loop.run_until_complete(volga_publisher.publish(data))


def main():
    global volga_publisher
    volga_publisher = VolgaPublisher(role_id, secret_id, topic_name)
    loop.run_until_complete(volga_publisher.setup())

    while True:

        logger.info("Fetching and processing data...")

        cutoff_time = pd.Timestamp.now(tz="Europe/Stockholm") - timedelta(hours=BUFFER_HOURS)

        for tag in TAG_PAIRS:
            data = fetch_sensor_data(tag, API_KEY, window_minutes=BUFFER_HOURS * 60)
            
            publish_sensor_data(json.dumps(data))
            logger.info(f"Published data for tag: {tag}")

        time.sleep(FETCH_INTERVAL)

if __name__ == "__main__":
    main()