import os
import time
import serial.tools.list_ports

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


def main():
    known_picos = set()

    while True:
        current_connected_picos = set(get_connected_picos())

        # Transfer script to any newly connected Picos
        new_picos = current_connected_picos - known_picos
        for pico_port in new_picos:
            print(f"Pico detected at {pico_port}. Transferring the main.py script.")
            read_config_and_update_main()
            transfer_script_to_pico(pico_port)
            print("Script transferred.")

        known_picos = current_connected_picos
        time.sleep(5)

if __name__ == "__main__":
    print("Waiting for Pico(s) to be connected...")
    main()