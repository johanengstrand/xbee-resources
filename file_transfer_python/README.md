# Xbee file transfer

This is a simple file transfer application for Xbee implemented in Python.

## Installation

You need Digi's Python library for Xbee:
```
pip install digi-xbee
```

Filetypes are identified automatically using the `filetype` library:
```
pip install filetype
```

## Xbee configuration

Xbee 3 802.15.4 radios were used during the development.
These scripts should work with other Xbee radios as well, but they *must* be setup in **API mode**.

## How to run

Edit the Python scripts to use the correct ports, baud rate and file paths.

Then, open a terminal window and run

```
python ReceiveFile.py
```
In another terminal window, run

```
python SendFile.py
```

When the file reception has finished, press `Enter` on your keyboard while the terminal window running `ReceiveFile.py` is active.
If the received file is identified as an image file `ReceiveFile.py` will spawn a new window and display the image shortly after `Enter` has been pressed.

The `SendFile.py` script will terminate itself shortly after the transmission is finished.
