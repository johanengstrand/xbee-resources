## :gear: Configuring XBee modules in XCTU

Set both XBee units to "Transparent mode" aka "AT mode".
XBee S1 units should be set up in AT mode out of the box.
For XBee 3 you must flash the 802.15.4 firmware first, if it has not already been done.

Set the following properties:

Property | Transmitter XBee      |	Receiver XBee           | Comment
---------|-----------------------|--------------------------|---------
CH 	     | C   	                 | C                        | The channel. Must be the same for both devices.
ID 	     | 3332   	             | 3332                     | The network. Must be the same for both devices.
DH 	     | 0       	             | 0       	                | High part of the destination address.
DL 	     | 1                     | 0                        | Low part of the destination address.
MY 	     | 0                     | 1                        | Source address for the XBee.
MM         | 802.15.4 (no ACKs)       | 802.15.4 (no ACKs)        | The MAC mode. Set to strict 802.15.4.
NI 	     | Transmitter 	         | Receiver 	              | Node identifier in ASCII characters.
PL       | 0                     |	0 	                    | Power level. Set it to the lowest setting.
BD         | 57600               |  57600                      | Baud rate. Must be same for XBees and Arduino.
RO         | 2                   | 2                           | Packetization timeout. Set to 2 character times.

## Xbee/XCTU troubleshooting

The Xbee shields from Sparkfun require the use of SoftwareSerial and therefore the Arduino to which it is connected must be loaded with a specific sketch that passes serial data from the USB interface to the right pins.
*Baud rate mismatches can easily occur in XCTU when using the Sparkfun shields - if XCTU throws errors you may need to unplug the device, program the Arduino with the appropriate baud rate and then re-discover it in XCTU.*

Another thing to try if things go south with the Xbee configuration:

Go into XCTU and open a serial console, select the port of the Xbee unit and quickly input
```
+++
```
The Xbee radio should respond "OK".
Then, quickly input
```
ATRE
```
and press the `Enter` key.
