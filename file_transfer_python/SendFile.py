from pathlib import Path
from digi.xbee.devices import XBeeDevice

# GNU/Linux port naming
PORT = "/dev/ttyACM0"
BAUD_RATE = 115200
REMOTE_NODE_ID = "RX1"
PAYLOAD_BYTES = 100

FILE_PATH = Path('/home/johan/Test.png')


def main():
    xbee = XBeeDevice(PORT, BAUD_RATE)

    try:
        xbee.open()

        xbee_network = xbee.get_network()

        remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
        if remote_device is None:
            print("Remote xbee could not be found!")
            exit(1)

        # important to use the correct flags:
        # 'r' - read
        # 'b' - binary, 't' for text
        f = open(FILE_PATH, 'rb')
        chunk = f.read(PAYLOAD_BYTES)
        while chunk:
            print("REMOTE MAC: %s PAYLOAD: %s" % (remote_device.get_64bit_addr(), chunk))
            xbee.send_data(remote_device, chunk)
            chunk = f.read(PAYLOAD_BYTES) #read the next chunk

        f.close()

    finally:
        if xbee is not None and xbee.is_open():
            xbee.close()


if __name__ == '__main__':
    main()
