import serial, time

def start_scanning(comport, baudrate):

    print(f"Conectare la {comport}")
    arduino_ser = serial.Serial(comport, baudrate, timeout=1)
    time.sleep(2) # wait 2 sec to let arduino reset
    text_file = open("./coords.xyz", "w")

    print("Conectat")
    try:
        while True:
            # read line, decode from bytes to text and strip white spaces/ end line
            data = arduino_ser.readline().decode('utf-8').strip()

            if data == 'end':
                print("Scanare termninata")

                if 'arduino_ser' in locals() and arduino_ser.is_open:
                    arduino_ser.close()
                    print("Port serial inchis")

                break

            if ',' in data:
                text_file.write(data)
                text_file.flush()
                
            print(data)

    except Exception:
        print("Eroare")

    finally:
        if 'arduino_ser' in locals() and arduino_ser.is_open:
            arduino_ser.close()
            print("Port serial inchis")
        if "text_file" in locals() and text_file:
            text_file.close()
            print("Fisier inchis")