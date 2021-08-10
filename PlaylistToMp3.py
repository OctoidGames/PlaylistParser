from pytube import Playlist
from youtube_title_parse import get_artist_title
from moviepy.editor import *
from pydub import AudioSegment
import webbrowser
import threading


def PURGE(folder):  # deletes directory and contents
    for file in os.listdir(os.curdir + "/"+folder):
        os.remove(os.curdir + "/"+folder+"/"+file)
    os.rmdir(os.curdir + "/"+folder)


def mkfolder(name):  # makes folder without breaking
    try:
        os.mkdir(name)
    except:
        pass  # so it doesn't break if the folders are already there


def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=10):  # this function returns how long the silence on one end of an audio file is
    trim_ms = 0  # ms

    assert chunk_size > 0
    while sound[trim_ms:trim_ms + chunk_size].dBFS < silence_threshold and trim_ms < len(sound): #checks for the last bit of the audio file that is silent (below the threshold)
        trim_ms += chunk_size

    return trim_ms


def mp4_to_mp3(mp4, mp3):     # this function converts from mp4 to mp3 using the pymovie library. it is used because pytube returns an mp4 with no video
    mp4 = AudioFileClip(mp4)     # makes it usable
    mp4.write_audiofile(mp3)     # converts to mp3
    mp4.close() # function call mp4_to_mp3("my_mp4_path.mp4", "audio.mp3")


def clip(file):
    print("picked mp3: " + file)
    sound = AudioSegment.from_file(os.curdir + "/NewAudio/" + file, format="mp3")

    start_trim = detect_leading_silence(sound)  # find silent part in beginning
    end_trim = detect_leading_silence(sound.reverse())  # send reversed song into function to get silence at end

    duration = len(sound)
    trimmed_sound = sound[start_trim:duration - end_trim]  # trim song

    trimmed_sound.export("completed/" + file, format="mp3")  # export trimmed song
    print("exported:" + file)


p = Playlist(input("playlist link: "))  # will change to args later

for video in p.videos:  # for video in playlists
    print("[downloading] "+video.title)  # I like to put these in so I can see it work and I don't get scared
    stream = video.streams.get_audio_only()  # doesn't bother with video, still returns an mp4 tho
    print("filesize: "+str(stream.filesize_approx)+"B")  # I use this as a time estimate

    try:
        # downloading the video
        stream.download("downloaded")
    except:
        print("Error")  # I dunno man, your internet probably broke
    print('Download Complete')

print("downloaded all songs, parsing audio")

mkfolder("audio")
mkfolder("NewAudio") #makes folders

Tlist = []

for file in os.listdir(os.curdir+"/downloaded"): # this adds threads set to parse each song to a list
    if file.endswith('.mp4'):  # filter those blasted mp4s
        #mp4_to_mp3("downloaded/"+file,"audio/"+file[:-1] + '3')
        t = threading.Thread(target=mp4_to_mp3, args=("downloaded/"+file, "audio/"+file[:-1] + '3'))
        Tlist.append(t)
        # this only workd because mp4 and mp3 are one charector different, it cuts off the 4 and appends a 3
        #pymovie likes to write to console alot, don't know how to disable so I keep it

for t in Tlist:  # opens the floodgates!! (starts the treads)
    t.start()

for t in Tlist:  # waits until all the treads are done
    t.join()

print("[Done] starting decifering Metadata")

for file in os.listdir(os.curdir+"/audio"):
    if file.endswith('.mp3'):
        print("decidering: "+file)
        try:
            artist, title = get_artist_title(file[:-4])  # this library tries to decifer the spooky youtube titles
            print("Artist? " + artist + " | title? " + title)
            os.rename(r'audio/' + file, r'NewAudio/' + artist + "-" + title + ".mp3")  # renames file
        except:
            os.rename(r'audio/' + file, r'NewAudio/' + file)  # moves file without rename because man made titles are hard for computers
            print("error decidering title")

print("completed decidering - starting clipping process")
mkfolder("completed")

Tlist = [] # clears the Thread List

for file in os.listdir(os.curdir+"/NewAudio"):
    if file.endswith('.mp3'):
        t = threading.Thread(target=clip, args=(file,))
        Tlist.append(t)

for t in Tlist:
    t.start()

for t in Tlist:
    t.join()

print("cleaning up the mess")

PURGE("audio")  # I made a purge function because you have to delete the directory contents before you can delete the directory
PURGE("NewAudio")
PURGE("downloaded")

print("completed!")

try:
    webbrowser.open(os.curdir+"/completed")
except:
    print("failed to open folder, find your completed songs in the 'completed' directory")

