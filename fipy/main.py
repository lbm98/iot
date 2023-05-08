from network import Bluetooth

# Define the UUID of the service you want to read from
SERVICE_UUID = '0000180f-0000-1000-8000-00805f9b34fb'

# Define the UUID of the characteristic you want to read from
CHARACTERISTIC_UUID = '00002a19-0000-1000-8000-00805f9b34fb'


def conn_cb(bt_o):
    events = bt_o.events()
    if events & Bluetooth.CLIENT_CONNECTED:
        print("Client connected")
    elif events & Bluetooth.CLIENT_DISCONNECTED:
        print("Client disconnected")


def char1_cb_handler(chr, data):
    # The data is a tuple containing the triggering event and the value
    # if the event is a WRITE event.
    # We recommend fetching the event and value from the input parameter,
    # and not via characteristic.event() and characteristic.value()
    events, value = data
    if events & Bluetooth.CHAR_WRITE_EVENT:
        print("Write request with value = {}".format(value))
    else:
        chr.value(100)
        print("transmitted :", 100)


bluetooth = Bluetooth()
bluetooth.set_advertisement(name='FiPy 45', manufacturer_data="Pycom", service_uuid=SERVICE_UUID)

bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=conn_cb)
bluetooth.advertise(True)

srv1 = bluetooth.service(uuid=SERVICE_UUID, isprimary=True, nbr_chars=1)
chr1 = srv1.characteristic(uuid=CHARACTERISTIC_UUID, value='read_from_here')

chr1.callback(trigger=Bluetooth.CHAR_WRITE_EVENT | Bluetooth.CHAR_READ_EVENT, handler=char1_cb_handler)

print('Start BLE service')
