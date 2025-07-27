import os
import sys
import tkinter as tk
import subprocess
import time
import tomllib as toml
import obsws_python as obs

###############################################################################################################################################
# Script by Allen Carson.                                                                                                                     #
# https://github.com/allenc125789/TCCR-OBS-ScreenDeck                                                                                         #
#                                                                                                                                             #
# SELF NOTE: The module to get item id's in obsws doesnt seem to have an ouput, or atleast I can't figure it out.                             #
#     Another way to find item id's in OBS is to export the scene.json file (if not already there) and search it for 'id:'. it'll be a number.#
###############################################################################################################################################

cwd = os.getcwd()
obsdir = 'C:\\Program Files\\obs-studio\\bin\\64bit\\'

###Prepare
#Waits for cameras to connect...
#Starts OBS.
os.chdir(obsdir)
obsprogram = subprocess.Popen([obsdir + 'obs64.exe'])
os.chdir(cwd)
time.sleep(5)

##Sys vars, don't change.
#tkinter
root = tk.Tk()
rootWarn = tk.Toplevel(root)
rootWarn.destroy()
fColumn = tk.Frame(root)
tbTitle = tk.Text(fColumn, height=3, width=60)
tbRoundCount = tk.Text(fColumn, height=1, width=3)
#OBS
titleText = ""
statusLive = False
sourceCAM1 = False
sourceTimer = False
sourceTimerStart = False
sourceRoundCount = False

###Functions
def disableEvent():
    pass

#Resets sysvars to default on when livestream is online or when program is opened.
def resetSysVars():
    cl = obs.ReqClient()
    sourceCAM1 = False
    cl.set_scene_item_enabled(scene_name="Main", item_id=29, enabled=False)
    sourceTimer = False
    cl.set_scene_item_enabled(scene_name="Main", item_id=8, enabled=False)
    sourceTimerStart = False
    cl.set_scene_item_enabled(scene_name="Main", item_id=6, enabled=False)
    #transitionScene
    cl.set_scene_item_enabled(scene_name="Main", item_id=35, enabled=False)

#Starts the livestream, sets as online.
def startStream():
    global statusLive
    resetSysVars()
    if (statusLive == False):
        statusLive = True
        cl = obs.ReqClient()
        cl.set_current_program_scene("Trans-In")
        time.sleep(19)
        cl.set_current_program_scene("Stand-By")
    else:
        pass

#Stops the livestream, sets as offline.
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

#Set scene to 'Stand-By'
def standBy():
    transitionScene()
    cl = obs.ReqClient()
    cl.set_current_program_scene("Stand-By")

#Set scene to 'Main', activates group 'CAM1'.
def CAM1():
    cl = obs.ReqClient()
    transitionScene()
    #CAM1
    cl.set_current_program_scene("Main")
    cl.set_scene_item_enabled(scene_name="Main", item_id=29, enabled=True)

#Set scene to 'Main', activates group 'Timer-Ready'.
def timerHideShow():
    global sourceTimer
    global sourceTimerStart
    cl = obs.ReqClient()
    if (sourceTimerStart == True):
        #TimerStart
        sourceTimerStart = False
        cl.set_scene_item_enabled(scene_name="Main", item_id=6, enabled=False)
        time.sleep(1)
    #Timer
    sourceTimer = (not sourceTimer)
    cl.set_scene_item_enabled(scene_name="Main", item_id=8, enabled=sourceTimer)

def timerStart():
    global sourceTimer
    global sourceTimerStart
    cl = obs.ReqClient()
    if (sourceTimer != True):
        #Timer
        sourceTimer = True
        cl.set_scene_item_enabled(scene_name="Main", item_id=8, enabled=True)
        time.sleep(1)
    #TimerStart
    sourceTimerStart = (not sourceTimerStart)
    cl.set_scene_item_enabled(scene_name="Main", item_id=6, enabled=sourceTimerStart)

#Set scene to 'Main', activates group 'Timer-Start'.
def roundcountHideShow():
    global sourceRoundCount
    cl = obs.ReqClient()
    sourceRoundCount = (not sourceRoundCount)
    cl.set_scene_item_enabled(scene_name="Main", item_id=32, enabled=sourceRoundCount)


def transitionScene():
    cl = obs.ReqClient()
    cl.set_current_program_scene("Main")
    cl.set_scene_item_enabled(scene_name="Main", item_id=35, enabled=True)
    time.sleep(1)
    cl.set_scene_item_enabled(scene_name="Main", item_id=35, enabled=False)

#Resets the title textbox to what's saved in the file. If none is there, one will be created.
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
            titleText = "           TCC, Tulsa Community Combat Robotics            |            Event: XXXXX: 04-08-2025             |            "
            f.write(titleText)
            tbTitle.insert("1.0", titleText)
            pass

#Saves what's in the current textbox to file.
def saveTitle():
    global fColumn
    global tbTitle
    titleText = tbTitle.get("1.0", tk.END)
    with open("title.txt", "w") as f:
        f.write(titleText)
        f.close


#Performs a safe exit, that terminates all child services.
def safeExit():
    #Stops obs
    obsprogram.terminate()
    obsprogram.wait()
    obsprogram.kill()
    #Stops tkinter
    root.quit()

#Closes the Warning window by `tkrenderWarning`.
def closeWarning():
    global rootWarn
    rootWarn.destroy()
    safeExit()

#Renders warning window for closing the program while the livestream is online.
def tkrenderWarning():
    global root
    global statusLive
    global rootWarn
    if (statusLive == True):
        rootWarn = tk.Toplevel(root)
        rootWarn.protocol("WM_DELETE_WINDOW", disableEvent)
        rootWarn.title('WARNING!')
        w = 775
        h = 375

        ws = rootWarn.winfo_screenwidth() # width of the screen
        hs = rootWarn.winfo_screenheight() # height of the screen

        x = (ws) - (w*4)
        y = (hs) - (h/4)

        rootWarn.geometry('%dx%d+%d+%d' % (w, h, x, y))
        lWarning = tk.Label(rootWarn, text="Waning!", font=("Aerial", 30, "bold"))
        lDescription = tk.Label(rootWarn, text="The Livestream is still online. Are you sure you want to Exit now?", font=("Aerial", 10, "bold"))
        btnContinue = tk.Button(rootWarn, text='Continue?', command=closeWarning)
        btnGoBack = tk.Button(rootWarn, text='Go back!', command=rootWarn.destroy)

        lWarning.pack()
        lDescription.pack()
        btnContinue.pack()
        btnGoBack.pack()
        rootWarn.grab_set()
        root.wait_window(rootWarn)
    else:
        safeExit()

#Renders control panel window for OBS
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

    x = (ws) - (w*2)
    y = (hs) - (h)

    # set the dimensions of the screen
    # and where it is placed
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    #Frame for Column
    fColumn.columnconfigure(0, weight=1)
    fColumn.columnconfigure(1, weight=1)
    root.attributes('-topmost', True)

    var1=tk.IntVar()

    #cbOnline/cbOffline frame.
    fState = tk.Frame(fColumn, width=228, height=20)
    fState.grid(row=0, column=0, sticky=tk.W+tk.E, padx=75)
    #Checkboxs to change stream from live-to-offline.
    cbOnline = tk.Checkbutton(fState, text='Online', variable=var1, offvalue=(not statusLive), command=startStream)
    cbOffline = tk.Checkbutton(fState, text='Offline', variable=var1, onvalue=statusLive, command=stopStream)
    #Label for Stream State
    lState = tk.Label(fColumn, text="Stream Status:", font=("Aerial", 30, "bold"))
    lState.grid(row=0, column=0, sticky=tk.W+tk.E, padx=150)


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


    #Buttons for cameras.
    btnStandBy = tk.Button(fColumn, text='Stand-by...',  font=("Aerial", 10, "bold"), command=standBy)
    btnStandBy.grid(row=5, column=0, sticky=tk.W+tk.E)
    btnCam1 = tk.Button(fColumn, text='Cam 1', command=CAM1)
    btnCam1.grid(row=6, column=0, sticky=tk.W+tk.E)
    btnCam2 = tk.Button(fColumn, text='Cam 2')
    btnCam2.grid(row=7, column=0, sticky=tk.W+tk.E)
    btnCam3 = tk.Button(fColumn, text='Cam 3')
    btnCam3.grid(row=8, column=0, sticky=tk.W+tk.E)


    #Buttons for Timer.
    fTimer = tk.Frame(fColumn, width=228, height=50, borderwidth=2, relief="solid")
    fTimer.grid(row=0, column=1, sticky=tk.W+tk.E)
    lTimer = tk.Label(fTimer, text="+Battle Timer+", font=("Aerial", 10, "bold"))
    btnShowHide = tk.Button(fTimer, text='Toggle', command=timerHideShow)
    btnStopStart = tk.Button(fTimer, text='Start/Stop', command=timerStart)

    #Buttons for Round Count.
    froundcount = tk.Frame(fColumn, width=228, height=50, borderwidth=2, relief="solid")
    froundcount.grid(row=1, column=1, sticky=tk.W+tk.E)
    lroundcount = tk.Label(froundcount, text="+Round-Count+", font=("Aerial", 10, "bold"))
    btnRCToggle = tk.Button(froundcount, text='Toggle', command=roundcountHideShow)


    #Button for safe exit.
    btnSafeExit = tk.Button(fColumn, text='Safe Exit', font=("Aerial", 10, "bold"), command=tkrenderWarning)
    btnSafeExit.grid(row=8, column=1, sticky=tk.W+tk.E)

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

    #Round Count Function.
    lroundcount.pack()
    btnRCToggle.pack()

    #Title Function.
    btnTitleReset.pack(side="left")
    btnTitleSave.pack(side="left")


    #Start root GUI window.
    root.mainloop()

#Main Loop
def main():
    time.sleep(2)
    resetSysVars()
    tkrender()

if __name__ == "__main__":
    main()
