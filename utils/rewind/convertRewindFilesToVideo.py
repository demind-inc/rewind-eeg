import os
import ffmpeg
from datetime import datetime


def convert_rewind_files_to_video(date_str):
  # Cleanup and creation
  if os.path.exists('./videos') == False:
      os.makedirs('./videos')

  if os.path.exists('./videos.txt'):
    os.remove('./videos.txt')

  ROOT_DIR = os.environ['HOME'] + '/Library/Application Support/com.memoryvault.MemoryVault'

  target_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
  target_year_month = str(target_date.year) + str(target_date.month)
  target_day = str(target_date.day).zfill(2)
  target_year_month_day = target_year_month + '/'+target_day
  chunk_files_path = ROOT_DIR + '/chunks/'+target_year_month_day

  if os.path.exists(chunk_files_path) == False:
    print('No chunk files for this date')
    return

  chunk_files = os.listdir(chunk_files_path)
  chunk_files_path = [chunk_files_path + '/' + chunk_file for chunk_file in chunk_files]


  # Create videos.txt
  with open('./videos.txt', 'w') as f:
    for chunk in chunk_files_path:
      f.write('file ' + chunk.replace(' ', '\ ') + '\n', )

  # Concatenate videos
  output_file = './videos/' + str(target_date.year) + '-' + str(target_date.month) +  '-' + target_day +'.mp4'
  ffmpeg.input('./videos.txt', format='concat', safe=0).output(output_file).run()


  # Remove videos.txt
  os.remove('./videos.txt')


# [test] Run command
convert_rewind_files_to_video('2023-12-01 23:59:59')
