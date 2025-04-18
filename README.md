## Description
Allows the Hercules Starlight to be used with Rekordbox on Windows.

This script runs two threads concurrently.

The first thread relays control messages from the Starlight to Rekordbox via a virtual MIDI device. Some messages get modified to match the type of data that Rekordbox expects. I.e. tempo slider and jog wheel direction are inverted on the Starlight.

The script also lets you browse by holding down the Shift key and moving the side of either jog wheel (pitch bending). This is achieved by modifying the pitch bend message if shift is held down, and mapping that unique message in Rekordbox.

The second thread relays LED messages from Rekordbox to the Starlight via another virtual device.

## Installation
[loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html) and [Mido](https://mido.readthedocs.io/en/stable/) are required.
Mido requires the [python-rtmidi](https://pypi.org/project/python-rtmidi/) and [vswhere](https://pypi.org/project/vswhere/) packages.

Default mappings that work with this script are included. Follow the instructions at the top of the Python file.