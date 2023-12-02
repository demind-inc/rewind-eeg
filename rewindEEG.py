from utils.rewind.videoAnalylze import analyze_video
from utils.rewind.convertRewindFilesToVideo import convert_rewind_files_to_video
from utils.analysis import handleEEG


if __name__ == "__main__":
    datafile = 'data/Emotiv-one-hour.csv'
    peak_points, trough_points = handleEEG.find_attention_points(datafile)

    print(peak_points, trough_points)