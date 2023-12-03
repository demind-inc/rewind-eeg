
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import pytz

"""
find top 10 (default) peaks and troughs in attention from Emotiv EEG

params: csv_data - filepath for data, nums(optional) - number of peaks/troughs
output: timestamps of 10 peaks and 10 troughs
"""
def find_attention_points(csv_data, convert=True, nums=10):
    data = load_csv(csv_data)
    attention_dataset = get_attention(data)

    peaks = find_attention_peaks(attention_dataset, return_ts=False)
    troughs = find_attention_peaks(attention_dataset, find_troughs=True, return_ts=False)

    # if convert:
    #     peak_ts = [convert_timestamp_to_nyt(ts) for ts in peak_ts]
    #     trough_ts = [convert_timestamp_to_nyt(ts) for ts in trough_ts]

    return peaks, troughs

def convert_timestamp_to_nyt(timestamp, tz='America/New_York'):
    dt_utc = datetime.utcfromtimestamp(timestamp)
    new_york_tz = pytz.timezone(tz)
    dt_new_york = dt_utc.replace(tzinfo=pytz.utc).astimezone(new_york_tz)
    return dt_new_york.strftime('%Y-%m-%d %H:%M:%S')

def load_csv(csv_file):
    pd.set_option('display.float_format', '{:.2f}'.format)
    df = pd.read_csv(csv_file, skiprows=1)
    return df

def get_attention(df):
    attention_data = df.loc[df['PM.Attention.Scaled'].notna(), ['Timestamp', 'PM.Attention.Scaled']]
    return attention_data

def find_attention_peaks(ds, find_troughs=False, return_ts=False):
    sorted = ds.sort_values(by='PM.Attention.Scaled', ascending=find_troughs) # will to descending for troughs
    if return_ts:
        return list(sorted.iloc[0:10]['Timestamp'])
    return sorted.iloc[0:10]

if __name__ == "__main__":
    # data = load_csv('../../data/Emotiv-one-hour.csv')
    result = find_attention_points('../../data/Emotiv-one-hour.csv')
    print(result)