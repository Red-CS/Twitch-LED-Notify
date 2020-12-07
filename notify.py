import time
import serial

serialcomm = serial.Serial('COM5', 115200)
serialcomm.timeout = 1

while True:
    i = input("input(on/off): ").strip()
    if i == 'done':
        print("Finished program")
        break
    serialcomm.write(i.encode())
    time.sleep(0.5)
    print(serialcomm.readline().decode('ascii'))

serialcomm.close()