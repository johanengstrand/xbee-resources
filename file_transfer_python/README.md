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

## How to run

Edit the Python scripts to use the correct ports, baud rate and file paths.

Then, run the receiver script and then the transmitter script (in two separate terminal windows), i.e.

```
python ReceiveFile.py
```

```
python SendFile.py
```

Once the reception is finished, press `Enter` on your keyboard while the terminal window running `ReceiveFile.py` is active.
The `SendFile.py` script will terminate itself shortly after the transmission is finished.
