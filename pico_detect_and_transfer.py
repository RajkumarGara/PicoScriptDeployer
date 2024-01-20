import os
import time
import serial.tools.list_ports

def is_pico_connected():
    # Check for connected USB devices and identify the Pico by its VID and PID
    pico_vid = 0x2E8A  # Pico's Vendor ID in hexadecimal
    pico_pid = 0x0005  # Pico's Product ID in hexadecimal
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if port.vid == pico_vid and port.pid == pico_pid:
            return True
    return False

def transfer_script_to_pico():
    # Use rshell to transfer the script to the Pico
    # Replace '/dev/ttyACM0' with the actual port if necessary
    # You might need to adjust this command based on your setup
    os.system('rshell -p /dev/ttyACM0 "cp main.py /pyboard"')

print("Waiting for Pico to be connected...")
while True:
    if is_pico_connected():
        print("Pico detected. Transferring the main.py script.")
        transfer_script_to_pico()
        print("Script transferred. Exiting.")
        break
    else:
        print("Pico not found. Retrying...")
        time.sleep(5)  # Check every 5 seconds
