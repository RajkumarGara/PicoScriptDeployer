import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
for port in ports:
    vid = port.vid
    pid = port.pid
    if vid is not None and pid is not None:
        print("VID: {:04X}".format(vid))
        print("PID: {:04X}".format(pid))
    else:
        print("Device without VID and PID found")