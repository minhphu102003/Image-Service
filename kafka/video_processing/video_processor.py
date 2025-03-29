import cv2
import os
import requests

class VideoProcessor:
    def __init__(self, output_folder="frames"):
        self.output_folder = output_folder
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    
    def download_video(self, url, output_path="video.mp4"):
        response = requests.get(url, stream=True)
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return output_path
    
    def extract_frames(self, video_path, interval=5):
        cap = cv2.VideoCapture(video_path)
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
