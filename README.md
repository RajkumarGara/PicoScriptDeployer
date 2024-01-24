
# About
The script will automatically upload the Python script to the Pico as soon as it's connected to the Pi.

## Installation of Prerequisites
* Open terminal in Raspberry Pi and enter the below commands to install `rshell`.
``` bash
sudo apt update
mkdir ~/python-environments
cd ~/python-environments
python3 -m venv rshell-env
pip install rshell
pip install pyserial
```

## Running the code
* Copy [`main.py`](./main.py) (code file that needs to run on pico) to the path `~/python-environments`
*  Copy [`pico_detect_and_transfer.py`](./pico_detect_and_transfer.py) to the path `~/python-environments`
* Open terminal in Raspberry Pi and enter the below command to run the code.
``` bash
cd ~/python-environments
source ~/python-environments/rshell-env/bin/activate
python pico_detect_and_transfer.py
```

## Setup
* Connect the pico-w (the target board) to the pi through usb cable.
![pi](img/pi.png)
![pico](img/pico.png)