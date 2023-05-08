import time
from bluepy.btle import Scanner, Peripheral

# Define the MAC address of the BLE device you want to connect to
DEVICE_MAC_ADDRESS = b'F0:08:D1:CC:3E:3A'

# Define the UUID of the service you want to read from
SERVICE_UUID = b'1234567890123456'

# Define the UUID of the characteristic you want to read from
CHARACTERISTIC_UUID = b'ab34567890123456'


# Define a function to handle BLE notifications
def handle_notification(handle, data):
    print(f'Received notification from handle {handle}: {data}')


# Define a function to discover services and characteristics of the BLE device
def discover_ble_device():
    scanner = Scanner()
    devices = scanner.scan(2.0)
    for dev in devices:
        print(dev.addr)

        # Compare the MAC addresses in a case-insensitive way,
        if dev.addr.lower() == DEVICE_MAC_ADDRESS.decode().lower():

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
    while True:
        value = characteristic.read()
        print(f'Read value: {value}')
        time.sleep(1.0)


def main():
    # Discover the BLE device and its characteristics
    peripheral, characteristic = discover_ble_device()

    # Start reading data from the characteristic
    read_ble_characteristic(peripheral, characteristic)

    # Disconnect from the BLE device
    peripheral.disconnect()


if __name__ == '__main__':
    main()
