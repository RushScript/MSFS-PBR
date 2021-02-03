from tkinter import *
from tkinter import filedialog
from tkinter import dialog
from SimConnect import *
import sys
import os
import logging
import math
import time
import threading
import json
import webbrowser
import keyboard

# Logging configuration
logging.basicConfig(filename='pbr.log', filemode='w', level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
LOGGER.info("START")

## GUI functions
# Custom dialog function
def customDialog(title, text, strings=('YES', 'NO'), bitmap='question', default=1):
    d = dialog.Dialog(title=title, text=text, bitmap=bitmap, default=default, strings=strings)
    print(strings[d.num])
    return strings[d.num]

# Get the last accessed path
def getDirPath(dirpath):
    path, filename = os.path.split(dirpath)
    return path

# Button 1 function
def btnClickFunction():
    root.filename = filedialog.askopenfilename(initialdir=settings["path"],
                                               title="Select your PBR file",
                                               filetypes=(("PBR files", "*.pbr"), ("all files", "*.*")))
    fpath = root.filename
    if fpath:
        settings["path"] = getDirPath(fpath)
        json.dump(settings, open("settings.json", 'w'))
        btn1["state"] = DISABLED
        btn2["state"] = DISABLED
        btn3["state"] = DISABLED
        btn4["state"] = NORMAL
        btn1["bg"] = "#adf542"
        btn1["fg"] = "#6B6B6B"
        btn2["bg"] = "white"
        btn2["fg"] = "#6B6B6B"
        btn3["bg"] = "white"
        btn3["fg"] = "#6B6B6B"
        btn4["bg"] = "#6B6B6B"
        btn1["text"] = "PBR File loaded"
        logging.info("Auto-Push back PBR file loaded: " + fpath)
        pbplayThd = threading.Thread(target=pbplay, args=(fpath,))
        pbplayThd.start()
    else:
        logging.info("Auto-Push back PBR file loaded: Cancelled by user input")

# Button 2 function
def btnClickFunction2():
    btn1["state"] = DISABLED
    btn2["state"] = DISABLED
    btn3["state"] = DISABLED
    btn4["state"] = NORMAL
    btn1["bg"] = "white"
    btn1["fg"] = "#6B6B6B"
    btn2["bg"] = "#adf542"
    btn2["fg"] = "#6B6B6B"
    btn3["bg"] = "white"
    btn3["fg"] = "#6B6B6B"
    btn4["bg"] = "#6B6B6B"
    pb()

# Button 3 function
def btnClickFunction3():
    ## TODO: Filename bug
    root.filename = filedialog.asksaveasfilename(initialdir=settings["path"],
                                                 title="Select your PBR file",
                                                 filetypes=(("PBR files", "*.pbr"), ("all files", "*.*")))
    if root.filename:
        if str(root.filename).find(".pbr") != -1:
            fpath = root.filename
        else:
            fpath = root.filename + ".pbr"
        settings["path"] = getDirPath(fpath)
        json.dump(settings, open("settings.json", 'w'))
        btn1["state"] = DISABLED
        btn2["state"] = DISABLED
        btn3["state"] = DISABLED
        btn4["state"] = NORMAL
        btn1["bg"] = "white"
        btn1["fg"] = "#6B6B6B"
        btn2["bg"] = "white"
        btn2["fg"] = "#6B6B6B"
        btn3["bg"] = "#adf542"
        btn3["fg"] = "#6B6B6B"
        btn4["bg"] = "#6B6B6B"
        btn3["text"] = "Recording Push Back"
        logging.info("Recording PBR file: " + fpath)
        pbrecThd = threading.Thread(target=pbrec, args=(fpath,))
        pbrecThd.start()
    else:
        logging.info("Recording PBR file: Cancelled by user input")

# Toggles the push back using the GUI button
def tugtglUI():
    tugtgl()
    if recphase is True:
        recstate()
    else:
        pbkstate()

# Toggles the jetway  using the GUI button
def jetwaytglUI():
    jetwaytgl()

# On start GUI function
def startAll():
    global settings
    global settooltip
    try:
        settings = json.load(open("settings.json"))
        if settings["tooltips"] is True:
            settooltip = " \u2713"
        elif settings["tooltips"] is False:
            settooltip = ""
    except:
        settings = {"tooltips": True, "sound": True, "brakes": False, "uiclose": False, "jetclose": False, "control": "modern", "path": getDirPath(os.path.realpath(__file__))}
        if settings["tooltips"] is True:
            settooltip = " \u2713"
        elif settings["tooltips"] is False:
            settooltip = ""
        try:
            json.dump(settings, open("settings.json", 'w'))
        except:
            logging.error(os.path.realpath(__file__)+" settings.json write permissions denied")
            ## TODO: Save into user directory to avoid error

## TODO: to be deleted soon
# Restarts the whole script 
def restartAll():
    if (smconnected == 1):
        smcheck.join()
        sm.exit()
        logging.info("SimConnect:Clean exit")
    os.execv(sys.executable, ['python'] + sys.argv)   
    logging.info("APP:Restart")
    os._exit(0)

# On exit GUI function
def exitAll():
    if (smconnected == 1):
        smcheck.join()
        sm.exit()
        logging.info("SimConnect:Clean exit")
    logging.info("APP:Exit")
    os._exit(0)

# Resets the GUI to the default page
def resetUI():
    pbstp = 0
    recphase = False
    rec = 2
    btn1["state"] = NORMAL
    btn1["fg"] = "white"
    btn1["bg"] = "#6B6B6B"
    btn1["text"] = "Auto-Push Back"
    btn2["state"] = NORMAL
    btn2["fg"] = "white"
    btn2["bg"] = "#6B6B6B"
    btn3["state"] = NORMAL
    btn3["fg"] = "white"
    btn3["bg"] = "#6B6B6B"
    btn3["text"] = "Record Push Back"
    btn4["state"] = DISABLED
    btn4["fg"] = "white"
    btn4["bg"] = "white"
    btn5["state"] = NORMAL
    btn5["fg"] = "white"
    btn5["bg"] = "#6B6B6B"
    logging.info("UI Reset -> Back to main page")

# About menu bar click function
def aboutClickFunction():
    webbrowser.open("https://github.com/RushScript/MSFS-PBR")

# Sim-tooltips menu bar click function
def tooltips():
    if settings["tooltips"] is True:
        settings["tooltips"] = False
        settingsmenu.entryconfigure(1, label="Sim-Tooltips")
        json.dump(settings, open("settings.json", 'w'))
    elif settings["tooltips"] is False:
        settings["tooltips"] = True
        settingsmenu.entryconfigure(1, label="Sim-Tooltips \u2713")
        json.dump(settings, open("settings.json", 'w'))
    
## Core functions
# Simconnect link
def simconnectLink():
    global sm
    global smconnected
    global aq
    global ae
    global tug
    global tugspd
    global tugtgl
    global jetwaytgl
    # Local var used to loop on SimConnect link attempt
    smconnected = 0
    logging.info("SimConnect:Linking to MSFS2020...")
    while True:
        try:
            sm.get_paused()
            smconnected = 1
            lbl2["fg"] = "#adf542"
            lbl2["text"] = "SimConnect: Linked"
        except:
            logging.warning("Simconnect:Connecting...")
            lbl2["fg"] = "#ffc000"
            lbl2["text"] = "SimConnect: Connecting"
            try:
                sm = SimConnect()
                smconnected = 1
                logging.info("SimConnect:Linked")
                lbl2["fg"] = "#adf542"
                lbl2["text"] = "SimConnect: Linked"
                aq = AircraftRequests(sm,  _time=10)  # Aircraft Requests Variable
                ae = AircraftEvents(sm)  # Aircraft Event Variables
                tug = ae.find("KEY_TUG_HEADING")
                tugspd = ae.find("KEY_TUG_SPEED")
                tugtgl = ae.find("TOGGLE_PUSHBACK")
                jetwaytgl = ae.find("TOGGLE_JETWAY")
                return (sm)
            except:
                time.sleep(10)
                lbl2["fg"] = "#ffc000"
                lbl2["text"] = "SimConnect: Not linked"
                logging.info("Retrying in 10sec")
                continue

# Manual Push Back
def pb():
    recphase = False
    logging.info("Manual Push Back started")
    keyboard.add_hotkey("left",
                        lambda: tug(((int(math.degrees(aq.get("PLANE_HEADING_DEGREES_TRUE"))) - 27) % 360 * 11930464)))
    keyboard.add_hotkey("left", lambda: heading('left'))
    keyboard.add_hotkey("right",
                        lambda: tug(((int(math.degrees(aq.get("PLANE_HEADING_DEGREES_TRUE"))) + 27) % 360 * 11930464)))
    keyboard.add_hotkey("right", lambda: heading('right'))
    keyboard.add_hotkey("up", lambda: pbst())
    keyboard.add_hotkey("down", lambda: tugtgl())
    return

# Record Push Back
def pbrec(fpath):
    global recphase
    global recdata
    recphase = True
    recdata = []
    recdata.append(str(aq.get("PLANE_LATITUDE")) + "\n")
    recdata.append(str(aq.get("PLANE_LONGITUDE")) + "\n")
    recdata.append(str(aq.get("PLANE_HEADING_DEGREES_TRUE")) + "\n")
    pbr = open(fpath, 'w')
    logging.info("Record Push Back started")
    # pbr = open(recdata[0].replace('\n', '').replace('.', '')+recdata[1].replace('\n', '').replace('.', '')+'.pbr', 'w')
    keyboard.add_hotkey("left",
                        lambda: tug(((int(math.degrees(aq.get("PLANE_HEADING_DEGREES_TRUE"))) - 27) % 360 * 11930464)))
    keyboard.add_hotkey("left", lambda: heading('left'))
    keyboard.add_hotkey("right",
                        lambda: tug(((int(math.degrees(aq.get("PLANE_HEADING_DEGREES_TRUE"))) + 27) % 360 * 11930464)))
    keyboard.add_hotkey("right", lambda: heading('right'))
    keyboard.add_hotkey("up", lambda: pbst())
    keyboard.add_hotkey("down", lambda: tugtgl())
    while rec > 0:
        try:
            if aq.get("GROUND_VELOCITY") > 0.1:
                time.sleep(rft)
                recdata.append(str(int(math.degrees(aq.get("PLANE_HEADING_DEGREES_TRUE")) % 360 * 11930464)) + "\n")
        except:
            logging.warning("aq.get(""GROUND_VELOCITY"") return null")
    tugspd(0)
    pbr.writelines(recdata)
    pbr.close()
    logging.info("Push back recorded and saved to file: " + fpath)
    if settings["tooltips"] is True:
        sm.sendText("Push back recorded and saved to file: " + fpath)
    logging.info("Record Push Back ended")
    time.sleep(2)
    resetUI()

# Push Back rec state
def recstate():
    global rec
    rec = rec - 1
    if rec == 1 and settings["tooltips"] is True:
        sm.sendText("Release parking brakes")
        sm.sendText("Recording Push back...")
    return rec

# Auto-Push Back
def pbplay(fpath):
    recphase = False
    pbrd = open(fpath, 'r')
    Lines = pbrd.readlines()
    aq.set("PLANE_LATITUDE", float(Lines[0]))
    aq.set("PLANE_LONGITUDE", float(Lines[1]))
    aq.set("PLANE_HEADING_DEGREES_TRUE", float(Lines[2]))
    logging.info("Applying -> Lat: " + str(Lines[0]).replace("\n", ""))
    logging.info("Applying -> Lon: " + str(Lines[1]).replace("\n", ""))
    logging.info("Applying -> Hdg: " + str(Lines[2]).replace("\n", ""))
    time.sleep(2)
    keyboard.add_hotkey("down", lambda: tugtgl())
    count = 0
    contact = 1
    while contact > 0:
        try:
            if aq.get("GROUND_VELOCITY") > 0.1:
                contact = 0
        except:
            pass
    logging.info("Auto-Push back started")
    btn4["state"] = DISABLED
    btn4["bg"] = "white"
    btn4["fg"] = "#6B6B6B"
    for line in Lines:
        count += 1
        if count > 3:
            time.sleep(rft)
            tug(int(line.strip()))
    time.sleep(erft)
    tugtgl()
    logging.info("Auto-Push back ended")
    pbkstate()

# Push Back last steering direction 
def pbst():
    tug = ae.find("KEY_TUG_HEADING")
    if (hdg == "left"):
        tug(((int(math.degrees(aq.get("PLANE_HEADING_DEGREES_TRUE"))) - 3) % 360 * 11930464))
    elif (hdg == "right"):
        tug(((int(math.degrees(aq.get("PLANE_HEADING_DEGREES_TRUE"))) + 3) % 360 * 11930464))
    return

# Push Back last heading update
def heading(trn):
    global hdg
    hdg = trn
    return hdg

## TODO: change def pbkstate to def pbnotify
# Push Back SM notification (Parking Brakes)
def pbkstate():
    global pbstp
    if (pbstp == 0):
        if settings["tooltips"] is True:
            sm.sendText("Release parking brakes")
        pbstp = 1
    else:
        if settings["tooltips"] is True:
            sm.sendText("Set parking brakes")
        tugspd(0)
        pbstp = 0
        time.sleep(2)
        resetUI()

## Code sequence starts here
startAll()

# GUI creation
root = Tk()

# Creates main window
root.geometry('400x390')
root.configure(background='#6B6B6B')
root.title('Push Back Recorder')
root.resizable(width=False, height=False)
root.attributes('-topmost', True)
root.iconbitmap(default="AppIcon.ico")
root.update()

# Creates the Menu Bar
global settingsmenu
menubar = Menu(root)
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Restart", command=restartAll)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=exitAll)
menubar.add_cascade(label="App", menu=filemenu)
settingsmenu = Menu(menubar, tearoff=0)
settingsmenu.add_command(label="Sim-Tooltips"+settooltip, command=tooltips)
menubar.add_cascade(label="Settings", menu=settingsmenu)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About...", command=aboutClickFunction)
menubar.add_cascade(label="Help", menu=helpmenu)

# GUI Buttons
global btn1
global btn2
global btn3
global btn4
global btn5

# Creates Main Page buttons 
btn1 = Button(root, text='Auto-Push Back', bg='#6B6B6B', fg="white", font=('arial', 10, 'normal'),
              command=btnClickFunction)
btn1.place(x=5, y=10)
btn2 = Button(root, text='Manual Push Back', bg='#6B6B6B', fg="white", font=('arial', 10, 'normal'),
              command=btnClickFunction2)
btn2.place(x=5, y=50)
btn3 = Button(root, text='Record Push Back', bg='#6B6B6B', fg="white", font=('arial', 10, 'normal'),
              command=btnClickFunction3)
btn3.place(x=5, y=90)
btn4 = Button(root, text='Toggle / Push Back', state=DISABLED, bg='white', fg="white", font=('arial', 10, 'normal'),
              command=tugtglUI)
btn4.place(x=135, y=10)
btn5 = Button(root, text='Toggle / Jetway', bg='#6B6B6B', fg="white", font=('arial', 10, 'normal'), command=jetwaytglUI)
btn5.place(x=135, y=50)

# Declares Auto-Push Back buttons
btnapb1 = Button(root, text='Click to start Auto-Push Back', bg='#6B6B6B', fg="white", font=('arial', 10, 'normal'),
                 command=btnClickFunction2)
btnapb2 = Button(root, text='Toggle / Jetway', bg='#6B6B6B', fg="white", font=('arial', 10, 'normal'),
                 command=btnClickFunction2)
btnpb1 = Button(root, text='Stop Push Back', bg='#6B6B6B', fg="white", font=('arial', 10, 'normal'),
                command=btnClickFunction2)

# GUI Canvas images
global HowToImg
global HowToImgTail

# Creates "How to manual push back" canvas image 
HowToImg = Canvas(root, height=190, width=380, bd=0, highlightthickness=0, relief='ridge')
picture_file = PhotoImage(file='howto.gif')
HowToImg.create_image(380, 0, anchor=NE, image=picture_file)
HowToImg.place(x=5, y=152)

# Declares "How to auto-push back" canvas image
HowToImgTail = Canvas(root, height=190, width=380, bd=0, highlightthickness=0, relief='ridge')
picture_fileT = PhotoImage(file='howtoTail.gif')
HowToImgTail.create_image(380, 0, anchor=NE, image=picture_fileT)

# Creates "Logo" canvas image
Logo = Canvas(root, height=100, width=100, bd=0, highlightthickness=0, relief='ridge')
picture_fileL = PhotoImage(file='logo.gif')
Logo.create_image(100, 0, anchor=NE, image=picture_fileL)
Logo.place(x=285, y=0)

# GUI Labels
global lbl1
global lbl2
# Creates Main Page labels
lbl1 = Label(root, text='* Remember to keep this window focused while using manual/record push back', bg='#6B6B6B',
             fg="#ffc000", font=('arial', 8, 'normal'))
lbl1.place(x=5, y=362)
lbl2 = Label(root, text='SimConnect: Not linked', bg='#6B6B6B', fg="#ffc000", font=('arial', 9, 'normal'))
lbl2.place(x=250, y=83)

# Declares a new thread for simconnectLink
smcheck = threading.Thread(target=simconnectLink)

# Local variables
hdg = ""
pbstp = 0
recphase = False
rec = 2
rft = 0.300  # Refresh rate
erft = 15    # Error Bug refresh rate

smcheck.start()
root.config(menu=menubar)
root.mainloop()
exitAll()
