import json
from kafka_library.config import create_kafka_consumer, create_kafka_producer
from video_processing.video_processor import VideoProcessor
from upload.uploader import Uploader
import os
from dotenv import load_dotenv

def delivery_report(err, msg):
    if err is not None:
        print(f"Lỗi khi gửi message: {err}")
    else:
        print(f"Message đã được gửi: {msg.topic()} [{msg.partition()}] @ {msg.offset()}")

def process_message(message, producer, output_topic):

    try:
        data = json.loads(message)
        load_dotenv()

        if "_id" in data:
            data["reportId"] = data["_id"]
            del data["_id"]        

        media_url = data.get("media_files", {}).get("media_url")
        
        if media_url:
            video_processor = VideoProcessor(output_folder="frames", video_path="downloaded_video.mp4")
            video_path = video_processor.download_video(media_url)
            
            frames = video_processor.extract_frames(interval=2)
            uploader = Uploader(
                service="cloudinary",
                cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
                cloud_api_key=os.getenv("CLOUDINARY_API_KEY"),
                cloud_api_secret=os.getenv("CLOUDINARY_API_SECRET")
            )
            uploaded_urls = []
            for frame in frames:
                url = uploader.upload_to_cloudinary(frame)
                uploaded_urls.append(url)
                print(f"Uploaded frame to Cloudinary: {url}")
            data["uploaded_frames"] = uploaded_urls
            print(data)
            producer.produce(output_topic, key=None, value=json.dumps(data), callback=delivery_report)
            producer.flush()                        
        else:
            print("Media URL không tồn tại trong message.")
    except json.JSONDecodeError as e:
        print(f"Lỗi khi parse JSON: {e}")
    except Exception as e:
        print(f"Lỗi khác: {e}")

def consume_messages(input_topic, group_id, output_topic):

    consumer = create_kafka_consumer(input_topic, group_id)
    producer = create_kafka_producer()

    try:
        while True:
            msg = consumer.poll(1.0) 
            if msg is None:
                continue
            if msg.error():
                print(f"Lỗi Kafka: {msg.error()}")
                continue

            message_value = msg.value().decode('utf-8')
            
            process_message(message_value, producer, output_topic)
    except KeyboardInterrupt:
        print("Dừng lắng nghe Kafka.")
    finally:
        consumer.close()