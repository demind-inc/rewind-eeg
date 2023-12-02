## How to run

### First, convert your local chunk files of Rewind into the video

Run the function in `convertRewindFilesToVideo.py`

```
convert_rewind_files_to_video('2023-12-01 23:59:59')
```

Then, it will automatically generate the mp4 file in `rewind/videos` folder with `YY-mm-dd-HH-MM-SS.mp4` format

### Second, analyze the video and get the screen shot of the target frame

Run the function in `videoAnalyze.py`

```
analyze_video('2023-12-01 23:59:59')
```
