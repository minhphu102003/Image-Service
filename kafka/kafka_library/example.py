import random
import math
import time
from producer import KafkaImageProducer

image_urls = [
    "https://baogiaothong.mediacdn.vn/files/news/2018/11/26/110331-46983782_1134274046740095_1180441090944139264_n.jpg",
    "https://baogiaothong.mediacdn.vn/files/news/2018/11/26/110331-46983782_1134274046740095_1180441090944139264_n.jpg",
    "https://baogiaothong.mediacdn.vn/files/news/2018/11/26/110331-46983782_1134274046740095_1180441090944139264_n.jpg"
]

# Tọa độ cơ sở riêng cho từng loại báo cáo
traffic_base_coords = (108.21797196886965, 16.063749108468627)  # Kẹt xe
flood_base_coords = (108.20531565208454, 16.072981703606757)  # Lũ lụt

def generate_nearby_coordinates(base_lon, base_lat, delta=0.01):
    distance = random.uniform(0, delta)
    angle = random.uniform(0, 2 * math.pi)

    # Đổi sang toạ độ Cartesian
    dlon = distance * math.cos(angle)
    dlat = distance * math.sin(angle)

    new_lon = base_lon + dlon
    new_lat = base_lat + dlat
    return round(new_lon, 6), round(new_lat, 6)

producer = KafkaImageProducer(topic="python-topic", group_id="traffic_group")

while True:

    traffic_longitude, traffic_latitude = generate_nearby_coordinates(*traffic_base_coords)
    producer.send_multiple_reports(image_urls, traffic_longitude, traffic_latitude, "TRAFFIC_JAM", delay=5)

    flood_longitude, flood_latitude = generate_nearby_coordinates(*flood_base_coords)
    producer.send_multiple_reports(image_urls, flood_longitude, flood_latitude, "FLOOD", delay=5)
