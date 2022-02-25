import re

from pytube import *
from youtube_title_parse import get_artist_title
from moviepy.editor import *
from pydub import AudioSegment
import webbrowser
import threading
from tkinter import *
import time

sema = threading.BoundedSemaphore(value=32)

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'', text)


def PURGE(folder):  # deletes directory and contents
    for file in os.listdir(os.curdir + "/" + folder):
        os.remove(os.curdir + "/" + folder + "/" + file)
    os.rmdir(os.curdir + "/" + folder)


def mkfolder(name):  # makes folder without breaking
    try:
        os.mkdir(name)
    except:
        pass  # so it doesn't break if the folders are already there


def detect_leading_silence(sound, silence_threshold=-50.0,
                           chunk_size=10):  # this function returns how long the silence on one end of an audio file is
    trim_ms = 0  # ms

    assert chunk_size > 0
    while sound[trim_ms:trim_ms + chunk_size].dBFS < silence_threshold and trim_ms < len(
            sound):  # checks for the last bit of the audio file that is silent (below the threshold)
        trim_ms += chunk_size

    return trim_ms


def mp4_to_mp3(mp4, mp3, thread_number):  # this function converts from mp4 to mp3 using the pymovie library. it is used because pytube returns an mp4 with no video
    sema.acquire()
    print("strarting #" + str(tn))
    mp4 = AudioFileClip(mp4)  # makes it usable
    mp4.write_audiofile(mp3)  # converts to mp3
    mp4.close()  # function call mp4_to_mp3("my_mp4_path.mp4", "audio.mp3")
    sema.release()


def clip(file):
    print("picked mp3: " + file)
    sound = AudioSegment.from_file(os.curdir + "/audio/" + file, format="mp3")

    start_trim = detect_leading_silence(sound)  # find silent part in beginning
    end_trim = detect_leading_silence(sound.reverse())  # send reversed song into function to get silence at end

    duration = len(sound)
    trimmed_sound = sound[start_trim:duration - end_trim]  # trim song

    trimmed_sound.export("completed/" + file, format="mp3")  # export trimmed song
    print("exported:" + file)

mkfolder("audio")
mkfolder("downloaded")
mkfolder("NewAudio")  # makes folders

p = Playlist(input("playlist link: "))  # will change to args later

songs = []
for v in p.videos:
    songs.append(v)

# not entirely sure, but it randomly stops some times and i think it's because youtube has a cetain number of videos per minute you can download or something
count = 0
for video in songs:  # for video in playlists
    count += 1
    print("[downloading] " + video.title + " : song " + str(count) + " of " + str(
        len(songs)))  # I like to put these in so I can see it work and I don't get scared
    video.streams.filter(only_audio=True) # doesn't bother with video, still returns an mp4 tho
    stream = video.streams.filter(only_audio=True).first()  # doesn't bother with video, still returns an mp4 tho

    print("filesize: " + str(stream.filesize) + "B")  # I use this as a time estimate

    try:
        # downloading the video
        f = stream.download("downloaded")
        #os.rename(f, deEmojify(f.title()))
    except Exception as e:
        if hasattr(e, 'message'):
            print(e.message)
        else:
            print(e)
        print("appending failed song to queue ||| moving on")
        songs.append(video)
    print('Download Complete')

print("downloaded all songs, parsing audio")

Tlist = []
tn = 0

for file in os.listdir(os.curdir + "/downloaded"):  # this adds threads set to parse each song to a list
    if file.endswith('.mp4'):  # filter those blasted mp4s
        # mp4_to_mp3("downloaded/"+file,"audio/"+file[:-1] + '3')
        tn += 1
        NEW = "audio/" + deEmojify(file[:-1] + '3')
        t = threading.Thread(target=mp4_to_mp3, args=("downloaded/" + file, NEW, tn))
        Tlist.append(t)
        # this only worked because mp4 and mp3 are one character different, it cuts off the 4 and appends a 3
        # pymovie likes to write to console a lot, don't know how to disable so I keep it


for t in Tlist:  # starts all threads
    t.start()

time.sleep(1)

for t in Tlist:  # waits until all the treads are done
    t.join()

print("completed deciphering - starting clipping process")
mkfolder("completed")

Tlist = []  # clears the Thread List

for file in os.listdir(os.curdir + "/audio"):
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

#try:
#    webbrowser.open(os.curdir + "/completed")
#except:
#    print("failed to open folder, find your completed songs in the 'completed' directory")

s = {}

c = 0
for file in os.listdir(os.curdir + "/completed"):
    if file.endswith('.mp3'):
        print("decidering: " + file)
        try:
            artist, title = get_artist_title(file[:-4])  # this library tries to decifer the spooky youtube titles\
            s[file] = [artist, title]

        except:
            s[file] = ["", ""]


artists = []
titles = []
# s = {"f.mp3": ["god", "tracks"], "m.mp3": ["god", "track2"], "g.mp3": ["God", "track3"], }
print(s.items())


def data():
    Label(frame, text="Youtube").grid(row=0, column=0)
    Label(frame, text="Artist").grid(row=0, column=1)
    Label(frame, text="Title").grid(row=0, column=2)

    for i in range(len(s)):
        g = list(s.items())[i][0]
        h = g[:-4]
        print(h)

        entryText = StringVar()
        entryText2 = StringVar()
        Label(frame, text=h).grid(row=i + 1, column=0, sticky=W)
        a = Entry(frame, text=s[g][0], textvariable=entryText)
        entryText.set(s[g][0])
        t = Entry(frame, text=s[g][1], textvariable=entryText2)
        entryText2.set(s[g][1])
        artists.append(a)
        titles.append(t)
        a.grid(row=i + 1, column=1, sticky=W)
        t.grid(row=i + 1, column=2, sticky=W)

    saveButton = Button(frame, text="Done", command=save, bg='green')
    saveButton.grid(row=len(s) + 1, column=1, columnspan=3, sticky=EW)


def myfunction(event):
    canvas.configure(scrollregion=canvas.bbox("all"), width=680, height=440)


def removeDots(dottedString):
    dottedString.replace(".", "")
    return dottedString


def save():
    for i in range(len(s)):
        g = list(s.items())[i][0]
        os.rename('completed/' + g, 'NewAudio/' + artists[i].get() + " - " + removeDots(titles[i].get()))

    print("closing window")

    try:
        webbrowser.open(os.curdir + "/NewAudio")
    except:
        print("failed to open folder, find your completed songs in the 'NewAudio' directory")

    PURGE("completed")
    root.destroy()


mkfolder("NewAudio")


root = Tk()

root.geometry("720x480")

#myframe = Frame(root, relief=GROOVE, bd=1, bg='blue')
myframe = LabelFrame(root, text="Edit Your Files", padx=5, pady=5)
myframe.pack(side="left", expand=True)

canvas = Canvas(myframe)
frame = Frame(canvas)
myscrollbar = Scrollbar(myframe, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=myscrollbar.set)

myotherscrollbar = Scrollbar(myframe, orient="horizontal", command=canvas.xview)
canvas.configure(xscrollcommand=myotherscrollbar.set)

myscrollbar.pack(side="right", fill="y")
myotherscrollbar.pack(side="bottom", fill="x")
canvas.pack(side="left", expand=True)
canvas.create_window((0, 0), window=frame, anchor='nw')
frame.bind("<Configure>", myfunction)

data()
root.mainloop()
