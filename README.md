## :gear: Configuring XBee modules in XCTU

Set both Xbee units to "Transparent mode" aka "AT mode".
Xbee S1 units should be set up in AT mode out of the box.
For Xbee 3 you must flash the 802.15.4 firmware first, if it has not already been done.

Set the following properties:

Property | Transmitter XBee      |	Receiver XBee           | Comment
---------|-----------------------|--------------------------|---------
CH 	     | C	                   | C                        | The channel. Must be the same for both devices.
ID 	     | 3332   	             | 3332                     | The network. Must be the same for both devices.
DH 	     | 0       	             | 0       	                | High part of the destination address.
DL 	     | 1                     | 0                        | Low part of the destination address.
MY 	     | 0                     | 1                        | Source address for the XBee.
MM         | 802.15.4 (no ACKs)       | 802.15.4 (no ACKs)        | The MAC mode. Set to strict 802.15.4.
NI 	     | Transmitter 	         | Receiver 	              | Node identifier in ASCII characters.
PL       | 0                     |	0 	                    | Power level. Set it to the lowest setting.
BD         | 57600               |  57600                      | Baud rate. Must be same for XBees and Arduino.
RO         | 2                   | 2                           | Packetization timeout. Set to 2 character times.

## Hardware

**IMPORTANT:** Most problems likely to stem from baud rate mismatches.

### Sparkfun Xbee shields

**IMPORTANT:** The Sparkfun Xbee shield requires a certain Arduino sketch (found in `./sparkfun_arduino`) to be loaded for the Xbee to PC communication to function. The Arduino sketch uses the SoftwareSerial library and as a result baud rate mismatches between the Xbee and Arduino can easily occur.

> If XCTU throws errors you may need to unplug the device, program the Arduino with the `uno_xbee` sketch with an appropriate baud rate and then re-discover it in XCTU.

### Arduino Wireless Proto Shield

The official Arduino Wireless Proto Shield requires an empty Arduino sketch to be loaded in order to discover the Xbee radio in XCTU. 
The Xbee unit may need to be disconnected from the shield when programming the Arduino.

## Troubleshooting in XCTU

If the Xbee radios cannot be discovered by XCTU even though you have followed all steps above you can try the following in XCTU in order to reset the Xbee radio to factory defaults: 

- Open a serial console window 
- Select the serial port of the Xbee unit and open the connection
- In the input text window, quickly input `+++`. The Xbee radio should respond "OK".
- Then, quickly input `ATRE` followed by the `Enter` key.

Once successful, remember that the Xbee unit may now be using 9600 baud instead of what was previously configured.

This output "OK" may be somewhat garbled if you have a baud rate mismatch.
If the Xbee does not respond, try another baud rate.
Remember to have the correct sketch for your shield loaded per the instructions above.

