# AVSpeechDownloader
Simple python script for downloading AVSpeech Dataset

Assumptions/Limitations: 
  - `avspeech_train.csv` and `avspeech_test.csv` are in the same directory as the download.py script.
  - creates the output folder in the currect directory based on the train/test set. For now you have to change the directories in the code if required.
  - the script creates a file called `badfiles_train.txt` which lists the youtube id's of the deleted/private videos which are no longer available for download.
  
Usage:
  ```
  python downloader.py train
  ```
Replace train with test if you want to download the test set.

Dependencies:
```
  conda install -c conda-forge ffmpeg
  conda install -c conda-forge youtube-dl
  pip install ffmpeg-python
```
NOTE:

  This is a very simple script. I haven't take too much care, just wrote it quickly to download the dataset. Let me know if you have any problems using it, will try to fix it. Feel free to send in pull requests if you would like to improve it.
  
  Cheers!
