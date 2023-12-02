import os
import cv2
from datetime import datetime
from pathlib import Path

# find the two closest dates to the target date
def find_closest_dates(target_time, dates):
    start_closest_date =  min([date for date in dates if date < target_time], key=lambda dt: abs(dt - target_time))
    end_closest_date =  min([date for date in dates if date > target_time], key=lambda dt: abs(dt - target_time) )

    return start_closest_date, end_closest_date

# Get the video file path between the two dates
def get_video_file_date_between_time(date_str):
  video_files = os.listdir('./videos')
  video_files.remove('tempText')

  # Get the list of timestamp of files
  video_file_timestamp_list = [datetime.strptime(Path(video_file).stem, '%Y-%m-%d-%H-%M-%S') for video_file in video_files ]

  closest_dates = find_closest_dates(datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S"), video_file_timestamp_list)[:2]

  return closest_dates

# Get the target video file and the start-time/end-time of the video
def get_video_file_and_start_end_time(date_str):
  [start_closest_date, end_closest_date] = get_video_file_date_between_time(date_str)

  target_video_file_name = './videos' + '/' + end_closest_date.strftime("%Y-%m-%d-%H-%M-%S") + '.mp4'


  return start_closest_date, end_closest_date, target_video_file_name,

# Get the target frame number
def get_target_video_frame(video_file_path, target_date, start_time, end_time):
  video_duration = (end_time - start_time).total_seconds()
  cap = cv2.VideoCapture(video_file_path)
  frame_num = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

  target_frame = int((frame_num /video_duration) * (datetime.strptime(target_date, "%Y-%m-%d %H:%M:%S") - start_time).total_seconds())

  return target_frame

# Show the screen shot of target frame
def show_image_target_frame(video_file_path, target_frame):
  cap = cv2.VideoCapture(video_file_path)
  cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
  ret, frame = cap.read()

  screenshot_filename = f"{video_file_path}frame_{target_frame}.png"
  cv2.imwrite(screenshot_filename, frame)

  cap.release()

def analyze_video(target_date):
    [start_time, end_time, video_file_path] = get_video_file_and_start_end_time(target_date)
    frame = get_target_video_frame(video_file_path,target_date, start_time, end_time)
    show_image_target_frame(video_file_path, frame)

# [test] Run command
# analyze_video('2023-12-01 23:39:46')
