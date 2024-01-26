import os
import subprocess

def get_active_wifi_connection():
    try:
        # Getting the current active SSID using nmcli
        ssid = subprocess.check_output("nmcli -t -f active,ssid dev wifi | grep yes: | cut -d ':' -f2", shell=True).decode().strip()
        return ssid
    except subprocess.CalledProcessError as e:
        print(f"Error getting active Wi-Fi connection: {e}")
        return None

def get_wifi_credentials(ssid):
    psk = None
    config_path = f'/etc/NetworkManager/system-connections/{ssid}.nmconnection'

    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if 'psk=' in line:
                        psk = line.split('=')[1].strip()
                        break
    except Exception as e:
        print(f"Error reading Wi-Fi credentials: {e}")
        return None, None

    return ssid, psk

def write_pi_wifi_credentials():
    print("Getting Wi-Fi SSID and password...")
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


def main():
    write_pi_wifi_credentials()

if __name__ == "__main__":
    main()