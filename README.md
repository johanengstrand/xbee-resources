Make sure to read the official documentation, e.g. for [Xbee 3 802.15.4](https://www.digi.com/resources/documentation/digidocs/PDFs/90002273.pdf).

## Hardware

Here some of the hardware and peripherals are described, along with some tips and tricks that I have amassed during my time working with them.

### Sparkfun Xbee shields

The Sparkfun Xbee shield requires a certain Arduino sketch ([found here under "The Arduino Sketch"](https://learn.sparkfun.com/tutorials/xbee-shield-hookup-guide#example-communication-test)) to be loaded for the Xbee to PC communication to function. The Arduino sketch uses the `SoftwareSerial` library and as a result baud rate mismatches between the Xbee and Arduino can easily occur. The `NewSoftSerial` library may be better in this regard.

> If XCTU throws errors you may need to re-program the Arduino with the `uno_xbee` sketch with an appropriate baud rate and then re-discover it in XCTU.

![The Sparkfun Xbee shield.](https://www.rpelectronics.com/Media/400/wrl-09976.jpg)

### Arduino Wireless Proto Shield

The official Arduino Wireless Proto Shield requires an empty Arduino sketch to be loaded in order to discover the Xbee radio in XCTU.
The Xbee unit may need to be disconnected from the shield when programming the Arduino.

![The Arduino Wireless Proto Shield.](https://store-cdn.arduino.cc/usa/catalog/product/cache/1/image/520x330/604a3538c15e081937dbfbd20aa60aad/A/0/A000064_featured_2.jpg)

### Sparkfun Xbee Explorer USB

The Sparkfun Xbee Explorer USB is probably the best-performing and easiest to use unit if you do not require a microcontroller (or if the Xbee 3's Micropython capabilites in combination with some sensor is sufficient for your purposes).
I would recommend using the Explorer USB for troubleshooting, instead of the Arduino/shield.

On GNU/Linux this device shows up as e.g. `/dev/ttyUSB0` instead of `/dev/ttyACM0` like the Arduino/shield setup would; keep this in mind in case e.g. port names are hard-coded into some of your scripts.

![The Sparkfun Xbee Explorer USB.](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ffr.hobbytronics.co.uk%2Fimage%2Fcache%2Fdata%2Fsparkfun%2Fxbee_explorer_usb-250x250.jpg&f=1&nofb=1)

## Configuring Xbee modules in XCTU

Xbee 3 radios come pre-loaded with Zigbee firmware, so if you want to use IEEE 802.15.4 (which has lower overhead than Zigbee) you must flash the 802.15.4 firmware, if it has not already been done by someone else.

Discovering an Xbee radio in XCTU is quite simple:
- Place your Xbee unit in a USB interface or a shield connected to an Arduino.
- Connect the Arduino/USB interface to your computer with a USB cable and click "Discover radio modules" in the upper left hand corner of XCTU.
- If your modules do not show up, check the [Troubshooting in XCTU](#troubleshooting-in-xctu) section down below.
   
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


## Measurement tools

All measurement tools are available under the Tools menu in XCTU (the wrench button at the top of the window).

### Measuring channel noise levels with the Spectrum Analyzer tool

The Spectrum Analyzer tool can measure the noise levels of the 16 available channels.

Choose the sampling interval and the number of samples and run the test.
You can click on one of the channel bars to see the current, maximum, minimum and average noise levels of the channel. 

The recorded data cannot be exported as a file on your computer, though you can save the graph by right-clicking on it. 
It is a good idea to take a screenshot of the entire window as well.

![The Spectrum Analyzer tool in XCTU.](/images/spectrum.png)


### Measuring data rate with the Throughput tool

The Throughput tool can measure the instant and average transfer ratio (i.e. data rate) in kbps between two radios.

Suggestions for doing a Throughput test:
- Set up at least one of the two Xbee radios in Transparent (AT) mode.
- In the Throughput tool window, select the AT-configured Xbee as the local radio device.
- You can now select a secondary local radio device. Select the other Xbee.
- You can leave the rest of the settings as-is, though you may want to choose a longer time duration or "Loop infinitely".

Xbee 3 (one in AT mode, one in API mode) at 115 200 baud generally scored around 50 kbps using default settings. 
Increasing the payload yielded (at most) a sustained 80 kbps or so.
Test some varying payload sizes and observe how the data rate changes. 

The recorded data cannot be exported as a file on your computer, though you can save the graph by right-clicking on it. 
It is a good idea to take a screenshot of the entire window as well.

It should be noted that the Throughput tool is [not entirely accurate](https://www.digi.com/support/forum/66513/how-can-we-send-a-100-000-byte-packet-through-xctu).

![The Throughput tool in XCTU.](/images/throughput.png)

### Measuring packet loss with the Range Test tool

The Range test tool can measure packet loss (or rather, packet success rate) as well as the received signal strength indicator (RSSI) of both transmitter and recceiver in a network of two radios.

*The remote radio device must have been "discovered" by the local one in order to measure the remote RSSI.*
Because of this, the local radio device should be configured in API mode.
Click the little button to the right of "Select the local radio device" once you have selected the API-enabled Xbee unit in the list in order to discover the remote radio module.
This can also be done in XCTU's main screen.

If using the 802.15.4 protocol, a jumper wire needs to be connected between the DIN and DOUT pins of the Xbee (usually corresponding to RX/GPIO 0 and TX/GPIO 1 on an Arduino Uno with a shield).

Once the remote radio has been discovered its MAC address should be automatically filled in on the right side (under "Select the remote radio device).
There are various settings here which are self-explanatory, though it is important to note that the TX interval works a little different than one might think: 
If the TX interval is set to e.g. 250 ms packets will actually *not* be sent exactly 4 times per second, instead the transmitter will wait for confirmation that the packet was received correctly before sending the next packet, which causes packets to be sent less frequently than the user-defined setting.

**IMPORTANT:** All other open XCTU consoles that are occupying an Xbee serial connection must be closed before the test! If not closed, XCTU may ruin the measurement due to lag!

You can now run the test, though the recorded data is to my knowledge not available as a file on your computer; you can however save the graph itself by right-clicking on it.
It is a good idea to take a screenshot of the entire window as well.

![The Range Test tool in XCTU.](/images/rangetest.png)

### Misc. tools/examples 

In `./xctu_frames` there are various collections of frames for sending test messages, AT commands etc. from an Xbee radio in API mode. 
Make sure to change the MAC address of each frame to that of your recipient Xbee.
A message addressed to an all-zero MAC address will be sent as a broadcast message to all available radios.

In `./xctu_packets` one can find some test packets that can be of use for local Xbee radios in Transparent (AT) mode.

Some profiles (consisting of configuration settings) that I have used for various purposes are available in `./xctu_profiles`.

## Troubleshooting in XCTU

**If possible, use the Sparkfun Explorer USB (or some other device that does not involve an Arduino or the likes).**

If the Xbee radio is not working correctly, you may try restoring the firmware in XCTU.
If XCTU will not recognize your plugged-in Xbee radios, try this:

- First and foremost - **did you try turning it on and off again?** Unplug and replug the USB cable and see if it works then.
- Remember to have the correct sketch for your shield (if you are using one) loaded on the Arduino per the instructions above.
- Try different baud rates in the discovery process but remember that choosing *every single* baud rate in the list can cause the discovery process to take quite some time.
- As a last resort, check *every single* setting and try the discovery again; it is probably going to take a *long* time.
- Try the manual discovery (the button with the plus sign to the left of the discovery button) 

**IMPORTANT:** Most problems are likely to stem from baud rate mismatches.

If the Xbee radios cannot be discovered by XCTU even though you have followed all steps above you can try the following in XCTU in order to reset the Xbee radio to factory defaults:

- Open a serial console window (from the Tools menu)
   - Select the serial port of the Xbee unit and open the connection using the baud rate that you *think* the Xbee is using.
   - In the input text window, quickly input `+++`. The Xbee radio should respond "OK".
   - Then, quickly input `ATRE` followed by the `Enter` key.
   - If the Xbee does not respond, try a different baud rate.

Once successful, remember that the Xbee unit may now be using 9600 baud instead of what was previously configured.

> If the Xbee does not respond, try another baud rate.

XCTU might at some point ask you to reset the radio module.
A reset can be performed by shorting the RESET pin to ground, in case pressing the reset button on your shield/USB interface has no effect.
RESET is for most Xbee modules located at pin 5 (ground is on pin 10) but check the data sheet.

![Pin layout on a typical Xbee module.](/images/pins.jpg)

Also, try the Recovery tool in XCTU in order to forcibly flash an unresponsive unit with your desired firmware. 

If all else fails you may need to download the old, XCTU legacy software, take a look at [this](https://www.digi.com/support/knowledge-base/recovery-procedure-for-xbees), [this](http://arduino.blogs.ua.sapo.pt/1874.html) and [this](https://www.instructables.com/id/Restoring-your-broken-XBee/).
This may however not work for newer modules.

### Non-responsive unit when running MicroPython
If MicroPython is active and the unit cannot be discovered in XCTU, try shorting the DIN pin to ground while resetting the module (with the designated reset button on the Sparkfun XBee Explorer USB). 
Once this has been performed the unit should be discoverable again, or at least recoverable using one of the previously described methods.
