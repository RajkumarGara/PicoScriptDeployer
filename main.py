import network
import socket
import time
from machine import UART, Pin

# Network credentials
WIFI_SSID = 'your_wifi_ssid'
WIFI_PASSWORD = 'your_wifi_password'

# Server details
IP_ADDRESS = 'your_device_ip_address'
TCP_PORT = 50000 

# Initialize UART and LED
uart1 = UART(1, 19200)
uart1.init(19200, bits=8, parity=None, stop=1, tx=4, rx=5)
led = Pin("LED", Pin.OUT)

def blink_led():
    led.toggle()

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

while not wlan.isconnected():
    blink_led()
    time.sleep(0.1)

led.off()
print("Connected to WiFi")

# Establish a new TCP connection with retry mechanism
def create_tcp_connection():
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((IP_ADDRESS, TCP_PORT))
            print("Connected to TCP server")
            return sock
        except Exception as e:
            print(f"Failed to connect to TCP server: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)

# Create initial TCP socket and connect
s = create_tcp_connection()
led.on()

try:
    while True:
        # Check for incoming UART data first
        if uart1.any():
            rxed = uart1.read().decode('utf-8').rstrip()
            s.send(rxed.encode())
            blink_led()
            # print("from MechoNet: ", rxed)

        # Non-blocking check for TCP data
        s.setblocking(False)
        try:
            data = s.recv(1024)
            if data == b'':  # TCP connection closed
                print("TCP connection closed by server. Reconnecting...")
                s.close()
                s = create_tcp_connection()
                print("Reconnected to server.")
                continue

            if data:
                cmd = data.decode()
                uart1.write(cmd)
                blink_led()
                # print("from Node-RED: ", cmd)

        except Exception as e:
            pass  # No data received, normal for non-blocking call

        s.setblocking(True)
        time.sleep(0.1)  # Short delay to prevent CPU overload

except Exception as e:
    print("An error occurred:", e)
finally:
    s.close()
    print("TCP socket closed")