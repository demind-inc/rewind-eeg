import os
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


__all__ = [ get_video_file_and_start_end_time, get_video_file_date_between_time, find_closest_dates]
