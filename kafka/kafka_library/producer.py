import json
import time
from config import create_kafka_producer, create_kafka_consumer
import datetime as date

class KafkaImageProducer:
    def __init__(self, topic, group_id):
        self.producer = create_kafka_producer()
        self.consumer = create_kafka_consumer(topic, group_id)
        self.topic = topic

    def send_traffic_report(self, img_url, longitude, latitude):
        data = {
            "type": "user report",
            "reportId": "67e39380aa898a66445a9135",
            "account_id": "6753c600039403e62e0be61a",
            "description": "Traffic jam",
            "typeReport": "TRAFFIC_JAM",
            "congestionLevel": "POSSIBLE_CONGESTION",
            "longitude": longitude,
            "latitude": latitude,
            "timestamp": date.datetime.now().isoformat(),
            "img": img_url
        }

        self.producer.produce(self.topic, key="traffic_image", value=json.dumps(data))
        self.producer.flush()

    def send_flood_report(self, img_url, longitude, latitude):
        """Gửi báo cáo lũ lụt"""
        data = {
            "type": "user report",
            "reportId": "67e39380aa898a66445a9135",
            "account_id": "6753c600039403e62e0be61a",
            "description": "Flooding detected",
            "typeReport": "FLOOD",
            "congestionLevel": None,
            "longitude": longitude,
            "latitude": latitude,
            "timestamp": date.datetime.now().isoformat(),
            "img": img_url
        }

        self.producer.produce(self.topic, key="flood_image", value=json.dumps(data))
        self.producer.flush()

    def send_multiple_reports(self, image_urls, longitude, latitude, report_type, delay=1):
        """Gửi nhiều ảnh báo cáo theo loại được chọn"""
        for img_url in image_urls:
            if report_type == "TRAFFIC_JAM":
                self.send_traffic_report(img_url, longitude, latitude)
            elif report_type == "FLOOD":
                self.send_flood_report(img_url, longitude, latitude)
            time.sleep(delay)
