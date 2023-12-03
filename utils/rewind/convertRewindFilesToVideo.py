import os
import ffmpeg
from datetime import datetime
from pathlib import Path

rewindDir = os.path.dirname(os.path.realpath(__file__))


def convert_rewind_files_to_video(date_str):
  # Cleanup and creation
  videos_folder_loc = os.path.join(rewindDir, 'videos')
  videos_temp_text_folder_loc = os.path.join(videos_folder_loc, 'tempText')

  if os.path.exists(videos_folder_loc) == False:
      os.makedirs(videos_folder_loc)

  if os.path.exists(videos_temp_text_folder_loc) == False:
    os.makedirs(videos_temp_text_folder_loc)


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
  for chunk in chunk_files_path:
    created_at = os.path.getmtime(chunk)
    # Convert the creation time to a human-readable format
    created_date = datetime.fromtimestamp(created_at).strftime("%Y-%m-%d-%H-%M-%S")

    with open(videos_temp_text_folder_loc + '/'+ created_date + '.txt', 'w') as f:
      f.write('file ' + chunk.replace(' ', '\ '))


  temp_text_files = os.listdir(videos_temp_text_folder_loc)

  # Concatenate videos from text files
  for text_file in temp_text_files:
    formated_text_file = Path(text_file).stem
    output_file = videos_folder_loc + '/' + formated_text_file +'.mp4'
    ffmpeg.input(videos_temp_text_folder_loc + '/' + text_file, format='concat', safe=0).output(output_file).run()

__all__ = [convert_rewind_files_to_video]

if __name__ == "__main__":
  convert_rewind_files_to_video('2023-12-02 23:59:59')
