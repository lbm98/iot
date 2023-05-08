from network import Bluetooth

# Connection interval in seconds
CONNECTION_INTERVAL = 1

# Define the UUID of the service you want to read from
SERVICE_UUID = 0x1000

# Define the UUID of the characteristic you want to read from
CHARACTERISTIC_UUID = 0x2000


def conn_cb(bt_o):
    events = bt_o.events()
    if events & Bluetooth.CLIENT_CONNECTED:
        print("Client connected")
    elif events & Bluetooth.CLIENT_DISCONNECTED:
        print("Client disconnected")


def chr1_cb_handler(chr, data):
    chr.value(100)
    print("transmitted :", 100)


bluetooth = Bluetooth()
bluetooth.set_advertisement(name='FiPy 45', manufacturer_data="Pycom", service_uuid=SERVICE_UUID)

bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=conn_cb)
bluetooth.advertise(True)

srv1 = bluetooth.service(uuid=SERVICE_UUID, isprimary=True, nbr_chars=1)
chr1 = srv1.characteristic(uuid=CHARACTERISTIC_UUID, value='read_from_here')

chr1.callback(trigger=Bluetooth.CHAR_READ_EVENT, handler=chr1_cb_handler)

print('Start BLE service')
