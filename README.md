
# About

## Installation of Prerequisites
* Open terminal in Raspberry Pi and enter the below commands to install `rshell`, `adafruit-ampy`.
``` bash
sudo apt update
mkdir ~/python-environments
cd ~/python-environments
python3 -m venv rshell-env
pip install rshell
pip install adafruit-ampy
pip install pyserial
```

## Getting the pico identity
 * Copy [`pico_id.py`](./pico_id.py) to the path `~/python-environments`
 * Connect pico to pi through usb and run [`pico_id.py`](./pico_id.py) to get the VID and PID of pico
 ``` bash
cd ~/python-environments
python3 pico_id.py
```
* Modify the [`pico_detect_and_transfer.py`](./pico_detect_and_transfer.py) with the above obtained VID and PID in line 7 and 8.

## Running the code
* Copy [`main.py`](./main.py) (code file that needs to run on pico) to the path `~/python-environments`
*  Copy [`pico_detect_and_transfer.py`](./pico_detect_and_transfer.py) to the path `~/python-environments`
* Open terminal in Raspberry Pi and enter the below command to run the code.
``` bash
cd ~/python-environments
source ~/python-environments/rshell-env/bin/activate
python3 pico_detect_and_transfer.py
deactivate
```
