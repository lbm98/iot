from network import Bluetooth
import pycom

from SI7006A20 import SI7006A20
from pycoproc_2 import Pycoproc

# Connection interval in seconds
CONNECTION_INTERVAL = 1

# The UUID of the service
SERVICE_UUID = 0x1000

# The characteristic of the service
CHARACTERISTIC_UUID = 0x2000

# Disable heartbeat LED to save power
pycom.heartbeat(False)

# Initialise the DHT temperature and humidity sensor
py = Pycoproc()
dht = SI7006A20(py)


def conn_cb(bt_o):
    events = bt_o.events()
    if events & Bluetooth.CLIENT_CONNECTED:
        print("Client connected")
    elif events & Bluetooth.CLIENT_DISCONNECTED:
        print("Client disconnected")


def chr1_cb_handler(chr, data):
    humidity = dht.humidity()
    chr.value(str(humidity))
    print("transmitted :", humidity)


bluetooth = Bluetooth()
bluetooth.set_advertisement(name='FiPy 45', manufacturer_data="Pycom", service_uuid=SERVICE_UUID)

bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=conn_cb)
bluetooth.advertise(True)

srv1 = bluetooth.service(uuid=SERVICE_UUID, isprimary=True, nbr_chars=1)
chr1 = srv1.characteristic(uuid=CHARACTERISTIC_UUID, value='read_from_here')

chr1.callback(trigger=Bluetooth.CHAR_READ_EVENT, handler=chr1_cb_handler)

print('Start BLE service')
