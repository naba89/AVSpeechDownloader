# AVSpeechDownloader

- This script for downloading AVSpeech Dataset. 
- It downloads only the relevant part of the video and audio. 
- The script creates a new folder named 'data' under the working directory.
- Each downloaded audio and video is placed in a folder named after the video id
  - Name of folder `yt_id`
  - Name of video and audio files `yt_id\_start_time\_end_time.mp4/mp3`
  - The script creates a file called `bad_files_csv.txt` which lists the youtube id's of the deleted/private videos which are no longer available for download.
  
Usage:
  ```
  pip install -r requirements.txt
  python downloader.py --csv ./example.csv
  ```

Features:

| Features        | Required | Values    |
|-----------------|----------|--------------------|
| --csv           |    ✅    | csv path           |
| --format        |     ❌    | best,worst,22/18,137/140   |
| --audio         |      ❌    | True/False   |
 

 'best'    = The best quality of video
 'worst'   = The worst quality of video
 '22/18'   = 720p 
 '137/140' =  1080p

NOTE : 
You can change the number of threads according to your resource constraints.
Happy downloading!
