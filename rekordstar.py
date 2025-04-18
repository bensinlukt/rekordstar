import mido
import threading

# 1. Start loopMIDI and create the virtual MIDI devices below
# 2. Run this script
# 3. Start Rekordbox
# 4. Open the MIDI window and import mappings to the corresponding devices
#    Default MIDI mappings for Rekordbox can be found in /Mappings
#    - The DDJ-SX mapping is completely empty, and only exists to receive jog messages
#    - The Control mapping is what receives control messages from this script
#    - The LED mapping is what sends output (LED) messages to this script, which passes them on to the controller

PHYSICAL_MIDI_DEVICE =       "DJControl Starlight"   # The name of your physical MIDI controller
VIRTUAL_JOGWHEEL_DEVICE =    "PIONEER DDJ-SX"        # Create a virtual device in loopMIDI with this name, and create an empty mapping for it in Rekordbox to receive jog messages
VIRTUAL_CONTROL_DEVICE =     "Starlight Control"     # Create a virtual device in loopMIDI with this name, and create a mapping in Rekordbox to receive Input messages to this device
VIRTUAL_LED_DEVICE =         "Starlight LED"         # Create a virtual device in loopMIDI with this name, and create a mapping in Rekordbox to send Output messages to this device

class Relay(threading.Thread):
    def __init__(self, input, output):
        super(Relay, self).__init__()
        self.inport = mido.open_input(input)
        self.outport = mido.open_output(output)

    def run(self):
        for msg in self.inport:
            self.outport.send(msg)

class Translator(threading.Thread):
    def __init__(self, input, output_jogwheel, output_other):
        super(Translator, self).__init__()
        self.inport = mido.open_input(input)
        self.outport_jogwheel = mido.open_output(output_jogwheel)
        self.outport_control = mido.open_output(output_other)

    def run(self):
        for msg in self.inport:
            isNote              = 'note' in msg.type
            isControl           = msg.type == 'control_change'

            isJogTouch          = isNote and msg.note == 8
            isJogBend           = isControl and msg.control == 9
            isJogScratch        = isControl and msg.control == 10

            if isJogTouch or isJogBend or isJogScratch:
                # Jogwheel direction is inverted on the Starlight
                if isJogBend or isJogScratch:
                    msg.value = 128 - msg.value

                # The Starlight sends jogwheel messages on these channels while Shift is held
                isShifted = msg.channel == 4 or msg.channel == 5

                # Hijack shifted jogbend messages to remap to Browse Up/Down in Rekordbox
                if isShifted and isJogBend:
                    # Determine the direction and set a unique channel number so we have 2 directional messages to Learn in Rekordbox
                    # This applies to both jog wheels, so they can both be used to browse
                    msg.channel = 7 if msg.value == 1 else 8
                    self.outport_control.send(msg)
                else:
                    self.outport_jogwheel.send(msg)
            else:
                # Tempo slider is inverted on the Starlight
                isTempoSlider = isControl and (msg.control == 8 or msg.control == 40)
                if (isTempoSlider):
                    msg.value = 127 - msg.value

                self.outport_control.send(msg)

if __name__ == "__main__":
    input_ports = mido.get_input_names()
    output_ports = mido.get_output_names()

    print("\nAvailable input ports:")
    print("\n".join(input_ports))

    print("\nAvailable output ports:")
    print("\n".join(output_ports))

    # Hook up the physical device
    inport_controller_name = None
    for port_name in input_ports:
        if PHYSICAL_MIDI_DEVICE in port_name:
            inport_controller_name = port_name
            break

    # Hook up to the virtual device used to send jogwheel messages
    outport_jogwheel_name = None
    for port_name in output_ports:
        if VIRTUAL_JOGWHEEL_DEVICE in port_name:
            outport_jogwheel_name = port_name
            break

    # Hook up to the virtual device used to send all other messages
    outport_other_name = None
    for port_name in output_ports:
        if VIRTUAL_CONTROL_DEVICE in port_name:
            outport_other_name = port_name
            break

    # Make Rekordbox send Output (LED) messages to this port
    inport_led_name = None
    for port_name in input_ports:
        if VIRTUAL_LED_DEVICE in port_name:
            inport_led_name = port_name
            break

    # Forward Rerkodbox's Output (LED) messages to the physical device
    outport_led_name = None
    for port_name in output_ports:
        if PHYSICAL_MIDI_DEVICE in port_name:
            outport_led_name = port_name
            break

    print("\nListening...")
    
    # Receives input messages from the controller, modifies them as needed, and passes them on to Rekordbox
    n = Translator(input=inport_controller_name, output_jogwheel=outport_jogwheel_name, output_other=outport_other_name)
    n.start()

    # Relays output (LED) messages from Rekordbox to the controller
    m = Relay(input=inport_led_name, output=outport_led_name)
    m.start()