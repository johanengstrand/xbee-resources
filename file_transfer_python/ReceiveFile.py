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
    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        device.open()

        # important to use the correct flags:
        # 'w' - write
        # 'b' - binary, 't' for text
        OUTPUT_PATH = OUTPUT_DIR.joinpath('received_data')
        f = open(OUTPUT_PATH,'wb')

        def collect_data(xbee_message):
            REMOTE_ADDRESS = xbee_message.remote_device.get_64bit_addr()
            PAYLOAD = xbee_message.data

            f.write(PAYLOAD)

            print("FROM MAC: %s PAYLOAD: %s" % (REMOTE_ADDRESS, PAYLOAD))

        device.add_data_received_callback(collect_data)

        print("Waiting for data...\n")

    finally:

        if device is not None and device.is_open():
            device.close()
            f.close()

            FILE_TYPE = filetype.guess(str(OUTPUT_PATH))

            if FILE_TYPE is not None:
                FILE_CATEGORY = filetype.guess_extension(str(OUTPUT_PATH))
                FILE_NAME = 'received.' + FILE_CATEGORY
                OUTPUT_PATH = OUTPUT_PATH.rename(OUTPUT_DIR.joinpath(FILE_NAME))

                if filetype.is_image(str(OUTPUT_PATH)):
                    img = mpimg.imread(OUTPUT_PATH)
                    plt.imshow(img)
                    plt.axis('off')
                    plt.show()

            print("\nReceived file %s (file type: %s)" % (OUTPUT_PATH, FILE_TYPE))


if __name__ == '__main__':
    main()
