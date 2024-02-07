# About
This project automatically sends Python code to the Pico-W when it connects to the Raspberry Pi. Running  [`PicoScriptDeployer.py`](./PicoScriptDeployer.py) fetches the Wi-Fi SSID, password and IP-address from the Pi and saves them in [`config.txt`](./config.txt), without overwriting existing details if new ones aren't found. The script waits for a Pico connection. Once a Pico is connected to the Pi, it updates the Wi-Fi credentials in [`main.py`](./main.py) with the details from "config.txt" and then transfers the updated code to the Pico. This project is an extension for [`pico-network-serial-port`](https://github.com/RajkumarGara/pico-network-serial-port).

## Installation of Prerequisites
* Open terminal in Raspberry Pi and enter the below commands to install `rshell`.
    ``` bash
    sudo apt update
    mkdir ~/python-environments
    cd ~/python-environments
    python -m venv rshell-env
    source ~/python-environments/rshell-env/bin/activate
    pip install rshell
    ```

## Running the code
* Copy [`PicoScriptDeployer.py`](./PicoScriptDeployer.py), [`config.txt`](./config.txt), and [`main.py`](./main.py) (code that needs to run on Pico) to the path `~/python-environments`.
* Open terminal on the Raspberry Pi and enter below commands to run the code.
    ``` bash
    cd ~/python-environments
    source ~/python-environments/rshell-env/bin/activate
    python PicoScriptDeployer.py
    ```

## Setup
* Connect Pico-W (the target board) to the Pi through usb cable.
    ![pi](img/pi.png)
    ![pico](img/pico.png)
    ![terminal](img/terminal.png)

## Developer Notes
* The [`main.py`](./main.py) will be deployed only to the most recently connected Pico if multiple Picos are attached to the Pi.
* If [`PicoScriptDeployer.py`](./PicoScriptDeployer.py) cannot detect your Wi-Fi details, you can manually update [`config.txt`](./config.txt) with the correct credentials.
* After the code is deployed to the Pico, it will automatically reset and run the code.
* Files in the [`extras`](./extras) folder are optional for this project. See the points below for more details.
    * Run [`wifi_cred_getter.py`](./extras/wifi_cred_getter.py) on the Pi to retrieve its wifi SSID, password and IP-address, and save these details in [`config.txt`](./config.txt). 
    * Run [`PicoJustScriptDeployer.py`](./extras/PicoJustScriptDeployer.py) on the Pi connected to the Pico to deploy [`main.py`](./main.py) on the Pico without modifying the wifi credentials. 
    * Run [`pico_id_getter.py`](./extras/pico_id_getter.py) on the Pi connected to the Pico to get the Pico VID and PID.