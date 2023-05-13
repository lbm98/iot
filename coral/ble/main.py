import time
import requests
from bluepy.btle import Scanner, Peripheral, BTLEDisconnectError

# The connection interval in seconds
CONNECTION_INTERVAL = 1

# The MAC address of the BLE device
DEVICE_MAC_ADDRESS = 'F0:08:D1:CC:3E:3A'

# The UUID of the service
SERVICE_UUID = 0x1000

# The UUID of the characteristic
CHARACTERISTIC_UUID = 0x2000

# The coral collects data from the sensors
# and will send it to the cloud.
# Here we define parameters related to the cloud connection.
CLOUD_HOST = '192.168.1.28'  # Could change because of DHCP
CLOUD_PORT = 8080
CLOUD_PATH = '/sensor'
COULD_URL = f'http://{CLOUD_HOST}:{CLOUD_PORT}{CLOUD_PATH}'


# Handle BLE notifications
def handle_notification(handle, data):
    print(f'Received notification from handle {handle}: {data}')


# Discover services and characteristics of the BLE device
def discover_ble_device():
    scanner = Scanner()

    while True:
        devices = scanner.scan(2)

        for dev in devices:
            print(dev.addr)

            # Compare the MAC addresses in a case-insensitive way,
            if dev.addr.lower() == DEVICE_MAC_ADDRESS.lower():

                print(f'Device {dev.addr} found!')

                peripheral = Peripheral(dev.addr)
                services = peripheral.getServices()
                for service in services:
                    if service.uuid == SERVICE_UUID:

                        print(f'Service {service.uuid} found!')

                        characteristics = service.getCharacteristics()
                        for characteristic in characteristics:
                            if characteristic.uuid == CHARACTERISTIC_UUID:
                                print(f'Characteristic {characteristic.uuid} found!')

                                return peripheral, characteristic


# Read data from the BLE characteristic
def read_ble_characteristic(peripheral, characteristic):
    try:
        while True:
            value_bytes = characteristic.read()
            value = value_bytes.decode()

            print(f'Read value: {value}')
            requests.post(
                url=COULD_URL,
                json={
                    'humidity': value
                }
            )

            time.sleep(CONNECTION_INTERVAL)
    except KeyboardInterrupt:
        reconnect = False
    except BTLEDisconnectError:
        reconnect = True

    return reconnect


def main():
    while True:
        # Discover the BLE device and its characteristics
        peripheral, characteristic = discover_ble_device()

        # Start reading data from the characteristic
        reconnect = read_ble_characteristic(peripheral, characteristic)

        if not reconnect:
            break

    # Disconnect from the BLE device
    peripheral.disconnect()
    print('Disconnected')


if __name__ == '__main__':
    main()
