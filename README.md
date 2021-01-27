# MSFS-PBR
Microsoft Flight Simulator 2020 - Push Back Recorder

Push Back Recorder is an MSFS2020 Push Back utility add-on which allows you to record and playback your push backs


## What can i do with Push Back Recorder?
- Auto-Push Back: Select a recorded PBR file and playback your push backs
- Manual Push Back: Use your keyboard keys to perform a manual push back
- Record Push Back: Record your push back using your keyboard keys and save your PBR file so it can be played back with the Auto-Push Back feature later on
- Toggle / Push Back: Toggles the push back tug
- Toggle / Jetway: Toggles the jetway connection (If available at your spot)


## Requirements (If you plan to use the source code)
- Run pbrsetupxxx.exe and complete the install wizard
- Please keep the default install path to avoid issues with the log generator 


## Requirements (If you plan to use the source code)
- [Python 3.8.7](https://www.python.org/downloads/release/python-387/)
- [Python-SimConnect](https://github.com/odwdinc/Python-SimConnect)
- [keyboard](https://github.com/boppreh/keyboard)
- [Auto PY to EXE](https://github.com/brentvollebregt/auto-py-to-exe)
- [Inno Setup](https://jrsoftware.org/isinfo.php)


## Known issues
- Play back is not accurate on long push backs 
- Play back turns a bit too early and sets the plane slightly to the left
- PBR wont reconnect after losing the link with SimConnect
- Log error: Could not create pbr.log (Use the default install path to avoid this issue)