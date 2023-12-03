from utils.rewind.videoAnalylze import analyze_video
from utils.analysis import handleEEG
import utils.gpt.config as config

if __name__ == "__main__":
    datafile = 'data/Emotiv-one-hour.csv'
    timestamps = handleEEG.get_all_timestamps(datafile)

    # generate screenshots
    for ts in timestamps:
        analyze_video(ts)