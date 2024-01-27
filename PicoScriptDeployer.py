import os
import subprocess
import sys
import time
import serial.tools.list_ports
import socket
import tempfile

# Function to check if the script is running as root
def is_root_user():
    return os.geteuid() == 0

# Function to get the active WiFi connection's SSID
def get_active_wifi_connection():
    ssid = subprocess.check_output("nmcli -t -f active,ssid dev wifi | grep yes: | cut -d ':' -f2", shell=True).decode().strip()
    return ssid

# Function to get WiFi credentials
def get_wifi_credentials(ssid):
    config_path = f'/etc/NetworkManager/system-connections/{ssid}.nmconnection'
    psk = None

    if os.path.exists(config_path):
        with open(config_path, 'r') as file:
            for line in file:
                if 'psk=' in line:
                    psk = line.split('=')[1].strip()
                    break
    return ssid, psk

# Function to get IP address
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

# Function to write WiFi credentials to a manually managed temporary file
def write_wifi_credentials_to_temp_file():
    ssid = get_active_wifi_connection()
    ssid, wifi_password = get_wifi_credentials(ssid)
    # Create a temporary file path in a way that ensures proper permissions
    temp_dir = tempfile.gettempdir()
    temp_file_path = os.path.join(temp_dir, "wifi_credentials.txt")
    with open(temp_file_path, 'w') as file:
        file.write(f"{ssid}\n{wifi_password}\n{get_ip_address()}")
    # Change the file permissions to ensure it can be read without sudo
    os.chmod(temp_file_path, 0o644)
    return temp_file_path

# Function to get connected Picos
def get_connected_picos():
    pico_vid = 0x2E8A  # Pico's Vendor ID
    pico_pid = 0x0005  # Pico's Product ID
    connected_picos = []
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if port.vid == pico_vid and port.pid == pico_pid:
            connected_picos.append(port.device)
    return connected_picos

# Function to transfer script to Pico
def transfer_script_to_pico(port):
    os.system(f'rshell -p {port} "cp main.py /pyboard"')

# Function to read config and update main.py
def read_config_and_update_main(temp_cred_file):
    with open(temp_cred_file, 'r') as file:
        ssid_line = file.readline().strip()
        password_line = file.readline().strip()
        ip_address_line = file.readline().strip()

    with open('main.py', 'r') as main_file:
        main_lines = main_file.readlines()

    main_lines[6] = f"WIFI_SSID = '{ssid_line}'\n"
    main_lines[7] = f"WIFI_PASSWORD = '{password_line}'\n"
    main_lines[10] = f"IP_ADDRESS = '{ip_address_line}'"

    with open('main.py', 'w') as main_file:
        main_file.writelines(main_lines)

    print("main.py is updated with the Wi-Fi credentials from config.txt")

# Main function
def main():
    if not is_root_user():
        print("Restarting script with sudo for Wi-Fi credentials.")
        temp_cred_file = subprocess.check_output(["sudo", "python3", __file__, "get_wifi_credentials"])
        temp_cred_file = temp_cred_file.decode().strip()

        print("Waiting for Pico to be connected...")
        known_picos = set()

        while True:
            current_connected_picos = set(get_connected_picos())
            new_picos = current_connected_picos - known_picos

            for pico_port in new_picos:
                print(f"Pico detected at {pico_port}.")
                read_config_and_update_main(temp_cred_file)
                print("Transferring the main.py script.")
                transfer_script_to_pico(pico_port)
                print("Script transferred.")

            known_picos = current_connected_picos
            time.sleep(5)

        os.unlink(temp_cred_file)
    else:
        if "get_wifi_credentials" in sys.argv:
            temp_cred_file = write_wifi_credentials_to_temp_file()
            print(temp_cred_file)  # This will be captured by subprocess.check_output

if __name__ == "__main__":
    main()
