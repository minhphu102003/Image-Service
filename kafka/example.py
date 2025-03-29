import os
from video_processing.video_processor import VideoProcessor

def test_video_processing(video_url, output_folder):
    processor = VideoProcessor(output_folder=output_folder)

    video_path = processor.download_video(url=video_url, output_path="test_video.mp4")
    assert os.path.exists(video_path),  "Video không được tải thành công!"

    frames = processor.extract_frames(video_path=video_path, interval=5)
    assert len(frames) > 0, " Không có frame nào được trích xuất!"

    for frame in frames:
        assert os.path.exists(frame), f"Frame {frame} không tồn tại!"

if __name__ == "__main__":
    VIDEO_URL = "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
    OUTPUT_FOLDER = "test_frames"
    test_video_processing(video_url=VIDEO_URL, output_folder= OUTPUT_FOLDER)
