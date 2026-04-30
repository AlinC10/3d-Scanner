import serial.tools.list_ports

def get_com_port():
    ports = list(serial.tools.list_ports.comports())

    # name for arduino or fake arduino's
    search_names = ["ARDUINO", "CH340", "CH341", "CP210", "FTDI", "USB-SERIAL"]

    for port in ports:
        description = port[1].upper()

        for name in search_names:
            if name in description:
                return port[0]

    return None