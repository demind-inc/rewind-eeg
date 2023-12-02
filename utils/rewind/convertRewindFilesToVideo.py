import os
import ffmpeg
from datetime import datetime


def convert_rewind_files_to_video(date_str):
  # Cleanup and creation
  if os.path.exists('./videos'):
    os.rmdir('./videos')

  os.makedirs('./videos')

  if os.path.exists('./out.mp4'):
    os.remove('./out.mp4')

  if os.path.exists('./videos.txt'):
    os.remove('./videos.txt')

  ROOT_DIR = os.environ['HOME'] + '/Library/Application Support/com.memoryvault.MemoryVault'

  target_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
  target_year_month = str(target_date.year) + str(target_date.month)
  target_day = str(target_date.day).zfill(2)
  target_year_month_day = target_year_month + '/'+target_day

  chunk_files = os.listdir(ROOT_DIR + '/chunks/'+target_year_month_day)
  chunk_files_path = [ROOT_DIR + '/chunks/'+ target_year_month_day + '/' + chunk_file for chunk_file in chunk_files]


  # Create videos.txt
  with open('./videos.txt', 'w') as f:
    for chunk in chunk_files_path:
      f.write('file ' + chunk.replace(' ', '\ ') + '\n', )

  # Concatenate videos
  ffmpeg.input('./videos.txt', format='concat', safe=0).output('./videos/out.mp4').run()


  # Remove videos.txt
  os.remove('./videos.txt')


# [test] Run command
# convert_rewind_files_to_video('2023-12-01 23:59:59')
