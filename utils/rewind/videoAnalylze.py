import os
import cv2
from datetime import datetime
from utils.rewind.fileHelper import get_video_file_and_start_end_time

rewindDir = os.path.dirname(os.path.realpath(__file__))

# Get the target frame number
def get_target_video_frame(video_file_path, target_date, start_time, end_time):
  video_duration = (end_time - start_time).total_seconds()
  cap = cv2.VideoCapture(video_file_path)
  frame_num = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

  target_frame = int((frame_num /video_duration) * (datetime.strptime(target_date, "%Y-%m-%d %H:%M:%S") - start_time).total_seconds())

  return target_frame

# Show the screen shot of target frame
def show_image_target_frame(video_file_path,file_name,target_frame):
  cap = cv2.VideoCapture(video_file_path)
  cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
  ret, frame = cap.read()

  screenshot_filename = f"{rewindDir}/screenShots/{file_name}.png"
  cv2.imwrite(screenshot_filename, frame)

  cap.release()

def analyze_video(target_date):
    [start_time, end_time, video_file_path] = get_video_file_and_start_end_time(target_date)
    frame = get_target_video_frame(video_file_path,target_date, start_time, end_time)
    show_image_target_frame( video_file_path,target_date, frame)
    return target_date

__all__ = [analyze_video]
