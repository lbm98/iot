# The coral collects data from the sensors
# and will send it to the cloud.
# Here we define parameters related to the cloud connection.
CLOUD_HOST = '192.168.1.28'  # Could change because of DHCP
CLOUD_PORT = 8080
CLOUD_PATH = '/sensor'
CLOUD_URL = f'http://{CLOUD_HOST}:{CLOUD_PORT}{CLOUD_PATH}'