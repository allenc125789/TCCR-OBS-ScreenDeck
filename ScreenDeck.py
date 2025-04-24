import tkinter as tk
import getpass
import subprocess
import errno
import os
import time
import obsws_python as obs

if os.getenv('VIRTUAL_ENV') is None:
    print("[ERROR] This script must be run in a virtual environment.")
    print("[HINT] `source ./.venv/bin/activate`.")
    exit()

subprocess.run(['/usr/bin/sudo', '/usr/bin/whoami'])

goprogram = subprocess.Popen(['/usr/bin/sudo', '/usr/local/sbin/gopro', 'webcam', '-p', 'enx', '-n', '-a'])
time.sleep(16)
obsprogram = subprocess.Popen(['/usr/bin/obs', '>', '/dev/null'])

root = tk.Tk()
fColumn = tk.Frame(root)
tbTitle = tk.Text(fColumn, height=3, width=60)

#Sys vars, don't change.
titleText = ""
statusLive = False


def startStream():
    global statusLive
    global tbTitle
    if (statusLive == False):
        statusLive = True
        cl = obs.ReqClient()
        cl.set_current_program_scene("Trans-In")
        time.sleep(21)
        cl.set_current_program_scene("Stand-By")
        tbTitle.insert('1.0', titleText)
    else:
        pass

def stopStream():
    global statusLive
    if (statusLive == True):
        statusLive = False
        cl = obs.ReqClient()
        cl.set_current_program_scene("Trans-Out")
        time.sleep(21)
        cl.set_current_program_scene("Off")
    else:
        pass


def resetTitle():
    global titleText
    global fColumn
    global tbTitle
    try:
        f = open("title.txt", "r")
        titleText = f.read()
        tbTitle.delete("1.0", tk.END)
        tbTitle.insert("1.0", titleText)
        f.close
    except:
        with open("title.txt", "w") as f:
            titleText = "           TCC, Tulsa Community College Robotics            |            Event: XXXXX: 04-08-2025             |            "
            f.write(titleText)
            tbTitle.insert("1.0", titleText)
            pass

def saveTitle():
    global fColumn
    global tbTitle
    titleText = tbTitle.get("1.0", tk.END)
    tbTitle.delete("1.0", tk.END)
    with open("title.txt", "w") as f:
        f.write(titleText)
        f.close
    tbTitle.delete("1.0", tk.END)
    tbTitle.insert("1.0", titleText)



def safeExit():
    #Stops obs
    obsprogram.terminate()
    obsprogram.wait()
    obsprogram.kill()
    #Stops gopro
    goprogram.terminate()
    goprogram.wait()
    goprogram.kill()
    #Restarts gopro and ends it again.
    #Fixes bug where gopro continues in webcam mode, despite exiting the program.
    time.sleep(2)
    goprogram2 = subprocess.Popen(['/usr/bin/sudo', '/usr/local/sbin/gopro', 'webcam', '-p', 'enx', '-n', '-a'])
    time.sleep(4)
    goprogram2.terminate()
    goprogram2.wait()
    goprogram2.kill()
    #Stops tkinter
    root.quit()

def disableEvent():
    pass

def tkrender():
    global root
    global fColumn
    global tbTitle
    root.protocol("WM_DELETE_WINDOW", disableEvent)
    root.title('TCCR OBS ScreenDeck')
    w = 775
    h = 375

    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen

    x = (ws) - (w*4)
    y = (hs) - (h/4)

    # set the dimensions of the screen
    # and where it is placed
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    #Frame for Column
    fColumn.columnconfigure(0, weight=1)
    fColumn.columnconfigure(1, weight=1)

    var1=tk.IntVar()

    #cbOnline/cbOffline frame.
    fState = tk.Frame(fColumn, width=228, height=50)
    fState.grid(row=0, column=0, sticky=tk.W+tk.E)
    #Checkboxs to change stream from live-to-offline.
    cbOnline = tk.Checkbutton(fState, text='Online', variable=var1, offvalue=(not statusLive), command=startStream)
    cbOffline = tk.Checkbutton(fState, text='Offline', variable=var1, onvalue=statusLive, command=stopStream)
    #Label for Stream State
    lState = tk.Label(fColumn, text="Stream Status:", font=("Aerial", 30, "bold"))
    lState.grid(row=0, column=0, sticky=tk.W+tk.E, padx=100)


    #Textbox for the Stream's Title.
    tbTitle.grid(row=3, column=0, sticky=tk.W+tk.E)
    resetTitle()
    #btnTitle* frame.
    fTitle = tk.Frame(fColumn, width=228, height=50)
    fTitle.grid(row=4, column=0, sticky=tk.W+tk.E)
    #Buttons for saving/reverting tbTitle.
    btnTitleReset = tk.Button(fTitle, text='Reset', command=resetTitle)
    btnTitleSave = tk.Button(fTitle, text='Save', command=saveTitle)
    #Label for tbTitle.
    lTitle = tk.Label(fColumn, text="Stream Title")
    lTitle.grid(row=2, column=0, sticky=tk.W+tk.E)


    #checkboxes for cameras.
    cbStandBy = tk.Checkbutton(fColumn, text='Stand-by...',  font=("Aerial", 10, "bold"))
    cbStandBy.grid(row=5, column=0, sticky=tk.W+tk.E)
    cbCam1 = tk.Checkbutton(fColumn, text='Cam 1')
    cbCam1.grid(row=6, column=0, sticky=tk.W+tk.E)
    cbCam2 = tk.Checkbutton(fColumn, text='Cam 2')
    cbCam2.grid(row=7, column=0, sticky=tk.W+tk.E)
    cbCam3 = tk.Checkbutton(fColumn, text='Cam 3')
    cbCam3.grid(row=8, column=0, sticky=tk.W+tk.E)


    #Buttons for Timer.
    fTimer = tk.Frame(fColumn, width=228, height=50, borderwidth=2, relief="solid")
    fTimer.grid(row=0, column=1, sticky=tk.W+tk.E)
    lTimer = tk.Label(fTimer, text="+Battle Timer+", font=("Aerial", 10, "bold"))
    btnShowHide = tk.Button(fTimer, text='Hide/Show')
    btnStopStart = tk.Button(fTimer, text='Start/Stop')


    #Button for safe exit.
    btnSafeExit = tk.Button(fColumn, text='Safe Exit', font=("Aerial", 10, "bold"), command=safeExit)
    btnSafeExit.grid(row=23, column=1, sticky=tk.W+tk.E)

    ###Packing/rendering into main window.
    #Online/Offline Function.
    fColumn.pack(fill='x')


    #Checkboxes for Online/Offline Stream.
    cbOffline.pack(side="bottom", anchor="e")
    cbOnline.pack(side="top", anchor="e")

    #Timer Function.
    lTimer.pack()
    btnShowHide.pack()
    btnStopStart.pack()

    #Title Function.
    btnTitleReset.pack(side="left")
    btnTitleSave.pack(side="left")


    #Start root GUI window.
    root.mainloop()

def execGopro():
       #For Linux Systems. Calls the program "gopro_as_webcam_on_linux" by jschmid1.
       #https://github.com/jschmid1/gopro_as_webcam_on_linux
       try:
           global goprogram
       except goprogram.CalledProcessError as e:
           print(
           """\n\n[ERROR] Failed to open gopro. Please make sure you have:
             1) Connected your gopro (The gopro will say 'USB connected')
             \t Tip 1: Turn off gopro, unplug, turn on, plug back in after full gopro boot.
             \t Tip 2: Try a different/better USB cable.
             2) Installed the program:
             \t 'https://github.com/jschmid1/gopro_as_webcam_on_linux'
             3) You have a gopro 8+""")
           exit()

def execOBS():
       try:
           global obsprogram
       except obsprogram.CalledProcessError as e:
           username = getpass.getuser()
           print("\n\n[ERROR] Failed to open OBS")
           exit()


def main():
    execGopro()
    execOBS()
    time.sleep(2)
    tkrender()

if __name__ == "__main__":
    main()
