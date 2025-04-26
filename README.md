## Description
Allows the Hercules Starlight to be used with Rekordbox on Windows.

This script runs two threads concurrently.

The first thread relays control messages from the Starlight to Rekordbox via a virtual MIDI device. Some messages get modified to match the type of data that Rekordbox expects. I.e. tempo slider and jog wheel direction are inverted on the Starlight.

The second thread relays LED messages from Rekordbox to the Starlight via another virtual device.

This script also lets you browse by holding down the Shift key and moving the side of either jog wheel (pitch bending). This is achieved by modifying the pitch bend message if shift is held down, and mapping that unique message in Rekordbox. Hold shift and press Play/Pause to load the selected track to that deck.

## Installation
1. Install [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html) and add the following virtual devices;
`PIONEER DDJ-SX`
`Starlight Control`
`Starlight LED`
2. Clone this repo and open the directory in cmd.
3. Create the virtual environment;
```python -m venv .venv```
4. Activate the virtual environment;
```.venv\Scripts\activate.bat```
5. Install requirements;
```pip install -r requirements.txt```
6. Open Rekordbox and import the mappings located in the `/Mappings` folder.

## Usage
1. Start loopMIDI.
2. Open the repo directory in cmd.
3. Activate the virtual environment;
```.venv\Scripts\activate.bat```
4. Run rekordstar;
```py rekordstar.py```
5. Start Rekordbox.

> Rekordbox might ask about outdated drivers on startup if the script is running. This is because it thinks a real Pioneer device is connected, and can be safely ignored.

## Customization
Device names and MIDI message handling can be changed in `rekordstar.py`. You can also modify the mappings to add custom functionality. Just remember that the mapping for the control input is separate from the LED output.

## Other
Optionally, you could make a bat file to start loopMIDI and run the script for you. Mine is located in the parent folder of the repo, and looks like this;
```
"C:\Program Files\Tobias Erichsen\loopMIDI\loopMIDI.exe"
call "%~dp0\rekordstar\.venv\Scripts\activate.bat"
python "%~dp0\rekordstar\rekordstar.py"
pause
```

## Troubleshooting
To keep it short, there is no error handling in this script. If you're getting errors;
* Check the list of input and output devices that gets printed when the script runs.
* If any of the previously mentioned device names are missing, make sure your controller is connected, you've added the virtual devices to loopMIDI, and loopMIDI is running.
* If you start Rekordbox without running the script, it will connect to your controller and lock it so the script can't access it. Close Rekordbox and give it a minute to release the controller before running the script again.

## Acknowledgements
Special thanks to [timkontradev](https://github.com/timkondratev/RekordJog) who made the script that inspired rekordstar.