import time
import socket
import requests
from bluepy.btle import Scanner, Peripheral, BTLEException

from config import CLOUD_URL

# We want to create an IP server on this device
# Here, we define the parameters related to the IP connection

HOST = '192.168.1.36'  # The IP address of the ethernet interface
PORT = 8090  # The IP port of the application

# We want to poll a BLE device for data
# Here, we define the parameters related to the BLE connection

CONNECTION_INTERVAL = 1  # We poll the device for data each CONNECTION_INTERVAL
DEVICE_MAC_ADDRESS = 'F0:08:D1:CC:3E:3A'  # The MAC address of the BLE device
SERVICE_UUID = 0x1000  # The UUID of the service
CHARACTERISTIC_UUID = 0x2000  # The UUID of the characteristic


def discover_ble_characteristic():
    scanner = Scanner()

    # Block until we find the correct characteristic
    while True:
        print('Trying to find BLE device')
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

        print(f'Data received from BLE: {value}')

        requests.post(
            url=CLOUD_URL,
            json={
                'humidity': value
            }
        )

        success = True
    except BTLEException:
        success = False

    return success

def main():
    char = discover_ble_characteristic()

    count = 0
    while True:
        # Sometimes, the BLE channel fails,
        if count % 5 == 0:
            time.sleep(5.0)
        else:
            # Try to poll the BLE device for data
            success = read_ble_characteristic(char)
            if not success:
                print('Failed to poll BLE device')
            time.sleep(CONNECTION_INTERVAL)

        count += 1


if __name__ == '__main__':
    main()
