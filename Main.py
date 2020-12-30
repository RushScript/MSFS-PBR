from SimConnect import *
import logging
import math
import time
import keyboard


#Logging configuration
#logging.basicConfig(filename='mhaf.log', filemode='w', level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
LOGGER.info("START")



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
    elif (pbstp == 1):
        sm.sendText("Set parking brakes")
        pbstp = 0

def simconnectLink() :
    global sm
    #Local var used to loop on SimConnect link attempt
    smconnected = 0
    logging.info("SimConnect:Linking to MSFS2020...")
    while smconnected < 1:
        try:
            sm = SimConnect()
            smconnected = 1
            logging.info("SimConnect:Linked")
            return (sm)
        except:
            logging.info("Retrying in 10sec")
            time.sleep(10)
            continue


sm = simconnectLink()


aq = AircraftRequests(sm) #Aircraft Requests Variable
ae = AircraftEvents(sm) # Aircraft Event Variables

tugtgl = ae.find("TOGGLE_PUSHBACK")
spd = ae.find("KEY_TUG_SPEED")
hdg = ""
pbstp = 0
rec = 2
rft = 0.300
erft = 15


####    print (aq.get("PLANE_LATITUDE"))
####    print (aq.get("PLANE_LONGITUDE"))

##    
##

pbplay("3615306230296912-5347122154676827.pbr")
