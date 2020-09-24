**This is not meant to replace any official documentation for the described products. Make sure to read those first, then come back here for my remarks!**

## Hardware

Here some of the hardware and peripherals are described, along with some tips and tricks that I have amassed during my time working with them.

### Sparkfun Xbee shields

The Sparkfun Xbee shield requires a certain Arduino sketch (![found here under "The Arduino Sketch"](https://learn.sparkfun.com/tutorials/xbee-shield-hookup-guide#example-communication-test)) to be loaded for the Xbee to PC communication to function. The Arduino sketch uses the `SoftwareSerial` library and as a result baud rate mismatches between the Xbee and Arduino can easily occur.

Baud rates higher than 57 600 are not recommended when using the Sparkfun Xbee shield.

> If XCTU throws errors you may need to re-program the Arduino with the `uno_xbee` sketch with an appropriate baud rate and then re-discover it in XCTU.

![The Sparkfun Xbee shield.](https://www.rpelectronics.com/Media/400/wrl-09976.jpg)

### Arduino Wireless Proto Shield

The official Arduino Wireless Proto Shield requires an empty Arduino sketch to be loaded in order to discover the Xbee radio in XCTU.
The Xbee unit may need to be disconnected from the shield when programming the Arduino.

Baud rates of 115 200 or possibly higher seem to work well with the Arduino Wireless Proto Shield.

![The Arduino Wireless Proto Shield.](https://store-cdn.arduino.cc/usa/catalog/product/cache/1/image/520x330/604a3538c15e081937dbfbd20aa60aad/A/0/A000064_featured_2.jpg)

### Sparkfun Xbee Explorer USB

The Sparkfun Xbee Explorer USB is probably the best-performing and easiest to use unit if you do not need a microcontroller (or if the Xbee 3's Micropython capabilites in combination with some sensor is sufficient for your purposes).
I would recommend using the Explorer USB for troubleshooting, instead of the Arduino/shield.

On GNU/Linux this device shows up as e.g. /dev/ttyUSB0 instead of /dev/ttyACM0 like an Arduino/shield setup; keep this in mind in case e.g. port names are hard-coded into some of your scripts.

![The Sparkfun Xbee Explorer USB.](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ffr.hobbytronics.co.uk%2Fimage%2Fcache%2Fdata%2Fsparkfun%2Fxbee_explorer_usb-250x250.jpg&f=1&nofb=1)

## Configuring Xbee modules in XCTU

Xbee 3 radios come pre-loaded with Zigbee firmware, so if you want to use IEEE 802.15.4 (which has lower overhead than Zigbee) you must flash the 802.15.4 firmware, if it has not already been done by someone else.

- Place your Xbee unit(s) in a shield connected to an Arduino or in another USB interface.
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

### Measuring data rate with the Throughput tool

The Throughput tool can measure the instant and average transfer ratio (i.e. data rate) in kbps between two radios.

For the best results, do the following:
- Set up one Xbee in API mode and the other in Transparent (AT) mode.
- In the Throughput tool window, select the AT-configured Xbee as the local radio device.
- You can now select a secondary local radio device. Select the API-configured Xbee.
- You can leave the rest of the settings as-is, though you may want to choose a longer time duration or "Loop infinitely".

The recorded data cannot be exported as a file on your computer, though you can save the graph by right-clicking on it. 
It is a good idea to take a screenshot of the entire window as well.

![The Throughput tool in XCTU.](/images/throughput.png)

### Measuring packet loss with the Range Test tool

The Range test tool can measure packet loss (or rather, packet success rate) as well as the received signal strength indicator (RSSI) of both transmitter and recceiver in a network of two radios.

*The remote radio device must have been "discovered" by the local one in order to measure the remote RSSI.*
Because of this, the local radio device should be configured in API mode.
Click the little button to the right of "Select the local radio device" once you have selected the API-enabled Xbee unit in the list in order to discover the remote radio module.
This can also be done in XCTU's main screen.

Once the remote radio has been discovered its MAC address should be automatically filled in on the right side (under "Select the remote radio device).
There are various settings here which are self-explanatory, though it is important to note that the TX interval works a little different than one might think: 
If the TX interval is set to e.g. 250 ms packets will actually *not* be sent exactly 4 times per second, instead the transmitter will wait for confirmation that the packet was received correctly before sending the next packet, which causes packets to be sent less frequently than the user-defined setting.

You can now run the test, though the recorded data is to my knowledge not available as a file on your computer; you can however save the graph itself by right-clicking on it.
It is a good idea to take a screenshot of the entire window as well.

![The Range Test tool in XCTU.](/images/rangetest.png)

### Measuring channel noise levels with the Spectrum Analyzer tool

The Spectrum Analyzer tool can measure the noise levels of the 16 available channels.

Choose the sampling interval and the number of samples and run the test.
You can click on one of the channel bars to see the current, maximum, minimum and average noise levels of the channel. 

The recorded data cannot be exported as a file on your computer, though you can save the graph by right-clicking on it. 
It is a good idea to take a screenshot of the entire window as well.

![The Spectrum Analyzer tool in XCTU.](/images/spectrum.png)

## Troubleshooting in XCTU

**If possible, use the Sparkfun Explorer USB (or some other device that does not involve an Arduino or the likes).**

If the Xbee radio is not working correctly, you may try restoring the firmware in XCTU.
If XCTU will not recognize your plugged-in Xbee radios, try this:

- First and foremost - **did you try turning it on and off again?** Unplug and replug the USB cable and see if it works then.
- Remember to have the correct sketch for your shield (if you are using one) loaded on the Arduino per the instructions above.
- Try different baud rates in the discovery process but remember that choosing *every single baud rate* in the list can cause the discovery process to take quite some time.
- As a last resort, check *every single* setting and try the discovery again; it is going to take quite some time.

**IMPORTANT:** Most problems are likely to stem from baud rate mismatches.

If the Xbee radios cannot be discovered by XCTU even though you have followed all steps above you can try the following in XCTU in order to reset the Xbee radio to factory defaults:

- Open a serial console window (from the Tools menu)
- Select the serial port of the Xbee unit and open the connection
- In the input text window, quickly input `+++`. The Xbee radio should respond "OK".
- Then, quickly input `ATRE` followed by the `Enter` key.

Once successful, remember that the Xbee unit may now be using 9600 baud instead of what was previously configured.

> If the Xbee does not respond, try another baud rate.

XCTU might at some point ask you to reset the radio module.
If you are using a shield, you may need to reset the Xbee by shorting the RESET pin to ground.
RESET is usually pin 5 (ground is on pin 10) but check the data sheet.
Resetting the radio module in this way rarely solved any problems for me, though.

![Pin layout on a typical Xbee module.](/images/pins.jpg)

If all else fails you may need to download the old, XCTU legacy software, take a look at ![this](https://www.digi.com/support/knowledge-base/recovery-procedure-for-xbees) ![this](http://arduino.blogs.ua.sapo.pt/1874.html) and this ![this](https://www.instructables.com/id/Restoring-your-broken-XBee/).
