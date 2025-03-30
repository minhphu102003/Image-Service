import cv2
import os
import requests

class VideoProcessor:
    def __init__(self, output_folder="frames", video_path="video.mp4"):
        self.output_folder = output_folder
        self.video_path = video_path
        self._clear_storage()
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    
    def _clear_storage(self):
        if os.path.exists(self.video_path):
            os.remove(self.video_path)
        if os.path.exists(self.output_folder):
            for file in os.listdir(self.output_folder):
                file_path = os.path.join(self.output_folder, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
    
    def download_video(self, url):
        response = requests.get(url, stream=True)
        with open(self.video_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return self.video_path
    
    def extract_frames(self, interval=5):
        cap = cv2.VideoCapture(self.video_path)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_interval = fps * interval
        frame_count = 0
        saved_count = 0
        frames = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if frame_count % frame_interval == 0:
                frame_path = os.path.join(self.output_folder, f"frame_{saved_count}.jpg")
                cv2.imwrite(frame_path, frame)
                frames.append(frame_path)
                saved_count += 1
            frame_count += 1
        cap.release()
        return frames
