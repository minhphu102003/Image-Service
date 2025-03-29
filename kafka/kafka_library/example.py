import random
import time
from producer import KafkaImageProducer

image_urls = [
    "https://res.cloudinary.com/dvrisaqgy/image/upload/v1742967678/uploads/1742967677245.png",
    "https://res.cloudinary.com/dvrisaqgy/image/upload/v1742967680/uploads/1742967680234.jpg",
    "https://res.cloudinary.com/dvrisaqgy/image/upload/v1742967683/uploads/1742967683578.jpeg"
]

# Tọa độ cơ sở riêng cho từng loại báo cáo
traffic_base_coords = (108.21797196886965, 16.063749108468627)  # Kẹt xe
flood_base_coords = (108.20531565208454, 16.072981703606757)  # Lũ lụt

def generate_nearby_coordinates(base_lon, base_lat, delta=0.001):
    """Sinh tọa độ ngẫu nhiên xung quanh một điểm"""
    new_lon = base_lon + random.uniform(-delta, delta)
    new_lat = base_lat + random.uniform(-delta, delta)
    return round(new_lon, 6), round(new_lat, 6)

producer = KafkaImageProducer(topic="python-topic", group_id="traffic_group")

while True:

    traffic_longitude, traffic_latitude = generate_nearby_coordinates(*traffic_base_coords)
    producer.send_multiple_reports(image_urls, traffic_longitude, traffic_latitude, "TRAFFIC_JAM", delay=5)

    flood_longitude, flood_latitude = generate_nearby_coordinates(*flood_base_coords)
    producer.send_multiple_reports(image_urls, flood_longitude, flood_latitude, "FLOOD", delay=5)
