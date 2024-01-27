import os
import time
import serial.tools.list_ports


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


def main():
    print("Waiting for Pico to be connected...")
    known_picos = set()

    while True:
        current_connected_picos = set(get_connected_picos())

        # Transfer script to any newly connected Picos
        new_picos = current_connected_picos - known_picos
        for pico_port in new_picos:
            print(f"Pico detected at {pico_port}.")
            print("Transferring the main.py script.")
            transfer_script_to_pico(pico_port)
            print("Script transferred.")

        known_picos = current_connected_picos
        time.sleep(5)


if __name__ == "__main__":
    main()