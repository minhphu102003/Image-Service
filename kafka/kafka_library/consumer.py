import json
from kafka_library.config import create_kafka_consumer
from video_processing.video_processor import VideoProcessor

def process_message(message):

    try:
        data = json.loads(message)

        media_url = data.get("media_files", {}).get("media_url")
        
        if media_url:
            print(f"Media URL: {media_url}")
            video_processor = VideoProcessor(output_folder="frames", video_path="downloaded_video.mp4")
            video_path = video_processor.download_video(media_url)
            print(f"Video đã được tải về: {video_path}")
            
            frames = video_processor.extract_frames(interval=2)
            print(f"Frames đã được trích xuất: {frames}")
        else:
            print("Media URL không tồn tại trong message.")
    except json.JSONDecodeError as e:
        print(f"Lỗi khi parse JSON: {e}")
    except Exception as e:
        print(f"Lỗi khác: {e}")

def consume_messages(topic, group_id):

    consumer = create_kafka_consumer(topic, group_id)

    try:
        while True:
            msg = consumer.poll(1.0) 
            if msg is None:
                continue
            if msg.error():
                print(f"Lỗi Kafka: {msg.error()}")
                continue

            message_value = msg.value().decode('utf-8')
            
            process_message(message_value)
    except KeyboardInterrupt:
        print("Dừng lắng nghe Kafka.")
    finally:
        consumer.close()