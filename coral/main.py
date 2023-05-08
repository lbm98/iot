import time
from bluepy.btle import Scanner, Peripheral, BTLEDisconnectError

# Define the MAC address of the BLE device you want to connect to
DEVICE_MAC_ADDRESS = 'F0:08:D1:CC:3E:3A'

# Define the UUID of the service you want to read from
SERVICE_UUID = 0x1000

# Define the UUID of the characteristic you want to read from
CHARACTERISTIC_UUID = 0x2000


# Define a function to handle BLE notifications
def handle_notification(handle, data):
    print(f'Received notification from handle {handle}: {data}')


# Define a function to discover services and characteristics of the BLE device
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


# Define a function to read data from the BLE characteristic
def read_ble_characteristic(peripheral, characteristic):
    try:
        while True:
            value_bytes = characteristic.read()
            value = int.from_bytes(value_bytes, 'big')
            print(f'Read value: {value}')
            time.sleep(1.0)
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
