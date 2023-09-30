import sys
import os
import subprocess
from multiprocessing.pool import ThreadPool
from yt_dlp import YoutubeDL

class VidInfo:
    def __init__(self, yt_id, start_time, end_time, outdir, download_audio=False, video_format='best'):
        self.yt_id = yt_id
        self.start_time = float(start_time)
        self.end_time = float(end_time)
        self.outdir = os.path.join(outdir, str(yt_id))
        self.video_out_filename = os.path.join(self.outdir, f"{yt_id}_{start_time}_{end_time}_video.mp4")
        self.audio_out_filename = os.path.join(self.outdir, f"{yt_id}_{start_time}_{end_time}_audio.mp3")
        self.download_audio = download_audio
        self.video_format = video_format
        
    

    def create_outdir(self):
        os.makedirs(self.outdir, exist_ok=True)

def download(vidinfo):
    yt_base_url = 'https://www.youtube.com/watch?v='
    yt_url = yt_base_url + vidinfo.yt_id

    ydl_opts = {
        'format': vidinfo.video_format,
        'quiet': True,
        'ignoreerrors': True,
        'no_warnings': True,
    }

    if vidinfo.download_audio:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url=yt_url, download=False)
            video_url = info['url']
            video_filename = info['title']
    except:
        return_msg = f'{vidinfo.yt_id}, ERROR (youtube)!'
        return return_msg

    try:
        subprocess.run([
            'ffmpeg', '-ss', str(vidinfo.start_time), '-to', str(vidinfo.end_time),
            '-i', video_url, '-c:v', 'libx264', '-crf', '18',
            '-preset', 'veryfast', '-pix_fmt', 'yuv420p',
            '-y', vidinfo.video_out_filename
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

        if vidinfo.download_audio:
            subprocess.run([
                'ffmpeg', '-ss', str(vidinfo.start_time), '-to', str(vidinfo.end_time),
                '-i', video_url, '-q:a', '0', '-map', 'a',
                '-y', vidinfo.audio_out_filename
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    except subprocess.CalledProcessError:
        return_msg = f'{vidinfo.yt_id}, ERROR (ffmpeg)!'
        return return_msg

    return_msg = f'{vidinfo.yt_id}, DONE!'
    return return_msg

if __name__ == '__main__':

    if "--csv" not in sys.argv:
        print("csv path was not found")
        sys.exit(1)
    
    csv_file = sys.argv[sys.argv.index("--csv")+1]
    if not os.path.exists(csv_file):
        print("csv path error")
        sys.exit(1)



    
    download_audio = "--audio" in sys.argv

    video_format = sys.argv[sys.argv.index("--format") + 1] if "--format" in sys.argv else 'best'

     

    os.makedirs('data', exist_ok=True)
    
    with open(csv_file, 'r') as f:
        lines = f.readlines()
        lines = [x.split(',') for x in lines]
        vidinfos = [VidInfo(x[0], x[1], x[2], 'data', download_audio, video_format) for x in lines]
        for vidinfo in vidinfos:
            vidinfo.create_outdir()

    bad_files = open(f'bad_files_csv.txt', 'w')
    results = ThreadPool(10).imap_unordered(download, vidinfos) 

    cnt,err_cnt = 0,0
    for r in results:
        cnt += 1
        print(cnt, '/', len(vidinfos), r)
        if 'ERROR' in r:
            bad_files.write(r + '\n')
            err_cnt += 1
    bad_files.close()
    print("Total Error : ",err_cnt)