## How to run

### First, convert your local chunk files of Rewind into the video

Run the function

```
from convertRewindFilesToVideo import convert_rewind_files_to_video

convert_rewind_files_to_video('2023-12-01 23:59:59')
```

Then, it will automatically generate the mp4 file in `rewind/videos` folder with `YY-mm-dd-HH-MM-SS.mp4` format

### Second, analyze the video and get the screen shot of the target frame

Run the function

```
from videoAnalyze import analyze_video

analyze_video('2023-12-01 23:59:59')
```

Then, you will get the screen shot of the specific time
