from tkinter import *
from tkinter import dialog
from SimConnect import *
import os
import logging
import math
import time
import threading
import keyboard

# Logging configuration
# logging.basicConfig(filename='mhaf.log', filemode='w', level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
LOGGER.info("START")


## GUI functions
# Custom dialog function
def customDialog(title, text, strings=('YES', 'NO'), bitmap='question', default=1):
    d = dialog.Dialog(title=title, text=text, bitmap=bitmap, default=default, strings=strings)
    print (strings[d.num])
    return strings[d.num]

# Button 1 function
def btnClickFunction():
    btn2.destroy()
    btn3.destroy()
    HowToImg.destroy()
    #customDialog("Push Back Recorder", "Please select Tail direction for your Push Back", strings=('Left', 'Straight', 'Right'))
    btn1ab.place(x=35, y=52)
    btn2ab.place(x=75, y=52)
    btn3ab.place(x=140, y=52)
    HowToImgTail.place(x=5, y=152)
    logging.info("Auto-Push back PBR file loaded: ")
    btn1["state"] =  DISABLED
    btn1["bg"] = "#ffc000"
    btn1["fg"] = "#6B6B6B"
    btn1["text"] = "Select Auto-Push Back tail direction"


# Button 2 function
def btnClickFunction2():
    if aq.get("GROUND_VELOCITY") > 0.1:
        tugtgl()
        btn2 = Button(root, text='Start Push Back', bg='#6B6B6B', fg="white", font=('arial', 10, 'normal'), command=btnClickFunction2).place(x=5, y=52)
    elif aq.get("GROUND_VELOCITY") < 0.1:    
        btn1 = tkinter.Button(root, text='Auto-Push Back', state=DISABLED, bg='white', fg="white", font=('arial', 10, 'normal'), command=btnClickFunction).place(x=5, y=12)
        btn3 = Button(root, text='Record Push Back', state=DISABLED, bg='white', fg="white", font=('arial', 10, 'normal'), command=btnClickFunction3).place(x=5, y=92)
        btn2 = Button(root, text='Starting Push Back... (Stop Push Back)', bg='#ffc000', fg="black", font=('arial', 10, 'normal'), command=btnClickFunction2).place(x=5, y=52)
        print('Start Push Back')
        pb()


# Button 3 function
def btnClickFunction3():
    global fpath
    tdct = customDialog("Push Back Recorder", "Please select Tail direction of your Push Back Record", strings=('Left', 'Straight', 'Right'))
    tdct = tdct[0]
    fpath = os.path.dirname(os.path.realpath(__file__))+"\\PBR Data\\longitudelatittude"+tdct+".pbr"
    btn3 = Button(root, text='Recording Push Back... (Stop Recording)', bg='#ffc000', fg="black", font=('arial', 10, 'normal'), command=btnClickFunction3).place(x=5, y=92)
    logging.info("Recording PBR file: "+fpath)




## Core functions
# Simconnect link
def simconnectLink() :
    global sm
    global simconnected
    global aq
    global ae
    global tugtgl
    #Local var used to loop on SimConnect link attempt
    smconnected = 0
    logging.info("SimConnect:Linking to MSFS2020...")
    while True:
        time.sleep(10)
        try:
            sm.get_paused()
            smconnected = 1
            lbl2["fg"] = "#adf542"
            lbl2["text"] = "SimConnect: Linked"
        except:
            logging.warning("Simconnect:Connecting...")
            try:
                sm = SimConnect()
                smconnected = 1
                logging.info("SimConnect:Linked")
                lbl2["fg"] = "#adf542"
                lbl2["text"] = "SimConnect: Linked"
                aq = AircraftRequests(sm) #Aircraft Requests Variable
                ae = AircraftEvents(sm) # Aircraft Event Variables
                tugtgl = ae.find("TOGGLE_PUSHBACK")
                return (sm)
            except:
                lbl2["fg"] = "#ffc000"
                lbl2["text"] = "SimConnect: Not linked"
                logging.info("Retrying in 10sec")
                continue


def pb():
    tgl = ae.find("TOGGLE_PUSHBACK")
    tug = ae.find("KEY_TUG_HEADING")
    keyboard.add_hotkey("left", lambda:tug(((int(math.degrees(aq.get("PLANE_HEADING_DEGREES_TRUE")))-27)%360*11930464)))
    keyboard.add_hotkey("left", lambda:heading('left'))
    keyboard.add_hotkey("right", lambda:tug(((int(math.degrees(aq.get("PLANE_HEADING_DEGREES_TRUE")))+27)%360*11930464)))
    keyboard.add_hotkey("right", lambda:heading('right'))
    keyboard.add_hotkey("up", lambda:pbst())
    keyboard.add_hotkey("down", lambda:tgl())
    keyboard.add_hotkey("down", lambda:pbkstate())
    return

def pbrec():
    global recdata
    recdata = []
    recdata.append(str(aq.get("PLANE_LATITUDE"))+"\n")
    recdata.append(str(aq.get("PLANE_LONGITUDE"))+"\n")
    recdata.append(str(aq.get("PLANE_HEADING_DEGREES_TRUE"))+"\n")
    tgl = ae.find("TOGGLE_PUSHBACK")
    tug = ae.find("KEY_TUG_HEADING")
    pbr = open(recdata[0].replace('\n', '').replace('.', '')+recdata[1].replace('\n', '').replace('.', '')+'.pbr', 'w')
    keyboard.add_hotkey("left", lambda:tug(((int(math.degrees(aq.get("PLANE_HEADING_DEGREES_TRUE")))-27)%360*11930464)))
    keyboard.add_hotkey("left", lambda:heading('left'))
    keyboard.add_hotkey("right", lambda:tug(((int(math.degrees(aq.get("PLANE_HEADING_DEGREES_TRUE")))+27)%360*11930464)))
    keyboard.add_hotkey("right", lambda:heading('right'))
    keyboard.add_hotkey("up", lambda:pbst())
    keyboard.add_hotkey("down", lambda:tgl())
    keyboard.add_hotkey("down", lambda:recstate())
    while rec > 0:
        if aq.get("GROUND_VELOCITY") > 0.1:
            time.sleep(rft)
            recdata.append(str(int(math.degrees(aq.get("PLANE_HEADING_DEGREES_TRUE"))%360*11930464))+"\n")
    pbr.writelines(recdata)
    pbr.close()
    sm.sendText("Push back recorded and saved to file")
    return

def recstate():
    global rec
    rec = rec - 1
    if (rec == 1):
        sm.sendText("Recording Push back...")
    return rec

def pbplay(fpath):
    tgl = ae.find("TOGGLE_PUSHBACK")
    tug = ae.find("KEY_TUG_HEADING")
    pbrd = open(fpath, 'r') 
    Lines = pbrd.readlines()
    aq.set("PLANE_LATITUDE", float(Lines[0]))
    aq.set("PLANE_LONGITUDE", float(Lines[1]))
    aq.set("PLANE_HEADING_DEGREES_TRUE", float(Lines[2]))
    time.sleep(2)
    sm.sendText("Release parking brakes")
    tgl()
    count = 0
    contact = 1
    while contact > 0:
        if aq.get("GROUND_VELOCITY") > 0.1:
            contact = 0
    for line in Lines:
        count += 1
        if count > 3:
            time.sleep(rft)
            tug(int(line.strip()))
    time.sleep(erft)
    sm.sendText("Set parking brakes")
    tgl()
    

def pbst():
    tug = ae.find("KEY_TUG_HEADING")
    if (hdg == "left"):
        tug(((int(math.degrees(aq.get("PLANE_HEADING_DEGREES_TRUE")))-3)%360*11930464))
    elif (hdg == "right"):
        tug(((int(math.degrees(aq.get("PLANE_HEADING_DEGREES_TRUE")))+3)%360*11930464))
    return

def heading(trn):
    global hdg
    hdg = trn
    return hdg


def pbkstate():
    global pbstp
    if (pbstp == 0):
        sm.sendText("Release parking brakes")
        pbstp = 1
    else:
        sm.sendText("Set parking brakes")
        pbstp = 0



    

root = Tk()

# This is the section of code which creates the main window
root.geometry('395x390')
root.configure(background='#6B6B6B')
root.title('Push Back Recorder')
root.resizable(width=False, height=False)
root.attributes('-topmost', True)
root.update()


# GUI Buttons
global btn1
global btn2
global btn3
global btn1ab
global btn2ab
global btn3ab
btn1 = Button(root, text='Auto-Push Back', bg='#6B6B6B', fg="white", font=('arial', 10, 'normal'), command=btnClickFunction)
btn1.place(x=5, y=12)
btn2 = Button(root, text='Start Push Back', bg='#6B6B6B', fg="white", font=('arial', 10, 'normal'), command=btnClickFunction2)
btn2.place(x=5, y=52)
btn3 = Button(root, text='Record Push Back', bg='#6B6B6B', fg="white", font=('arial', 10, 'normal'), command=btnClickFunction3)
btn3.place(x=5, y=92)

btn1ab = Button(root, text='Left', state=DISABLED, bg='white', fg="white", font=('arial', 10, 'normal'), command=btnClickFunction2)
btn2ab = Button(root, text='Straight', state=DISABLED, bg='white', fg="white", font=('arial', 10, 'normal'), command=btnClickFunction3)
btn3ab = Button(root, text='Right', state=DISABLED, bg='white', fg="white", font=('arial', 10, 'normal'), command=btnClickFunction3)


# GUI Canvas images
global HowToImg
global HowToImgTail
HowToImg= Canvas(root, height=190, width=380, bd=0, highlightthickness=0, relief='ridge')
picture_file = PhotoImage(file = 'howto.gif')
HowToImg.create_image(380, 0, anchor=NE, image=picture_file)
HowToImg.place(x=5, y=152)

HowToImgTail= Canvas(root, height=190, width=380, bd=0, highlightthickness=0, relief='ridge')
picture_fileT = PhotoImage(file = 'howtoTail.gif')
HowToImgTail.create_image(380, 0, anchor=NE, image=picture_fileT)

Logo= Canvas(root, height=100, width=100, bd=0, highlightthickness=0, relief='ridge')
picture_fileL = PhotoImage(file = 'logo.gif')  
Logo.create_image(100, 0, anchor=NE, image=picture_fileL)
Logo.place(x=285, y=0)


# GUI Labels
global lbl1
global lbl2
lbl1 = Label(root, text='* Remember to keep this window focused while using manual/record push back', bg='#6B6B6B', fg="#ffc000", font=('arial', 7, 'normal'))
lbl1.place(x=5, y=362)
lbl2 = Label(root, text='SimConnect: Not linked', bg='#6B6B6B', fg="#ffc000", font=('arial', 9, 'normal'))
lbl2.place(x=250, y=83)



smcheck = threading.Thread(target=simconnectLink)
#smcheck.start()


hdg = ""
pbstp = 0
rec = 2
rft = 0.300
erft = 15


root.mainloop()
logging.info("GUI:Exit")
sm.exit()
logging.info("SimConnect:Clean exit")
