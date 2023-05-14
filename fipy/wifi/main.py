import usocket
import utime
from network import WLAN
import pycom
import sys
import machine

from SI7006A20 import SI7006A20
from pycoproc_2 import Pycoproc

# Socket References:
# - https://docs.pycom.io/firmwareapi/micropython/usocket/
# - https://docs.pycom.io/tutorials/networkprotocols/socket/
#
# Network references:
# - https://docs.pycom.io/firmwareapi/pycom/network/wlan/
# - https://docs.pycom.io/tutorials/networks/wlan/
#
# Sensing references:
# - https://docs.pycom.io/tutorials/expansionboards/sensing/
#
# Other references:
# - https://docs.pycom.io/firmwareapi/micropython/utime/
# - https://github.com/micropython/micropython-lib/blob/master/python-ecosys/urequests/urequests.py

SERVER = '192.168.1.36'  # Replace with the server's IP address
PORT = 8090  # Replace with the server's IP port
SSID = 'AP200'  # Replace with the name of your WiFi network
WPA2_KEY = 'LarsWard'  # Replace with the password of your WiFi network

# Disable heartbeat LED to save power
pycom.heartbeat(False)

# Create WLAN interface as a station
wlan = WLAN(mode=WLAN.STA)

# Initialise the DHT temperature and humidity sensor
py = Pycoproc()
dht = SI7006A20(py)

# Setup network connection
wlan.connect(ssid=SSID, auth=(WLAN.WPA2, WPA2_KEY))

while not wlan.isconnected():
    print('Trying to connect to WLAN')
    utime.sleep_ms(500)
print('Connect to WLAN success')

# We can either:
# - keep the socket open or
# - establish a new connection before each message sent
#
# Keeping a socket open is more efficient in terms of network overhead.
# However, network connection may be lost or disrupted at some point,
# which could cause the socket to become invalid or unusable.
while True:

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

        # Construct a message containing the humidity
        message = str(dht.humidity())

        sock.send(message.encode())

        print('Message sent')
    except OSError as e:
        sock.close()
        raise

    # Close the connection to the server
    sock.close()

    # The boolean value enables or disable
    # restoring after wakeup any WiFi or BLE connection that was interrupted by light sleep.
    # This should be more power efficient than `utime.sleep_ms(5000)`
    # machine.sleep(5000, True)

    utime.sleep_ms(5000)
