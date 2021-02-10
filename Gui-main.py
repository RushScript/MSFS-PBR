from tkinter import *
from tkinter import filedialog
from tkinter import dialog
import tkinter as tk
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
from audioplayer import AudioPlayer

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
    global pbtbtn1
    global pbtbtn2
    global pbtbtn3
    global pbtbtn4
    global pbtbtn5
    global pbtbtn6
    global pbtbtn7
    global pbtbtn8
    global plgbtn1
    global plgbtn2
    global plgbtn3
    global pbtlbl1
    global length
    global pbtWindow
    pbtWindow = tk.Toplevel(root)
    try:
        pbtWindow.geometry('400x550'+str(settings["uipos"][0])+str(settings["uipos"][1]))
    except:
        pbtWindow.geometry('400x550')
    pbtWindow.configure(background='#6B6B6B')
    pbtWindow.title('Planned Push Back')
    pbtWindow.resizable(width=False, height=False)
    pbtWindow.attributes('-topmost', True)
    pbtWindow.iconbitmap(default="AppIcon.ico")
    pbtbtn1image = PhotoImage(file=appdir+"\\Assets\\Images\\pbtbtn1.png")
    pbtbtn2image = PhotoImage(file=appdir+"\\Assets\\Images\\pbtbtn2.png")
    pbtbtn3image = PhotoImage(file=appdir+"\\Assets\\Images\\pbtbtn3.png")
    pbtbtn4image = PhotoImage(file=appdir+"\\Assets\\Images\\pbtbtn4.png")
    pbtbtn5image = PhotoImage(file=appdir+"\\Assets\\Images\\pbtbtn5.png")
    pbtbtn6image = PhotoImage(file=appdir+"\\Assets\\Images\\pbtbtn6.png")
    pbtbtn7image = PhotoImage(file=appdir+"\\Assets\\Images\\pbtbtn7.png")
    pbtbtn8image = PhotoImage(file=appdir+"\\Assets\\Images\\pbtbtn8.png")
    plgbtn1image = PhotoImage(file=appdir+"\\Assets\\Images\\plgbtn1.png")
    plgbtn2image = PhotoImage(file=appdir+"\\Assets\\Images\\plgbtn2.png")
    plgbtn3image = PhotoImage(file=appdir+"\\Assets\\Images\\plgbtn3.png")
    pbtlbl1 = Label(pbtWindow, text='Select type of Push Back:', bg='#6B6B6B',
             fg="#ffc000", font=('segoe ui', 16, 'normal'))
    pbtlbl1.place(x=80, y=0)
    pbtbtn1 = Button(pbtWindow, text='Play recorded Push Back', bg='#6B6B6B', fg="white", font=('segoe ui', 10, 'normal'), compound = TOP, image=pbtbtn1image,
              command=PBTbtnClickFunction)
    pbtbtn2 = Button(pbtWindow, text='    Planned Push Back     ', bg='#6B6B6B', fg="white", font=('segoe ui', 10, 'normal'), compound = TOP, image=pbtbtn2image,
              command=PBTbtnClickFunction2)
    pbtbtn3 = Button(pbtWindow, text='75° Left', bg='#6B6B6B', fg="white", font=('segoe ui', 10, 'normal'), compound = TOP, image=pbtbtn3image,
              command=lambda: PBTbtnClickFunction4(appdir+"\\PBT\\"+length+"-LEFT-75.pbt"))
    pbtbtn4 = Button(pbtWindow, text='75° Right', bg='#6B6B6B', fg="white", font=('segoe ui', 10, 'normal'), compound = TOP, image=pbtbtn4image,
              command=lambda: PBTbtnClickFunction4(appdir+"\\PBT\\"+length+"-RIGHT-75.pbt"))
    pbtbtn5 = Button(pbtWindow, text='90° Left', bg='#6B6B6B', fg="white", font=('segoe ui', 10, 'normal'), compound = TOP, image=pbtbtn5image,
              command=lambda: PBTbtnClickFunction4(appdir+"\\PBT\\"+length+"-LEFT-90.pbt"))
    pbtbtn6 = Button(pbtWindow, text='90° Right', bg='#6B6B6B', fg="white", font=('segoe ui', 10, 'normal'), compound = TOP, image=pbtbtn6image,
              command=lambda: PBTbtnClickFunction4(appdir+"\\PBT\\"+length+"-RIGHT-90.pbt"))
    pbtbtn7 = Button(pbtWindow, text='180° Left', bg='#6B6B6B', fg="white", font=('segoe ui', 10, 'normal'), compound = TOP, image=pbtbtn7image,
              command=lambda: PBTbtnClickFunction4(appdir+"\\PBT\\"+length+"-LEFT-180.pbt"))
    pbtbtn8 = Button(pbtWindow, text='180° Right', bg='#6B6B6B', fg="white", font=('segoe ui', 10, 'normal'), compound = TOP, image=pbtbtn8image,
              command=lambda: PBTbtnClickFunction4(appdir+"\\PBT\\"+length+"-RIGHT-180.pbt"))
    plgbtn1 = Button(pbtWindow, text='Short', bg='#6B6B6B', fg="white", font=('segoe ui', 10, 'normal'), compound = TOP, image=plgbtn1image,
              command=lambda: PBTbtnClickFunction3("SMALL"))
    plgbtn2 = Button(pbtWindow, text='Medium', bg='#6B6B6B', fg="white", font=('segoe ui', 10, 'normal'), compound = TOP, image=plgbtn2image,
              command=lambda: PBTbtnClickFunction3("MEDIUM"))
    plgbtn3 = Button(pbtWindow, text='Long', bg='#6B6B6B', fg="white", font=('segoe ui', 10, 'normal'), compound = TOP, image=plgbtn3image,
              command=lambda: PBTbtnClickFunction3("LARGE"))
    pbtbtn1.place(x=120, y=115)
    pbtbtn2.place(x=120, y=280)
    pbtWindow.grab_set()
    pbtWindow.mainloop()
    pbtWindow.destroy()
    
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
    pbThd = threading.Thread(target=pb)
    pbThd.start()

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
        json.dump(settings, open("pbr.config", 'w'))
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

# PBT Button 1 function
def PBTbtnClickFunction():
    root.filename = filedialog.askopenfilename(initialdir=settings["path"],
                                               title="Select your Push Back Recorder file",
                                               filetypes=(("Record file", "*.pbr"), ("Template file", "*.pbt")))
    fpath = root.filename
    if fpath:
        settings["path"] = getDirPath(fpath)
        json.dump(settings, open("pbr.config", 'w'))
        if str(fpath).find(".pbr") != -1:
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
        elif str(fpath).find(".pbt") != -1:
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
            btn1["text"] = "PBT File loaded"
            logging.info("Auto-Push back PBT file loaded: " + fpath)
            pbplayTemplateThd = threading.Thread(target=pbplayT, args=(fpath,))
            pbplayTemplateThd.start()
        else:
            logging.warning("Invalid Auto-Push back PBR file")
        pbtWindow.destroy()
    else:
        logging.info("Auto-Push back PBR file loaded: Cancelled by user input")

# PBT Button 2 Length function
def PBTbtnClickFunction2():
    pbtlbl1["text"] = " Select Push Back length:"
    pbtbtn1["state"] = DISABLED
    pbtbtn1.place_forget()
    pbtbtn2["state"] = DISABLED
    pbtbtn2.place_forget()
    plgbtn1.place(x=135, y=380)
    plgbtn2.place(x=135, y=215)
    plgbtn3.place(x=135, y=50)

# PBT Button 3 Template select function
def PBTbtnClickFunction3(lgth):
    global length
    length = lgth
    pbtlbl1["text"] = "Select Push Back direction:"
    plgbtn1["state"] = DISABLED
    plgbtn1.place_forget()
    plgbtn2["state"] = DISABLED
    plgbtn2.place_forget()
    plgbtn3["state"] = DISABLED
    plgbtn3.place_forget()
    pbtbtn3.place(x=60, y=45)
    pbtbtn4.place(x=205, y=45)
    pbtbtn5.place(x=60, y=210)
    pbtbtn6.place(x=205, y=210)
    pbtbtn7.place(x=60, y=375)
    pbtbtn8.place(x=205, y=375)
    print(length)

# PBT Button 4 Template launch function
def PBTbtnClickFunction4(fpath):
    pbtWindow.destroy()
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
    btn1["text"] = "PBT File loaded"
    logging.info("Auto-Push back PBT file loaded: " + fpath)
    pbplayTemplateThd = threading.Thread(target=pbplayT, args=(fpath,))
    pbplayTemplateThd.start()
    

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
        unfreeze()
    except:
        pass
    try:
        settings = json.load(open("pbr.config"))
        if settings["tooltips"] is True:
            settooltip = " \u2713"
        elif settings["tooltips"] is False:
            settooltip = ""
    except:
        settings = {"tooltips": True, "sound": True, "brakes": False, "uiclose": False, "jetclose": False, "control": "modern", "path": getDirPath(os.path.realpath(__file__))+"\\PBR", "uipos": ""}
        if settings["tooltips"] is True:
            settooltip = " \u2713"
        elif settings["tooltips"] is False:
            settooltip = ""
        try:
            json.dump(settings, open("pbr.config", 'w'))
        except:
            logging.error(os.path.realpath(__file__)+" pbr.config write permissions denied")
            ## TODO: Save into user directory to avoid error

## TODO: to be deleted soon
# Restarts the whole script 
def restartAll():
    global smconnected
    if root.winfo_x() > 0:
        x = "+"+str(root.winfo_x())
    else:
        x = str(root.winfo_x())
    if root.winfo_y() > 0:
        y = "+"+str(root.winfo_y())
    else:
        y = str(root.winfo_y())
    settings["uipos"] = (x, y)
    json.dump(settings, open("pbr.config", 'w'))
    if (smconnected == 1):
        smcheck.join()
        sm.exit()
        logging.info("SimConnect:Clean exit")
    try:
        os.execv(sys.executable, ['python'] + sys.argv)   
    except:
        logging.error("os.execv(sys.executable, ['python'] + sys.argv) - Could not restart the App")
    logging.info("APP:Restart")
    os._exit(0)

# On exit GUI function
def exitAll():
    global smconnected
    if root.winfo_x() > 0:
        x = "+"+str(root.winfo_x())
    else:
        x = str(root.winfo_x())
    if root.winfo_y() > 0:
        y = "+"+str(root.winfo_y())
    else:
        y = str(root.winfo_y())
    settings["uipos"] = (x, y)
    json.dump(settings, open("pbr.config", 'w'))
    if (smconnected == 1):
        unfreeze()
        smcheck.join()
        sm.exit()
        logging.info("SimConnect:Clean exit")
    logging.info("APP:Exit")
    os._exit(0)

# Resets the GUI to the default page
def resetUI():
    global settings
    global settooltip
    global smconnected
    global recdata
    global phdgbl
    global rec
    global alltime
    global start
    global stp
    global hdg
    global steps
    global pbstp
    pbstp = 0
    stp = 0
    start = 0
    alltime = 0
    hdg = ""
    recphase = False
    rec = 2
    steps = 0
    phdgbl = 0
    try:
        recdata.clear()
    except:
        pass
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
        json.dump(settings, open("pbr.config", 'w'))
    elif settings["tooltips"] is False:
        settings["tooltips"] = True
        settingsmenu.entryconfigure(1, label="Sim-Tooltips \u2713")
        json.dump(settings, open("pbr.config", 'w'))
    
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
    global pkbrakes
    global freezetgl
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
                lbl2["text"] = "    SimConnect: Linked"
                aq = AircraftRequests(sm)  # Aircraft Requests Variable
                ae = AircraftEvents(sm)  # Aircraft Event Variables
                tug = ae.find("KEY_TUG_HEADING")
                tugspd = ae.find("KEY_TUG_SPEED")
                tugtgl = ae.find("TOGGLE_PUSHBACK")
                jetwaytgl = ae.find("TOGGLE_JETWAY")
                pkbrakes = ae.find("PARKING_BRAKES")
                freezetgl = ae.find("FREEZE_LATITUDE_LONGITUDE_TOGGLE")
                return (sm)
            except:
                time.sleep(10)
                lbl2["fg"] = "#ffc000"
                lbl2["text"] = "SimConnect: Not linked"
                logging.info("Retrying in 10sec")
                continue

# Manual Push Back
def pb():
    global recphase
    global phdgbl
    global pbstp
    recphase = False
    logging.info("Manual Push Back started")
    keyboard.add_hotkey("down", lambda: tugtglUI())
    while pbstp < 0:
        time.sleep(0.500)
        continue
    keyboard.unhook_all()
    time.sleep(18)
    pbphase(2, False)
    contact = 0
    while pbstp > 0:
        gs = aq.find("GROUND_VELOCITY")
        gs.time = smrft
        gs = aq.get("GROUND_VELOCITY")
        pbk = aq.find("BRAKE_PARKING_INDICATOR")
        pbk.time = smrft
        pbk = aq.get("BRAKE_PARKING_INDICATOR")
        try:
            if gs > 0.1:
                if (contact == 0):
                    freezetgl()
                    contact = 1
                    time.sleep(5)
                    if settings["tooltips"] is True:
                        sm.sendText("Release parking brakes")
                    pbphase(3, True)
                    while (pbk > 0.0):
                        pbk = aq.find("BRAKE_PARKING_INDICATOR")
                        pbk.time = smrft
                        pbk = aq.get("BRAKE_PARKING_INDICATOR")
                        time.sleep(1)
                        if (pbk < 1.0):
                            if settings["tooltips"] is True:
                                sm.sendText("Starting push back")
                            pbphase(4, True)
                            time.sleep(4)
                            keyboard.add_hotkey("left", lambda: tug(((int(math.degrees(aq.get("PLANE_HEADING_DEGREES_TRUE"))) - 27) % 360 * 11930464)))
                            keyboard.add_hotkey("left", lambda: heading('left'))
                            keyboard.add_hotkey("right", lambda: tug(((int(math.degrees(aq.get("PLANE_HEADING_DEGREES_TRUE"))) + 27) % 360 * 11930464)))
                            keyboard.add_hotkey("right", lambda: heading('right'))
                            keyboard.add_hotkey("up", lambda: pbst())
                            keyboard.add_hotkey("down", lambda: tugtglUI())
                            freezetgl()
        except:
            logging.warning("aq.get(""GROUND_VELOCITY"") return null")
            pass
        while contact > 0:
            gs = aq.find("GROUND_VELOCITY")
            gs.time = smrft
            gs = aq.get("GROUND_VELOCITY")
            pbk = aq.find("BRAKE_PARKING_INDICATOR")
            pbk.time = smrft
            pbk = aq.get("BRAKE_PARKING_INDICATOR")
            phd = aq.find("PLANE_HEADING_DEGREES_TRUE")
            phd.time = smrft
            phd = aq.get("PLANE_HEADING_DEGREES_TRUE")
            phdgbl = phd
            if (pbstp == 2):
                tugtgl()
                keyboard.unhook_all()
                freezetgl()
                contact = -1
                pbk = aq.find("BRAKE_PARKING_INDICATOR")
                pbk.time = smrft
                pbk = aq.get("BRAKE_PARKING_INDICATOR")
                time.sleep(1)
            while contact < 0:
                pbk = aq.find("BRAKE_PARKING_INDICATOR")
                pbk.time = smrft
                pbk = aq.get("BRAKE_PARKING_INDICATOR")
                time.sleep(1)
                try:
                    if pbk > 0.0:
                        time.sleep(5)
                        tugtgl()
                        freezetgl()
                        contact = 0
                        time.sleep(15)
                        if settings["tooltips"] is True:
                            sm.sendText("Tug disconnected. Have a safe flight!")
                        pbphase(6, True)
                        time.sleep(5)
                        break
                except:
                    logging.warning("aq.get(""BRAKE_PARKING_INDICATOR"") return null")
                    pass
    restartAll()
            
# Record Push Back
def pbrec(fpath):
    global recphase
    global recdata
    global phdgbl
    global rec
    global alltime
    global start
    global stp
    stp = 0
    start = 0
    alltime = 0
    contact = 0
    recphase = True
    recdata = {"longitude": [], "latitude": [], "trueheading": [], "steps": [], "heading": [], "time": [], "direction": [], "heading": []}
    recdata["longitude"].append(aq.get("PLANE_LONGITUDE"))
    recdata["latitude"].append(aq.get("PLANE_LATITUDE"))
    recdata["trueheading"].append(aq.get("PLANE_HEADING_DEGREES_TRUE"))
    logging.info("Record Push Back started")
    # pbr = open(recdata[0].replace('\n', '').replace('.', '')+recdata[1].replace('\n', '').replace('.', '')+'.pbr', 'w')
    keyboard.add_hotkey("down", lambda: tugtglUI())
    while rec > 0:
        gs = aq.find("GROUND_VELOCITY")
        gs.time = smrft
        gs = aq.get("GROUND_VELOCITY")
        pbk = aq.find("BRAKE_PARKING_INDICATOR")
        pbk.time = smrft
        pbk = aq.get("BRAKE_PARKING_INDICATOR")
        phd = aq.find("PLANE_HEADING_DEGREES_TRUE")
        phd.time = smrft
        phd = aq.get("PLANE_HEADING_DEGREES_TRUE")
        phdgbl = phd
        try:
            if gs > 0.1:
                if (contact == 0):
                    freezetgl()
                    if settings["tooltips"] is True:
                        sm.sendText("Release parking brakes")
                    while (pbk > 0.0):
                        pbk = aq.find("BRAKE_PARKING_INDICATOR")
                        pbk.time = smrft
                        pbk = aq.get("BRAKE_PARKING_INDICATOR")
                        if (pbk < 1.0):
                            contact = 1
                            freezetgl()
                            start = time.time()
                            logging.info("Tick-Timer started")
                            keyboard.add_hotkey("left", lambda: stprec(alltime, "left"))
                            keyboard.add_hotkey("left", lambda: heading('left'))
                            keyboard.add_hotkey("right", lambda: stprec(alltime, "right"))
                            keyboard.add_hotkey("right", lambda: heading('right'))
                            keyboard.add_hotkey("up", lambda: stprec(alltime, "straight"))
                            keyboard.add_hotkey("down", lambda: stprec(alltime, "stop"))
                        time.sleep(1)
                alltime =+ time.time() - start
        except:
            logging.warning("aq.get(""GROUND_VELOCITY"") return null")
            pass
        time.sleep(smrft / 1000)
    keyboard.unhook_all()
    tugspd(0)
    freezetgl()
    time.sleep(1)
    if settings["tooltips"] is True:
        sm.sendText("Set parking brakes")
    pbk = aq.find("BRAKE_PARKING_INDICATOR")
    pbk.time = smrft
    pbk = aq.get("BRAKE_PARKING_INDICATOR")
    while (pbk < 1.0):
        pbk = aq.find("BRAKE_PARKING_INDICATOR")
        pbk.time = smrft
        pbk = aq.get("BRAKE_PARKING_INDICATOR")
        if (pbk > 0.0):
            freezetgl()
            tugtgl()
        time.sleep(1)
    json.dump(recdata, open(fpath, 'w'))
    logging.info("Push back recorded and saved to file: " + fpath)
    if settings["tooltips"] is True:
        sm.sendText("Push back recorded and saved to file: " + fpath)
    logging.info("Record Push Back ended")
    restartAll()

# Push Back rec state
def recstate():
    global rec
    rec = rec - 1
    if (rec == 1 and settings["tooltips"] is True):
        sm.sendText("Tug is on his way")
        sm.sendText("Recording Push back...")
    elif rec == 0:
        tugtgl()
    return rec

def stprec(rectime, turn):
    global stp
    global rec
    global hdg
    global phdgbl
    global recdata
    if (turn == "left"):
        tug(((int(math.degrees(phdgbl)) - 27) % 360 * 11930464))
        recdata["steps"] = stp
        recdata["time"].append(rectime)
        recdata["direction"].append(turn)
        recdata["heading"].append(27)
        stp += 1
    elif (turn == "right"):
        tug(((int(math.degrees(phdgbl)) + 27) % 360 * 11930464))
        recdata["steps"] = stp
        recdata["time"].append(rectime)
        recdata["direction"].append(turn)
        recdata["heading"].append(27)
        stp += 1
    elif (turn == "straight") and (hdg == "left"):
        tug(((int(math.degrees(phdgbl)) - 3) % 360 * 11930464))
        recdata["steps"] = stp
        recdata["time"].append(rectime)
        recdata["direction"].append(hdg)
        recdata["heading"].append(3)
        stp += 1
    elif (turn == "straight") and (hdg == "right"):
        tug(((int(math.degrees(phdgbl)) + 3) % 360 * 11930464))
        recdata["steps"] = stp
        recdata["time"].append(rectime)
        recdata["direction"].append(hdg)
        recdata["heading"].append(3)
        stp += 1
    elif (turn == "stop"):
        if (rec == 0):
            recdata["steps"] = stp
            recdata["time"].append(rectime)
            recdata["direction"].append("straight")
            recdata["heading"].append(0)
            stp = 0
    time.sleep(1)
    
# Auto-Push Back PBR File
def pbplay(fpath):
    global start
    global steps
    global start
    global recphase
    recphase = False
    pbr = json.load(open(fpath))
    time.sleep(1)
    steps = 0
    keyboard.add_hotkey("down", lambda: tugtglUI())
    contact = 1
    start = 0
    aq.set("PLANE_LATITUDE",  pbr["latitude"][0])
    aq.set("PLANE_LONGITUDE", pbr["longitude"][0])
    aq.set("PLANE_HEADING_DEGREES_TRUE", pbr["trueheading"][0])
    while pbstp < 0:
        time.sleep(0.500)
        continue
    keyboard.unhook_all()
    time.sleep(18)
    pbphase(2, False)
    while contact > 0:
        gs = aq.find("GROUND_VELOCITY")
        gs.time = smrft
        gs = aq.get("GROUND_VELOCITY")
        try:
            if gs > 0.1:
                freezetgl()
                contact = -1
                time.sleep(5)
                if settings["tooltips"] is True:
                    sm.sendText("Release parking brakes")
                pbphase(3, False)
        except:
            logging.warning("aq.get(""GROUND_VELOCITY"") return null")
            pass
    while contact < 0:
        pbk = aq.find("BRAKE_PARKING_INDICATOR")
        pbk.time = smrft
        pbk = aq.get("BRAKE_PARKING_INDICATOR")
        time.sleep(4)
        try:
            if pbk < 1.0:
                if settings["tooltips"] is True:
                    sm.sendText("Starting push back")
                pbphase(4, True)
                time.sleep(4)
                freezetgl()
                start = time.time()
                logging.info("Tick-Timer started")
                contact = 0
        except:
            logging.warning("aq.get(""BRAKE_PARKING_INDICATOR"") return null")
            pass
    logging.info("Auto-Push back template started")
    btn4["state"] = DISABLED
    btn4["bg"] = "white"
    btn4["fg"] = "#6B6B6B"
    while steps <= pbr["steps"]:
        gs = aq.find("GROUND_VELOCITY")
        gs.time = smrft
        gs = aq.get("GROUND_VELOCITY")
        if time.time() - start >= pbr["time"][steps]:
            if (pbr["direction"][steps] == "left"):
                tug(((int(math.degrees(aq.get("PLANE_HEADING_DEGREES_TRUE"))) - pbr["heading"][steps]) % 360 * 11930464))
            elif (pbr["direction"][steps] == "right"):
                tug(((int(math.degrees(aq.get("PLANE_HEADING_DEGREES_TRUE"))) + pbr["heading"][steps]) % 360 * 11930464))
            else:
                pass
            steps += 1
        #print("STEP:", steps)
        time.sleep(smrft / 1000)
    contact = -1
    freezetgl()
    pbkstate()
    while contact < 0:
        pbk = aq.find("BRAKE_PARKING_INDICATOR")
        pbk.time = smrft
        pbk = aq.get("BRAKE_PARKING_INDICATOR")
        time.sleep(4)
        try:
            if pbk > 0.0:
                freezetgl()
                contact = 0
                tugtgl()
                time.sleep(15)
                if settings["tooltips"] is True:
                    sm.sendText("Tug disconnected. Have a safe flight!")
                pbphase(6, True)
        except:
            logging.warning("aq.get(""BRAKE_PARKING_INDICATOR"") return null")
            pass 
    logging.info("Auto-Push back template ended")
    restartAll()

# Auto-Push Back PBT File
def pbplayT(fpath):
    global recphase
    recphase = False
    pbt = json.load(open(fpath))
    time.sleep(1)
    steps = 0
    keyboard.add_hotkey("down", lambda: tugtglUI())
    contact = 1
    feets = 0
    while pbstp < 0:
        time.sleep(0.500)
        continue
    keyboard.unhook_all()
    time.sleep(18)
    pbphase(2, False)
    while contact > 0:
        gs = aq.find("GROUND_VELOCITY")
        gs.time = smrft
        gs = aq.get("GROUND_VELOCITY")
        try:
            if gs > 0.1:
                freezetgl()
                contact = -1
                time.sleep(5)
                if settings["tooltips"] is True:
                    sm.sendText("Release parking brakes")
                pbphase(3, True)
        except:
            logging.warning("aq.get(""GROUND_VELOCITY"") return null")
            pass
    while contact < 0:
        pbk = aq.find("BRAKE_PARKING_INDICATOR")
        pbk.time = smrft
        pbk = aq.get("BRAKE_PARKING_INDICATOR")
        time.sleep(4)
        try:
            if pbk < 1.0:
                if settings["tooltips"] is True:
                    sm.sendText("Starting push back")
                pbphase(4, True)
                time.sleep(4)
                freezetgl()
                contact = 0
        except:
            logging.warning("aq.get(""BRAKE_PARKING_INDICATOR"") return null")
            pass          
    logging.info("Auto-Push back template started")
    btn4["state"] = DISABLED
    btn4["bg"] = "white"
    btn4["fg"] = "#6B6B6B"
    while steps < pbt["steps"][0] + 1:
        gs = aq.find("GROUND_VELOCITY")
        gs.time = smrft
        gs = aq.get("GROUND_VELOCITY")
        feets += gs       
        if feets >= pbt["feets"][steps] * 10:
            if (pbt["direction"][steps] == "left"):
                tug(((int(math.degrees(aq.get("PLANE_HEADING_DEGREES_TRUE"))) - pbt["heading"][steps]) % 360 * 11930464))
            elif (pbt["direction"][steps] == "right"):
                tug(((int(math.degrees(aq.get("PLANE_HEADING_DEGREES_TRUE"))) + pbt["heading"][steps]) % 360 * 11930464))
            else:
                pass
            steps += 1
        time.sleep(smrft / 1000)
    contact = -1
    keyboard.unhook_all()
    freezetgl()
    pbkstate()
    while contact < 0:
        pbk = aq.find("BRAKE_PARKING_INDICATOR")
        pbk.time = smrft
        pbk = aq.get("BRAKE_PARKING_INDICATOR")
        time.sleep(1)
        try:
            if pbk > 0.0:
                time.sleep(5)
                freezetgl()
                contact = 0
                tugtgl()
                time.sleep(15)
                if settings["tooltips"] is True:
                    sm.sendText("Tug disconnected. Have a safe flight!")
                pbphase(6, True)
                time.sleep(6)
                restartAll()
        except:
            logging.warning("aq.get(""BRAKE_PARKING_INDICATOR"") return null")
            pass
    print(feets)
    logging.info("Auto-Push back template ended")

# Push Back last steering direction 
def pbst():
    tug = ae.find("KEY_TUG_HEADING")
    if (hdg == "left"):
        tug(((int(math.degrees(phdgbl)) - 3) % 360 * 11930464))
    elif (hdg == "right"):
        tug(((int(math.degrees(phdgbl)) + 3) % 360 * 11930464))
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
            sm.sendText("Tug is on his way")
        pbphase(1, False)
        pbstp += 1
    else:
        pbstp += 1
        if settings["tooltips"] is True:
            sm.sendText("Push back completed, set parking brakes")
        keyboard.unhook_all()
        pbphase(5, True)
        tugspd(0)
        pbstp = 0
        time.sleep(2)

def pbphase(phase, wait):
    global comms
    comms = AudioPlayer(appdir+"\\Assets\\Audio\\"+str(phase)+".mp3")
    comms.volume = volset
    comms.play(block=wait)
    print(appdir+"\\Assets\\Audio\\"+str(phase)+".mp3")

def unfreeze():
    if (aq.get("IS_LATITUDE_LONGITUDE_FREEZE_ON") == 1.0):
        freezetgl()
        
        

## Code sequence starts here
# Gets the App Directory path
appdir = getDirPath(os.path.realpath(__file__))
#############################
startAll()

# GUI creation
root = Tk()

# Creates main window
try:
    root.geometry('460x390'+str(settings["uipos"][0])+str(settings["uipos"][1]))
except:
    root.geometry('460x390')
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
btn1image = PhotoImage(file=appdir+"\\Assets\\Images\\btn1.png")
btn2image = PhotoImage(file=appdir+"\\Assets\\Images\\btn2.png")
btn3image = PhotoImage(file=appdir+"\\Assets\\Images\\btn3.png")
btn4image = PhotoImage(file=appdir+"\\Assets\\Images\\btn4.png")
btn5image = PhotoImage(file=appdir+"\\Assets\\Images\\btn5.png")
btn1 = Button(root, text='Auto-Push Back', bg='#6B6B6B', fg="white", font=('segoe ui', 10, 'normal'), compound = LEFT, image=btn1image,
              command=btnClickFunction)
btn1.place(x=5, y=10)
btn2 = Button(root, text='Manual Push Back', bg='#6B6B6B', fg="white", font=('segoe ui', 10, 'normal'), compound = LEFT, image=btn2image,
              command=btnClickFunction2)
btn2.place(x=5, y=55)
btn3 = Button(root, text='Record Push Back', bg='#6B6B6B', fg="white", font=('segoe ui', 10, 'normal'), compound = LEFT, image=btn3image, 
              command=btnClickFunction3)
btn3.place(x=5, y=100)
btn4 = Button(root, text='Toggle / Push Back', state=DISABLED, bg='white', fg="white", font=('segoe ui', 10, 'normal'), compound = LEFT, image=btn4image,
              command=tugtglUI)
btn4.place(x=170, y=10)
btn5 = Button(root, text='Toggle / Jetway', bg='#6B6B6B', fg="white", font=('segoe ui', 10, 'normal'), compound = LEFT, image=btn5image, command=jetwaytglUI)
btn5.place(x=170, y=55)

# Declares Auto-Push Back buttons
btnapb1 = Button(root, text='Click to start Auto-Push Back', bg='#6B6B6B', fg="white", font=('segoe ui', 10, 'normal'),
                 command=btnClickFunction2)
btnapb2 = Button(root, text='Toggle / Jetway', bg='#6B6B6B', fg="white", font=('segoe ui', 10, 'normal'),
                 command=btnClickFunction2)
btnpb1 = Button(root, text='Stop Push Back', bg='#6B6B6B', fg="white", font=('segoe ui', 10, 'normal'),
                command=btnClickFunction2)

# GUI Canvas images
global HowToImg
global HowToImgTail

# Creates "How to manual push back" canvas image 
HowToImg = Canvas(root, height=190, width=380, bd=0, highlightthickness=0, relief='ridge')
picture_file = PhotoImage(file=appdir+"\\Assets\\Images\\howto.gif")
HowToImg.create_image(380, 0, anchor=NE, image=picture_file)
HowToImg.place(x=35, y=152)

### Declares "How to auto-push back" canvas image
##HowToImgTail = Canvas(root, height=190, width=380, bd=0, highlightthickness=0, relief='ridge')
##picture_fileT = PhotoImage(file='howtoTail.gif')
##HowToImgTail.create_image(380, 0, anchor=NE, image=picture_fileT)

# Creates "Logo" canvas image
Logo = Canvas(root, height=100, width=100, bd=0, highlightthickness=0, relief='ridge')
picture_fileL = PhotoImage(file=appdir+"\\Assets\\Images\\logo.gif")
Logo.create_image(100, 0, anchor=NE, image=picture_fileL)
Logo.place(x=340, y=10)

# GUI Labels
global lbl1
global lbl2
# Creates Main Page labels
lbl1 = Label(root, text='* Remember to keep this window focused while using manual/record push back', bg='#6B6B6B',
             fg="#ffc000", font=('segoe ui', 9, 'normal'))
lbl1.place(x=15, y=362)
lbl2 = Label(root, text='SimConnect: Not linked', bg='#6B6B6B', fg="#ffc000", font=('segoe ui', 9, 'normal'))
lbl2.place(x=320, y=113)

# Declares a new threads
smcheck = threading.Thread(target=simconnectLink)

# Local variables
volset = 90
hdg = ""
pbstp = 0
recphase = False
rec = 2
rft = 0.165     # PBR Read Refresh rate
wft = 0.100     # PBR Write Refresh rate
smrft = 50      # SimConnect Refresh rate
erft = 15       # Error Bug refresh rate

smcheck.start()
root.config(menu=menubar)
root.mainloop()
exitAll()
