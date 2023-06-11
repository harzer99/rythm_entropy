import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=UserWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)
import pydub
import os
from tqdm.notebook import tqdm
from multiprocessing.pool import Pool
import pytube as pt
from functools import partial
import librosa

def read(f, normalized=False):
    """MP3 to numpy array"""
    a = pydub.AudioSegment.from_mp3(f)
    y = np.array(a.get_array_of_samples())
    if a.channels == 2:
        y = y.reshape((-1, 2))
    if normalized:
        return np.float32(y) / 2**15, a.frame_rate
    else:
        return y, a.frame_rate
    
def rythm_entropy(audio, sr, start = 0.1,  cutoff = 10):
    transformed = np.fft.rfft(audio)
    cutoff_index = int(cutoff/sr*len(audio))
    start_index = int(start/sr*len(audio))
    transformed = transformed[start_index:cutoff_index]
    normalization = max(np.abs(transformed))
    entropy = complex_entropy(transformed/normalization)
    return entropy

def complex_entropy(transformed):
    p = np.abs(transformed)
    S = -np.sum(p*(np.log(p)))
    return S

def analyze_file(path, downsampling_factor = 2):
    audio, sr = librosa.load(path, mono = True)
    #audio = np.array(audio)
    #audio = np.mean(audio, axis = 1)
    audio = audio[::downsampling_factor]   #downsampling for faster fft as we are only interested in low frequencies
    sr = int(sr/downsampling_factor)
    return rythm_entropy(audio, sr)

def analyze_folder(path, Playlist = True):
    if Playlist:
        file_names = os.listdir(path) 
        file_paths = [os.path.join(path, file_name) for file_name in file_names]
        pool = Pool()

        results = pool.map(analyze_file, file_paths)
        pool.close()
        pool.join()
        entropies = {name: entropy for name, entropy in zip(file_names, results)}
        return entropies
    else:
        print(path)
        entropies = {path: analyze_file(path)}
        return entropies

def single_video_download(video_url, playlistname):
    try:
        vid_title = pt.YouTube(video_url).title 
        vid_title = clean_string(vid_title)
        video = pt.YouTube(video_url)
        stream = video.streams.filter(only_audio=True).order_by('abr').last()   #get the audio stream with the highest bitrate
        B = stream.download(output_path= 'cache/'+playlistname, filename=vid_title+'.webm')
        return
    except:
        print('skipping song')

def download(playlist, playlistname):
        n = len(playlist)
        print('Number of Songs: {:.2f}'.format(n))
        i = 0
        #playlistnames = repeat(playlistname, len(playlist))
        pool = Pool()
        worker = pool.imap_unordered(partial(single_video_download, playlistname = playlistname), playlist )
        #tqdm(Worker(worker, n))
        with tqdm(total=n) as pbar:
            while i < n:
                next(worker)
                #print(f'Song {i}/{n} got downloaded')
                pbar.update()
                i += 1
                #print('Download')
        pool.close()
        pool.join()

def analyze_playlist(playlisturl, Playlist = True):
    if Playlist:
        p = pt.Playlist(playlisturl)
        yt_urls = p.video_urls
        playlistname = p.title
        playlistname = clean_string(playlistname)
        download(yt_urls, playlistname)
        return analyze_folder('cache/'+playlistname)
    else:
        playlistname = 'single_download'
        yt_urls = [playlisturl]
        print(yt_urls)
        download(yt_urls, playlistname)
        vid_title = pt.YouTube(playlisturl).title 
        vid_title = clean_string(vid_title)
        return analyze_folder('cache/'+playlistname+'/'+vid_title+'.webm', Playlist= False)

def clean_string(string):
    chars = ['.','/', ':', '(', ')']
    for char in chars:
        string = string.replace(char, '')
    return string

if __name__ == '__main__':
    #complex_music = analyze_folder('complex_music')
    #techno = analyze_folder('techno')
    playlist = 'https://www.youtube.com/watch?v=S83AQhEWmPY&list=PL7eU2Xjx0QsWlmWahShsG1Lm6JfDcskD0&ab_channel=JamesHypeVEVO'
    playlist = 'https://www.youtube.com/watch?v=RZkhCRtdWO8&list=PLPOtzhQJI-KmFnXLkXxJpb3MUdh0T6UxI&ab_channel=DavidSanborn-Topic'
    my_entropies = analyze_playlist(playlist)
    print(my_entropies)
    mean_entropy = np.average(list(my_entropies.values()))
    print(mean_entropy)