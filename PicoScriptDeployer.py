import os
import subprocess
import time
import serial.tools.list_ports

# Function to get the active WiFi connection's SSID
def get_active_wifi_connection():
    print("Getting Wi-Fi credentials")
    try:
        ssid = subprocess.check_output("nmcli -t -f active,ssid dev wifi | grep yes: | cut -d ':' -f2", shell=True).decode().strip()
        return ssid
    except subprocess.CalledProcessError:
        return None

# Function to get WiFi credentials
def get_wifi_credentials(ssid):
    psk = None
    config_path = f'/etc/NetworkManager/system-connections/{ssid}.nmconnection'

    if os.path.exists(config_path):
        with open(config_path, 'r') as file:
            for line in file:
                if 'psk=' in line:
                    psk = line.split('=')[1].strip()
                    break
    return ssid, psk

# Function to write WiFi credentials to a file
def write_pi_wifi_credentials():
    ssid = get_active_wifi_connection()
    if ssid:
        ssid, wifi_password = get_wifi_credentials(ssid)
        if wifi_password:
            with open('config.txt', 'w') as cred_file:
                cred_file.write(f"WIFI_SSID = '{ssid}'\n")
                cred_file.write(f"WIFI_PASSWORD = '{wifi_password}'")
            print("Wi-Fi credentials written to config.txt")
        else:
            print("Wi-Fi password not found")
            print("Wi-Fi credentials are not written to config.txt")
    else:
        print("Wi-Fi SSID not found")
        print("Wi-Fi credentials are not written to config.txt")

# Rest of the PicoScriptDeployer code
def get_connected_picos():
    pico_vid = 0x2E8A  # Pico's Vendor ID
    pico_pid = 0x0005  # Pico's Product ID
    connected_picos = []
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if port.vid == pico_vid and port.pid == pico_pid:
            connected_picos.append(port.device)
    return connected_picos

def transfer_script_to_pico(port):
    os.system(f'rshell -p {port} "cp main.py /pyboard"')

def read_config_and_update_main():
    # Read Wi-Fi credentials from config.txt
    with open('config.txt', 'r') as config_file:
        config_lines = config_file.readlines()

    ssid_line = config_lines[0].strip()
    password_line = config_lines[1].strip()

    # Read the main.py file
    with open('main.py', 'r') as main_file:
        main_lines = main_file.readlines()

    # Update the SSID and password in main.py
    main_lines[6] = ssid_line + '\n'
    main_lines[7] = password_line + '\n'

    # Write the updated main.py file
    with open('main.py', 'w') as main_file:
        main_file.writelines(main_lines)

    print("main.py is updated with the Wi-Fi credentials from config.txt")

def main():
    write_pi_wifi_credentials()  # Attempt to write Wi-Fi credentials

    print("Waiting for Pico to be connected...")
    known_picos = set()

    while True:
        current_connected_picos = set(get_connected_picos())

        # Transfer script to any newly connected Picos
        new_picos = current_connected_picos - known_picos
        for pico_port in new_picos:
            print(f"Pico detected at {pico_port}.")
            read_config_and_update_main()
            print("Transferring the main.py script.")
            transfer_script_to_pico(pico_port)
            print("Script transferred.")

        known_picos = current_connected_picos
        time.sleep(5)

if __name__ == "__main__":
    main()