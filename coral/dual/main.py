import time
import socket
import requests
from bluepy.btle import Scanner, Peripheral, BTLEDisconnectError

# We want to create an IP server on this device
# Here, we define the parameters related to the IP connection

HOST = ''  # The IP address of this device, so leave empty
PORT = 8090  # The IP port of the application

# We want to poll a BLE device for data
# Here, we define the parameters related to the BLE connection

CONNECTION_INTERVAL = 1  # We poll the device for data each CONNECTION_INTERVAL
DEVICE_MAC_ADDRESS = 'F0:08:D1:CC:3E:3A'  # The MAC address of the BLE device
SERVICE_UUID = 0x1000  # The UUID of the service
CHARACTERISTIC_UUID = 0x2000  # The UUID of the characteristic


def listen_on_ip_socket():
    # Create a socket object using the following options:
    # - socket.AF_INET: For use with Internet protocols (WiFi, LTE, Ethernet)
    # - socket.SOCK_STREAM: Creates a stream socket (INET socket only, UDP protocol only)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    sock.bind((HOST, PORT))

    # Listen for incoming connections
    # Accept maximum 1 connection at the same time
    sock.listen(1)


def discover_ble_characteristic():
    scanner = Scanner()

    # Block until we find the correct characteristic
    while True:
        devices = scanner.scan(2)

        # Try to find the correct device
        for dev in devices:
            # Compare the MAC addresses in a case-insensitive way,
            if dev.addr.lower() == DEVICE_MAC_ADDRESS.lower():
                print(f'Device {dev.addr} found')
                peripheral = Peripheral(dev.addr)

                # Try to find the correct service
                services = peripheral.getServices()
                for service in services:
                    if service.uuid == SERVICE_UUID:
                        print(f'Service {service.uuid} found')

                        # Try to find the correct characteristic
                        characteristics = service.getCharacteristics()
                        for characteristic in characteristics:
                            if characteristic.uuid == CHARACTERISTIC_UUID:
                                print(f'Characteristic {characteristic.uuid} found')

                                return characteristic


def read_ble_characteristic(characteristic):
    try:
        value_bytes = characteristic.read()
        value = value_bytes.decode()

        print(f'Read value: {value}')

        # requests.post(
        #     url=COULD_URL,
        #     json={
        #         'humidity': value
        #     }
        # )

        success = True
    except BTLEDisconnectError:
        success = False

    return success


def main():
    sock = listen_on_ip_socket()
    char = discover_ble_characteristic()

    while True:
        success = read_ble_characteristic(char)
        if not success:
            print('Failed to get data')


if __name__ == '__main__':
    main()
