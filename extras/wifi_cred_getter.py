import os
import subprocess
import socket

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

# Function to write WiFi credentials to a file
def write_pi_wifi_credentials():
    ssid = get_active_wifi_connection()
    ip_address = get_ip_address()

    if ssid:
        ssid, wifi_password = get_wifi_credentials(ssid)
        if wifi_password:
            with open('config.txt', 'w') as config_file:
                config_file.write(f"WIFI_SSID = '{ssid}'\n")
                config_file.write(f"WIFI_PASSWORD = '{wifi_password}'\n")
                config_file.write(f"IP_ADDRESS = '{ip_address}'\n")
            print("Wi-Fi credentials written to config.txt")
        else:
            print("Wi-Fi password not found")
            print("Wi-Fi credentials are not written to config.txt")
    else:
        print("Wi-Fi SSID not found")
        print("Wi-Fi credentials are not written to config.txt")

def read_config_and_update_main():
    # Read Wi-Fi credentials from config.txt
    with open('config.txt', 'r') as config_file:
        config_lines = config_file.readlines()

    ssid_line = config_lines[0].strip()
    password_line = config_lines[1].strip()
    ip_address_line = config_lines[2].strip()

    # Read the main.py file
    with open('main.py', 'r') as main_file:
        main_lines = main_file.readlines()

    # Update the SSID and password in main.py
    main_lines[6] = ssid_line + '\n'
    main_lines[7] = password_line + '\n'
    main_lines[10] = ip_address_line + '\n'

    # Write the updated main.py file
    with open('main.py', 'w') as main_file:
        main_file.writelines(main_lines)

    print("main.py is updated with the Wi-Fi credentials from config.txt")

def main():
    write_pi_wifi_credentials()  # Attempt to write Wi-Fi credentials
    read_config_and_update_main()

if __name__ == "__main__":
    main()