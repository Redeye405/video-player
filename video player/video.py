import cv2
import numpy as np
import os
import time
import sys

def frame_to_ascii(frame, width, height):

    frame = cv2.resize(frame, (width, height))
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    ascii_chars = " .:-=+*#@%&/|()[]"

    num_chars = len(ascii_chars)
    
    intensity = gray / 255.0 * (num_chars - 1)
    intensity = intensity.astype(int)
    
    ascii_frame = ""
    for i in range(height):
        for j in range(width):
            char = ascii_chars[intensity[i, j]]
            ascii_frame += char
        ascii_frame += "\n"
    return ascii_frame

def play_video_in_ascii(video_path, width=100, height=47, skip_factor=1.0):

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30.0
    max_fps = 30.0
    base_frame_time = 1.0 / min(fps, max_fps)
    
    effective_frame_time = base_frame_time * skip_factor
    
    try:
        last_frame_time = time.time()
        frame_count = 0
        while cap.isOpened():
    
            ret, frame = cap.read()
            if not ret:
                break 
            ascii_frame = frame_to_ascii(frame, width, height)
            os.system('cls' if os.name == 'nt' else 'clear')
            sys.stdout.write(ascii_frame)
            sys.stdout.flush()

            elapsed = time.time() - last_frame_time
            sleep_time = max(0, effective_frame_time - elapsed)
            time.sleep(sleep_time)
            last_frame_time = time.time()

            while time.time() - last_frame_time > effective_frame_time * 2:
                ret, _ = cap.read()
                if not ret:
                    break
                last_frame_time += effective_frame_time
                frame_count += 1

            frame_count += 1

    except KeyboardInterrupt:
        print(f"\nPlayback interrupted by user. Processed {frame_count} frames.")
    finally:
        cap.release()

if __name__ == "__main__":


    # Path to the video file
    video_path = r"C:\Users\Tharindu\Downloads\video3.mp4"
    # Manually set width, height, and skip_factor here
    play_video_in_ascii(video_path, width=158, height=36, skip_factor=2.0)  # Your size with faster playback