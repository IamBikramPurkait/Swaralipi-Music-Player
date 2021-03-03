'''
Music Player Using Tkinter - Musicolet
Author : Bikram Purkait
Completed on : 03/03/2021
'''


# Import neccesary module
from tkinter import *
from tkinter import ttk
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from pygame import mixer
from tkinter import messagebox as mb
from PIL import ImageTk, Image
from tkinter import filedialog
import os
import time

# Set global value
playing = False
paused = False
mute = False
current_time = 0
total_time = 0
current_time_converted = 0
songs = []
file = ''



''' Create all required function '''

# Function for load music folderwise
def loadmusic():
    # create a list for playble extension
    extension = ['mp3', 'wav', 'mpeg', 'm4a', 'wma', 'ogg']
    global songs
    # Ask for a directory, and return the file name
    dir_ = filedialog.askdirectory(
        initialdir='Desktop', title='Select Directory')
    # Change the current working directory to the specified path.
    os.chdir(dir_)
    # Return a list containing the names of the files in the directory
    dir_files = os.listdir(dir_)
    # check extension from the selected folder and insert a song in playlist box and songs list
    for file in dir_files:
        for ex in extension:
            # check for right extension
            if file.split('.')[-1] == ex:
                # insert the song in playlist box by removing .mp3 from the song name
                playlistbox.insert(END, file.replace('.mp3', ''))
                # insert the song in songs list
                songs.append(file)
                # update status
                status.set('Playlist Updated')


# Function for load music filewise
def fileselect():
    # Ask for a filename to open
    song = filedialog.askopenfilename(
        initialdir='audio/', title="Choose A Song")
    # Change the current working directory to the specified path
    os.chdir(os.path.dirname(song))
    # remove path and .mp3 from the song name
    song = song.split('/')[-1]
    song = song.replace(".mp3", "")
    # insert a song in playlist box
    playlistbox.insert(END, song)
    # insert a song in songs list with adding .mp3 extension
    songs.append(f'{song}.mp3')


# function for playing a song
def play():
    # make playing and paused global variable
    global playing
    global paused

# using try and except block
    try:
        # if playing == false then song is paused state so play the song
        if playing == False:
            global file
            # Get a ACTIVE item from playlist box
            file = playlistbox.get(ACTIVE)
            # adding .mp3 in file name
            file = f"{file}.mp3"
            # load the song
            mixer.music.load(file)
            # play the song
            mixer.music.play()
            # update the status bar
            status.set('Playng - '+str(file.split('.mp3')[0]))
            # change the play button image to pause button image
            playbtn['image'] = pause_image
            # set the playing variable state to True
            playing = True
            # show the album art for the current ACTIVE song
            show_detail(file)

        else:
            # if paused == True then music is currently in paused state
            if paused == True:
                # unpause the song
                mixer.music.unpause()
                # update the status
                status.set('Playng - '+str(file.split('.mp3')[0]))
                # change the play button image to pause button image
                playbtn['image'] = pause_image
                # set the paused variable state to False
                paused = False
            else:
                # pause the song
                mixer.music.pause()
                # update the status
                status.set('Music Paused')
                # change the pause button image to play button image
                playbtn['image'] = play_image
                # set the paused variable state to True
                paused = True

        # call the play_time function for get the song details
        play_time()

    except:
        # show error if no songs found to play
        mb.showerror('error', 'No file found to play.')


# function for grab the songs details
def play_time():
    # get the current position of the song in sec
    current_time = mixer.music.get_pos()/1000
    # formatting the current song time in local mm:ss format  
    current_time_converted = time.strftime('%M:%S', time.gmtime(current_time))
    # set the start durartion label to current_time_converted
    dur_start.config(text=current_time_converted)
    # update the song scalebar by song current time
    myscroll.config(value=int(current_time))
    # call the play_time function after every 1000 ms to update the current song time
    dur_start.after(1000, play_time)
    global file
    # load song with mutagen
    song = MP3(file)
    global total_time
    # get the song length
    total_time = song.info.length
    # convert song length to local mm:ss format
    total_time_converted = time.strftime('%M:%S', time.gmtime(total_time))
    # update the end duration label by the song length
    dur_end.config(text=total_time_converted)
    # change the total song slider size to song length
    slider_pos = int(total_time)
    myscroll.config(to=slider_pos)


# function for stop the song
def stop():
    global playing, dur_start
    # stop the song
    mixer.music.stop()
    # set the playing variable state to False
    playing = False
    # change the pause button image to play button image
    playbtn['image'] = play_image
    # Clear the ACTIVE selection song from the playlist box 
    playlistbox.selection_clear(ACTIVE)
    # update the status
    status.set('Music Stopped')
    # update the start duration label to 00:00
    dur_start.config(text='00:00')


# function the change the previous song
def prev_song():
    global songs
    global file
    # get the previous songs index from the songs list using file name
    index = songs.index(file)-1
    # get the song name using index
    file = songs[index]
    # load the song
    mixer.music.load(file)
    # play the song
    mixer.music.play()
    # update the status
    status.set('Playng - '+str(file.split('.mp3')[0]))
    # clear the past song selection in playlist box
    playlistbox.selection_clear(0, END)
    # activate the new song selection bar
    playlistbox.activate(index)
    # set the new song selection bar
    playlistbox.selection_set(index, last=None)
    # show the album art for the current ACTIVE song
    show_detail(file)


# function for change the next song
def next_song():
    global file
    global songs
    # get the next songs index from the songs list using file name
    index = songs.index(file)+1
    # get the song name using index
    file = songs[index]
    # load the song
    mixer.music.load(file)
    # play the song
    mixer.music.play()
    # update the status
    status.set('Playng - '+str(file.split('.mp3')[0]))
    # clear the past song selection in playlist box
    playlistbox.selection_clear(0, END)
    # activate the new song selection bar
    playlistbox.activate(index)
    # set the new song selection bar
    playlistbox.selection_set(index, last=None)
    # show the album art for the current ACTIVE song
    show_detail(file)


# function for the mute the song
def mute_fun():
    global mute
    # if song not mute then mute the song
    if mute == False:
        # set the song volume to 0.0
        mixer.music.set_volume(0.0)
        # update the status
        status.set('Music Mute')
        # change the volume button image to mute button image
        vol_btn['image'] = mute_image
        # set the mute variable state to True
        mute = True
    else:
        # if song not mute then set the song volume to full level
        mixer.music.set_volume(1.0)
        # change the mute button image to volume button image
        vol_btn['image'] = vol_image
        # upadte the status
        status.set('Playng  -'+str(file.split('.mp3')[0]))
        # set the mute variable state to False
        mute = False


# function for the change the volume level using volume slider 
def set_volume(num):
    # get the current volume slider value
    volume = volume_bar.get()/100
    # set the current volume slider value to songs volume
    mixer.music.set_volume(float(volume))


# function for the delete a single song from a playlist box
def delete_song():
    # stop the current song
    mixer.music.stop()
    # delete the ANCHOR song from the playlist box
    playlistbox.delete(ANCHOR)
    # clear the selection
    playlistbox.selection_clear(ANCHOR)
    # update the status
    status.set('Song Deleted')


# function for the delete all song from the playlist box
def delete_allsong():
    # stop the song
    mixer.music.stop()
    # delete the all songs from the playlist box
    playlistbox.delete(0, END) 
    # update the status
    status.set('All song deleted')


# function for make albumart for the current playing song
def show_detail(play_song):
    # open temp.jpg and write new song image on it
    with open('temp.jpg', 'wb') as img:
        # load song with ID3
        a = ID3(play_song)
        # fetch current song albumart image
        img.write(a.getall('APIC')[0].data)
        # calling the makealbumartimage function for resize the current song albumart
        image = makealbumartimage('temp.jpg')
        # configure albumart to the albumart label
        album_art_label.configure(image=image)
        album_art_label.image = image


# function for the resize the album art image
def makealbumartimage(image_path):
    # open the image
    image = Image.open(image_path)
    # resize the image
    image = image.resize((290, 270), Image.ANTIALIAS)
    # return the image
    return ImageTk.PhotoImage(image)


# function for about
def about():
    mb.showinfo('Musicolet', 'It is the basic music player with some advance feature made in Python.😎\nIt is created by Bikram Purkait with ❤.\nIt is completed on 03/03/2021.\nThanks for using the application.👍')


# function for shortcut key
def shortcut_key():
    mb.showinfo('Shortcut Key','1> Select a Folder - ctrl + o\n2> Select a File - ctrl + l\n3> Delete a song - Delete\n4> Delete all song - ctrl + Delete\n5> Exit - e\n6> Play/Pause - Spacebar\n7> Select and Play Song - Double Click Left Mouse Button\n8> Prev Song - Up Arrow\n9> Next Song - Down Arrow\n10> Stop - s\n11> Mute - m ')


# function for repeat 
def repeat():
    status.set('Feature Coming Soon.Please Stay with Us.')




''' Main GUI '''

# initialising pygame mixer
mixer.init()
# create a root instances for the tkinter
root = Tk()


# set the title
root.title("Musicolet")
# set the geometry
root.geometry('800x520')
# set tkinter window not resizable
root.resizable(height=False, width=False)
# set the icon
root.iconbitmap("icon/icon.ico")
# create the StringVar for the status 
status = StringVar()
# set the initial status
status.set('❤Welcome to you in Musiocolet❤')




''' Create a Menu '''

# create the mainmenu
mainmenu = Menu(root, tearoff=0)
# create filemenu under mainmenu
filemenu = Menu(mainmenu, tearoff=0)
# create submenu for the filemenu
filemenu.add_command(label='Folder Select - ctrl + o',font='Helvetica 10 bold', command=loadmusic)
filemenu.add_command(label='File Select - ctrl + l',font='Helvetica 10 bold',  command=fileselect)
# add the separator
filemenu.add_separator()
# create submenu for the filemenu
filemenu.add_command(label='Delete a Song - Delete',font='Helvetica 10 bold',  command=delete_song)
filemenu.add_command(label='Delete all song - ctrl + Delete',font='Helvetica 10 bold',  command=delete_allsong)
# add the separator
filemenu.add_separator()
# create submenu for the filemenu
filemenu.add_command(label='Exit - e',font='Helvetica 10 bold',  command=exit)
# add filemenu to the mainmenu
mainmenu.add_cascade(label='File', menu=filemenu)
# add about under mainmenu
mainmenu.add_command(label='About', command=about)
# add Shortcut Key under mainmenu
mainmenu.add_command(label='Shortcut Key', command=shortcut_key)
# configure mainmenu with the root
root.config(menu=mainmenu)



# Create LabelFrame
songtrack_frm = LabelFrame(master=root, text="Song Track",font='Helvetica 11 bold italic',fg='indian red')
songtrack_frm.place(x=0, y=0, width=350, height=350)

playlist_frm = LabelFrame(master=root, text="Playlist",font='Helvetica 11 bold italic',fg='peachpuff4')
playlist_frm.place(x=350, y=0, width=450, height=350)

control_frm = LabelFrame(master=root, text="Control Bar",font='Helvetica 11 bold italic',fg='blue')
control_frm.place(x=0, y=350, width=800, height=110)

status_frm = LabelFrame(master=root, text="Song Status",font='Helvetica 11 bold italic',fg='DarkOrange4')
status_frm.place(x=0, y=460, width=800, height=40)




''' Create a Load Button '''

# create a style for the ttk.button
s = ttk.Style()
# configure ttk.button
s.configure('TButton', font='Helvetica 10 bold italic')
# Create load button to add folderwise song in playlist box
loadbtn = ttk.Button(playlist_frm, text="Load Music", command=loadmusic,style='TButton')
# pack the load button
loadbtn.pack()



''' Make a Scrollbar '''

# create vertical and horizontal scrollbar for the playlist box
x_scroll = ttk.Scrollbar(playlist_frm, orient=HORIZONTAL)
y_scroll = ttk.Scrollbar(playlist_frm, orient=VERTICAL)
# create the playlist box and set the xscrollcommand and yscrollcommand
playlistbox = Listbox(playlist_frm, yscrollcommand=y_scroll.set,
                      xscrollcommand=x_scroll.set, height=350,font='Helvetica 10 italic',fg='purple4')
# pack the horizontal and vertical scrollbar 
x_scroll.pack(side=BOTTOM, fill=X)
y_scroll.pack(side=RIGHT, fill=Y)
# configure vertical and horizontal scrollbar with yview and xview 
x_scroll.config(command=playlistbox.xview)
y_scroll.config(command=playlistbox.yview)
# pack the playlist box
playlistbox.pack(fill=BOTH)


# Create the image for buttons
pause_image = PhotoImage(file="icon/pause.png")
mute_image = PhotoImage(file="icon/mute.png")
vol_image = PhotoImage(file="icon/vol.png")
play_image = PhotoImage(file="icon/play.png")
prev_image = PhotoImage(file="icon/prev.png")
next_image = PhotoImage(file="icon/next.png")
stop_image = PhotoImage(file="icon/stop.png")
repeat_image = PhotoImage(file="icon/repeat.png")
repeat_one_image = PhotoImage(file="icon/repeat_one.png")
shuffle_image = PhotoImage(file="icon/shuffle.png")


# create the albumart label and place it
album_art_label = Label(songtrack_frm)
album_art_label.place(x=25, y=25)



''' Make Button and bind it with its corresponding description label''' 

# create the play button , place it and bind it with its description label
playbtn = Button(control_frm, command=play, image=play_image, bd=0)
playbtn.place(x=350, y=5)

def on_enter_play(event):
    play_des.place(x=325, y=35)

def on_leave_play(event):
    play_des.place(x=1000, y=1000)

playbtn.bind('<Enter>', on_enter_play)
playbtn.bind('<Leave>', on_leave_play)


# create the previous button , place it and bind it with its description label
prevbtn = Button(control_frm, image=prev_image, bd=0, command=prev_song)
prevbtn.place(x=300, y=0)

def on_enter_prev(event):
    prev_des.place(x=290, y=35)

def on_leave_prev(event):
    prev_des.place(x=1000, y=1000)

prevbtn.bind('<Enter>', on_enter_prev)
prevbtn.bind('<Leave>', on_leave_prev)


# create the next button , place it and bind it with its description label
nextbtn = Button(control_frm, image=next_image, bd=0, command=next_song)
nextbtn.place(x=380, y=0)

def on_enter_next(event):
    next_des.place(x=365, y=35)

def on_leave_next(event):
    next_des.place(x=1000, y=1000)

nextbtn.bind('<Enter>', on_enter_next)
nextbtn.bind('<Leave>', on_leave_next)


# create the stop button , place it and bind it with its description label
stopbtn = Button(control_frm, command=stop, image=stop_image, bd=0)
stopbtn.place(x=425, y=5)

def on_enter_stop(event):
    stop_des.place(x=410, y=35)

def on_leave_stop(event):
    stop_des.place(x=1000, y=1000)

stopbtn.bind('<Enter>', on_enter_stop)
stopbtn.bind('<Leave>', on_leave_stop)


# create the volume button , place it and bind it with its description label
vol_btn = Button(control_frm, command=mute_fun, image=vol_image, bd=0)
vol_btn.place(x=600, y=10)

def on_enter_vol(event):
    vol_des.place(x=595, y=35)

def on_leave_vol(event):
    vol_des.place(x=1000, y=1000)

vol_btn.bind('<Enter>', on_enter_vol)
vol_btn.bind('<Leave>', on_leave_vol)


# create the repeat button , place it and bind it with its description label
repeat_btn = Button(control_frm, image=repeat_image, bd=0, command=repeat)
repeat_btn.place(x=265, y=7)

def on_enter_repeat(event):
    repeat_des.place(x=255, y=35)

def on_leave_repeat(event):
    repeat_des.place(x=1000, y=1000)

repeat_btn.bind('<Enter>', on_enter_repeat)
repeat_btn.bind('<Leave>', on_leave_repeat)



'''Make a volume bar and song slider'''

# create the scale for control the volume of the song
global volume_bar
volume_bar = ttk.Scale(control_frm, from_=0, to=100,
                       orient=HORIZONTAL, command=set_volume)
# set the initial volume bar to 70    
volume_bar.set(70)
# set the initial song volume to 0.7 under 1
mixer.music.set_volume(0.7)
# place the volume bar
volume_bar.place(x=630, y=8)



# create the scale for the current song
global myscroll
myscroll = ttk.Scale(control_frm, from_=0, to=100,
                     orient=HORIZONTAL, length=500)
myscroll.place(x=130, y=50)


# create label for start and end duration and place
global dur_start, dur_end
dur_start = Label(control_frm, text='00:00',font='Helvetica 11 bold italic',fg='dark violet')
dur_start.place(x=80, y=50)
dur_end = Label(control_frm, text='00:00',font='Helvetica 11 bold italic',fg='dark violet')
dur_end.place(x=650, y=50)



''' Binding the key with 
1) Folder load  
2) File load 
3) Delete a single song 
4) Delete all song 
5) Exit 
6) Mute 
7) Play Button 
8) Prev 
9) Next 
10) Stop Button 
'''

# Create a corresponding function for binding the key
def load_fun(event):
    loadmusic()

def file_select_fun(event):
    fileselect()

def delete_song_fun(event):
    delete_song()

def delete_all_song_fun(event):
    delete_allsong()

# function for exit
def exit_fun(event):
    stop()
    exit()

def mute_key_fun(event):
    mute_fun()

def play_fun(event):
    if event.char == ' ':
        play()

def play_fun_doublebutton(event):
    stop()
    play()

def prev_fun(event):
    prev_song()

def next_fun(event):
    next_song()

def stop_fun(event):
    stop()


# bind the function with the key
root.bind('<Control-o>', load_fun)
root.bind('<Control-l>', file_select_fun)
root.bind('<Delete>', delete_song_fun)
root.bind('<Control-Delete>', delete_all_song_fun)
root.bind('<e>', exit_fun)
root.bind('<m>', mute_key_fun)
root.bind('<Key>', play_fun)
root.bind('<Double-Button-1>', play_fun_doublebutton)
root.bind('<Up>', prev_fun)
root.bind('<Down>', next_fun)
root.bind('<s>', stop_fun)



# create the all description label for the button
play_des = Label(control_frm, text='Play/Pause', relief='groove')
stop_des = Label(control_frm, text='Stop Music', relief='groove')
prev_des = Label(control_frm, text='Previous Track', relief='groove')
next_des = Label(control_frm, text='Next Track', relief='groove')
vol_des = Label(control_frm, text='Mute', relief='groove')
repeat_des = Label(control_frm, text='Repeat', relief='groove')



# create the label for the status and pack it
status_lbl = Label(status_frm, textvariable=status,font='Helvetica 11 bold italic',fg='dark green')
status_lbl.pack()



# Call the mainloop of Tk
root.mainloop()
