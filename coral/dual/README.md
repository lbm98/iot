## Sources

### Setup

```bash
sudo apt install python3-venv libglib2.0-dev
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

### Run

Start the IP server as a background process
```bash
venv/bin/python wifi.py &
```

Close the IP server
```bash
pkill -f "venv/bin/python wifi.py"
```

Run the BLE functions
```bash
sudo venv/bin/python ble.py
```