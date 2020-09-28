import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import filetype
from pathlib import Path

from digi.xbee.devices import XBeeDevice

# GNU/Linux port naming
PORT = "/dev/ttyACM1"
BAUD_RATE = 115200

OUTPUT_DIR = Path('/tmp')


def main():
    xbee = XBeeDevice(PORT, BAUD_RATE)

    try:
        xbee.open()

        OUTPUT_PATH = OUTPUT_DIR.joinpath('received_data')

        # important to use the correct flags:
        # 'w' - write
        # 'b' - binary, 't' for text
        f = open(OUTPUT_PATH,'wb')

        def collect_data(xbee_message):
            REMOTE_ADDRESS = xbee_message.remote_device.get_64bit_addr()
            PAYLOAD = xbee_message.data

            f.write(PAYLOAD)

            print("FROM MAC: %s PAYLOAD: %s" % (REMOTE_ADDRESS, PAYLOAD))

        xbee.add_data_received_callback(collect_data)

        print("Waiting for data...\n")
        input()

    finally:
        if xbee is not None and xbee.is_open():
            xbee.close()

        f.close()

    OUTPUT_PATH_STR = str(OUTPUT_PATH)
    FILE_TYPE = filetype.guess(OUTPUT_PATH_STR)

    if FILE_TYPE is not None:
        FILE_EXTENSION = filetype.guess_extension(OUTPUT_PATH_STR)
        FILE_NAME = 'received.' + FILE_EXTENSION
        OUTPUT_PATH = OUTPUT_PATH.rename(OUTPUT_DIR.joinpath(FILE_NAME))

    if filetype.is_image(str(OUTPUT_PATH)):
        img = mpimg.imread(OUTPUT_PATH)
        plt.imshow(img)
        plt.axis('off')
        plt.show()

    print("\nReceived file %s (file type: %s)" % (OUTPUT_PATH, FILE_TYPE))


if __name__ == '__main__':
    main()
