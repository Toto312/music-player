from tkinter import *
from tkinter import Tk
from tkinter import filedialog
from tkinter import ttk
import tkinter

import os
import pygame
from pytube import Playlist
from pytube import YouTube

#Init
root=Tk()
root.title('Music player')
root.geometry("800x800")
root.configure(bg= "#0f1a2b")
root.resizable(False, False)
pygame.init()
selected = 0

#Songs path
if(not os.path.isdir("Songs")):
    os.mkdir("Songs")

#General variables
CURRENT_PATH = os.getcwd()
SONGS_PATH = os.path.join(CURRENT_PATH,"Songs")

def get_songs():
    return os.listdir(SONGS_PATH)

def playmusic():
    global selected
    selected = Lb1.curselection()[0]
    song = os.path.join(SONGS_PATH,get_songs()[selected])
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    que()

def que():
    global selected
    pos = pygame.mixer.music.get_pos()
    if(int(pos)==-1):
        selected+=1
        song = os.path.join(SONGS_PATH,get_songs()[selected])
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
    root.after(1,que)

def pause():
    if(pygame.mixer.music.get_busy()):
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()

def import_music():
    print("Write the url of the playlist or song (it has to be public)")
    a=input()
    if("playlist" in a):
        playlist = Playlist(a)
        for url in playlist:
            YouTube(url).streams.filter(only_audio=True).first().download(SONGS_PATH)
    for i in get_songs():
        if(i[(len(i)-1-2):] == "mp4"):
            to_mp3 = i[:i.find(".")]+".mp3"
            os.system("ffmpeg -i \"{0}\" \"{1}\"".format(os.path.join(SONGS_PATH,i), os.path.join(SONGS_PATH,to_mp3)))
            os.remove(os.path.join(SONGS_PATH,i))

Lb1 = tkinter.Listbox(root)

for i in range(len(get_songs())):
    Lb1.insert(i,get_songs()[i])

#Lb1.curselection()
Lb1.place(relx=0, width=800, height=700)

separator = ttk.Separator(root, orient='horizontal')
separator.place(relx=0, rely=7/8, relwidth=1, relheight=1)

separator = ttk.Separator(root, orient='vertical')
separator.place(relx=8/10, rely=0, relwidth=1, relheight=0.875)

btn = Button(root, text = 'Play', bd = '3',command=playmusic)
btn.place(relx=0.05, rely=0.9, relwidth=0.1, relheight=0.05)

btn1 = Button(root, text = 'Stop', bd = '3',command=pause)
btn1.place(relx=0.2, rely=0.9, relwidth=0.1, relheight=0.05)

btn2 = Button(root, text = 'Import music', bd = '3',command=import_music)
btn2.place(relx=0.35, rely=0.9, relwidth=0.1, relheight=0.05)

root.mainloop()