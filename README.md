# PlaylistParser
Downloads the audio from a youtube playlist and parses it

# use case: 
I use youbube music for most of my music playlists, however songs get removed and songs need internet to be played. 
I used to use Media Human's youtube to mp3 converter to get the songs, but the pure audio from the videos usually has some silence in the begining and end of the file that I wanted to get rid of, so I wrote the [SongCutter](https://github.com/OctoidGames/SongCutter)
This is a continuation of that script, but with the ability to download the songs too. 

# How to use
#### Built for Linux systems | tested on Ubuntu 20.04
Asuming you have the dependencies installed. navigate to the folder PlaylistToMp3.py is in and run it in the terminal with `python3 PlaylistToMp3.py`. It will ask you for the playlist link so paste it into the terminal. the link should look like `https://www.youtube.com/playlist?list=XXXXXXXXXXXXXXXXXXX` After the script has run, a GUI will pop up with the youtube name and the artist and title guessed by the machine. Here you can edit these and make sure all the metadata is correct.

# How to Install
There is no real instalation process as it is just a python script. However, I have added a `Dep.sh` that you can run to install the dependencies

#### step by step
download the files with the green download button.

open the folder in the file explorer of your choise and right click the folder and select open in terminal

now run `chmod +x Dep.sh` this will give Dep.sh permision to run on your machine 

run `./Dep.sh` this will run the dependencies script to install all the libraries and programs that the file uses to run

you will need to put in a password because it is installing things using apt. to see what it is installing and what commands it will run, you can use `nano Dep.sh` or an equivelent command to open the text of the script and inspect it. This is one of the many upsides to open source projects as you can see what it is installing on your machine and you can choose whether or not you want to trust the software based not on the reputation of the developer, but on the actual code itself.

after the script is done, you will now be able to run the python script. Use `python3 PlaylistToMp3.py` to run it and fill in the prompts as given

# wanted features:
* windows translation
