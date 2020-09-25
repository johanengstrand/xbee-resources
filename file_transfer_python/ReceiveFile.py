from digi.xbee.devices import XBeeDevice

# GNU/Linux port naming
PORT = "/dev/ttyACM1"
BAUD_RATE = 115200


def main():
    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        device.open()

        # important to use the correct flags:
        # 'w' - write
        # 'b' - binary, 't' for text
        f = open('/tmp/receivedimg.png','wb')

        def collect_data(xbee_message):
            REMOTE_ADDRESS = xbee_message.remote_device.get_64bit_addr()
            PAYLOAD = xbee_message.data

            f.write(PAYLOAD)

            print("FROM MAC: %s PAYLOAD: %s" % (REMOTE_ADDRESS, PAYLOAD))

        device.add_data_received_callback(collect_data)

        f.close()

        print("Waiting for data...\n")

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()
