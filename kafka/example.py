import os
from video_processing.video_processor import VideoProcessor
from upload.uploader import Uploader
from dotenv import load_dotenv

def test_video_processing(video_url, output_folder):
    processor = VideoProcessor(output_folder=output_folder, video_path="test_video.mp4")

    video_path = processor.download_video(url=video_url)
    assert os.path.exists(video_path), "Video không được tải thành công!"

    frames = processor.extract_frames(interval=5)
    assert len(frames) > 0, "Không có frame nào được trích xuất!"

    for frame in frames:
        assert os.path.exists(frame), f"Frame {frame} không tồn tại!"
    
    return frames

def test_upload(frames, service="cloudinary"):
    load_dotenv()
    
    uploader = Uploader(service=service, cloud_name= os.getenv("CLOUDINARY_CLOUD_NAME"), cloud_api_key= os.getenv("CLOUDINARY_API_KEY"),cloud_api_secret= os.getenv("CLOUDINARY_API_SECRET"))
    uploaded_urls = []
    
    for file_path in frames:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} không tồn tại!")
        
        if service == "s3":
            url = uploader.upload_to_s3(file_path)
        elif service == "cloudinary":
            url = uploader.upload_to_cloudinary(file_path)
        else:
            raise ValueError("Dịch vụ upload không được hỗ trợ!")
        
        assert url.startswith("http"), f"Upload không thành công, URL nhận được: {url}"
        uploaded_urls.append(url)
    
    return uploaded_urls

if __name__ == "__main__":
    VIDEO_URL = "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
    OUTPUT_FOLDER = "test_frames"

    frames = test_video_processing(video_url=VIDEO_URL, output_folder=OUTPUT_FOLDER)
    print(f"Extracted {len(frames)} frames.")
    
    uploaded_urls = test_upload(frames, service="cloudinary")
    print("Uploaded frames:", uploaded_urls)
