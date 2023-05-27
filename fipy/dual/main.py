from network import Bluetooth
import pycom
import time
import usocket

from network import WLAN
from SI7006A20 import SI7006A20
from pycoproc_2 import Pycoproc

# Connection interval in seconds
CONNECTION_INTERVAL = 1

# The UUID of the service
SERVICE_UUID = 0x1000

# The characteristic of the service
CHARACTERISTIC_UUID = 0x2000

SERVER = '192.168.1.36'  # Replace with the server's IP address
PORT = 8090  # Replace with the server's IP port
SSID = 'AP200'  # Replace with the name of your WiFi network
WPA2_KEY = 'LarsWard'  # Replace with the password of your WiFi network

# Create WLAN interface as a station
wlan = WLAN(mode=WLAN.STA)

# Disable heartbeat LED to save power
pycom.heartbeat(False)

# Setup network connection
wlan.connect(ssid=SSID, auth=(WLAN.WPA2, WPA2_KEY))

while not wlan.isconnected():
    print('Trying to connect to WLAN')
    time.sleep(0.5)
print('Connect to WLAN success')

# Variable to track the time of the last BLE read event
last_read_event_time = time.time()

# Initialise the DHT temperature and humidity sensor
py = Pycoproc()
dht = SI7006A20(py)


def conn_cb(bt_o):
    events = bt_o.events()
    if events & Bluetooth.CLIENT_CONNECTED:
        print("BLE client connected")
    elif events & Bluetooth.CLIENT_DISCONNECTED:
        print("BLE client disconnected")


def chr1_cb_handler(chr, data):
    global last_read_event_time

    humidity = dht.humidity()
    chr.value(str(humidity))
    print("BLE transmitted :", humidity)

    last_read_event_time = time.time()

def use_wifi():
    # Create a socket object with options:
    # - socket.AF_INET: For use with Internet protocols (WiFi, LTE, Ethernet)
    # - socket.SOCK_STREAM: Creates a stream socket (INET socket only, UDP protocol only)
    #
    # We use UDP, rather than TCP, to reduce network overhead.
    sock = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)

    # Connect to the server
    try:
        sock.connect((SERVER, PORT))

        print('Connected to server')

        # Construct a message with format: CSV humidity, temperature
        humidity = str(dht.humidity())
        temperature = str(dht.temperature())
        message = f'{humidity},{temperature}'

        sock.send(message.encode())

        print("WIFI transmitted :", message)
    except OSError as e:
        sock.close()
        raise

    # Close the connection to the server
    sock.close()

bluetooth = Bluetooth()
bluetooth.set_advertisement(name='FiPy 45', manufacturer_data="Pycom", service_uuid=SERVICE_UUID)

bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=conn_cb)
bluetooth.advertise(True)

srv1 = bluetooth.service(uuid=SERVICE_UUID, isprimary=True, nbr_chars=1)
chr1 = srv1.characteristic(uuid=CHARACTERISTIC_UUID, value='read_from_here')

chr1.callback(trigger=Bluetooth.CHAR_READ_EVENT, handler=chr1_cb_handler)

print('BLE service started')

while True:
    if time.time() - last_read_event_time > 3.0:
        print("BLE failed, use WIFI")
        use_wifi()
        last_read_event_time = time.time()

    time.sleep(0.1)

