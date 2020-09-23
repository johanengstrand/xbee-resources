## :computer: Hardware

### Sparkfun Xbee shields

The Sparkfun Xbee shield requires a certain Arduino sketch (found in `./sparkfun_arduino`) to be loaded for the Xbee to PC communication to function. The Arduino sketch uses the SoftwareSerial library and as a result baud rate mismatches between the Xbee and Arduino can easily occur.

Baud rates higher than 57 600 are not recommended when using the Sparkfun Xbee shield.

> If XCTU throws errors you may need to re-program the Arduino with the `uno_xbee` sketch with an appropriate baud rate and then re-discover it in XCTU.

### Arduino Wireless Proto Shield

The official Arduino Wireless Proto Shield requires an empty Arduino sketch to be loaded in order to discover the Xbee radio in XCTU.
The Xbee unit may need to be disconnected from the shield when programming the Arduino.

Baud rates of 115 200 or possibly higher seem to work well with the Arduino Wireless Proto Shield.

## :wrench: Configuring XBee modules in XCTU

Xbee 3 radios come pre-loaded with Zigbee firmware, so if you want to use IEEE 802.15.4 (which has lower overhead than Zigbee) you must flash the 802.15.4 firmware, if it has not already been done by someone else.

There are a number of important configuration parameters.

**Make sure that the channel (`CH`), the network (`ID`) and the baud rate (`BD`) are the same across all devices which you wish to be able to communicate with each other.**

You may also wish to set a unique identifying ASCII string for each unit using the `NI` parameter and set the power level using `PL`.

For a simple point-to-point network, configure the following

Property | Transmitter XBee      |	Receiver XBee           | Comment
---------|-----------------------|--------------------------|---------
DH 	     | 0       	             | 0       	                | High part of the destination address.
DL 	     | 1                     | 0                        | Low part of the destination address.
MY 	     | 0                     | 1                        | Source address for the XBee.

These settings will work well when Transparent (AT) mode is used.
API mode will also be fine with these settings, though explicit addressing is possible in that mode and that is what you will want to use then.

> Setting the device role (`CE`), i.e. coordinator/end device may not be strictly required in all situations but is probably good practice.

## :warning: Troubleshooting in XCTU

**IMPORTANT:** Most problems are likely to stem from baud rate mismatches.

XCTU may ask you to reset the radio module.
If you are using a shield, you may need to reset the Xbee by shorting the RESET pin to ground.
RESET is usually pin 5 (ground is on pin 10) but check the data sheet.

![Pin layout on a typical Xbee module](/images/pins.jpg)

If the Xbee radios cannot be discovered by XCTU even though you have followed all steps above you can try the following in XCTU in order to reset the Xbee radio to factory defaults:

- Open a serial console window
- Select the serial port of the Xbee unit and open the connection
- In the input text window, quickly input `+++`. The Xbee radio should respond "OK".
- Then, quickly input `ATRE` followed by the `Enter` key.

Once successful, remember that the Xbee unit may now be using 9600 baud instead of what was previously configured.

> If the Xbee does not respond, try another baud rate.

> Remember to have the correct sketch for your shield loaded per the instructions above.

