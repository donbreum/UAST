#!/usr/bin/python3
# Standard libraries
import glob
import serial
import time

def get_user_input():
    message = input('Enter set point (0-100) or S for stop ')
    return message

def set_speed(ser, speed):
    message = ("1{sp}".format(sp=speed)).encode()
    ser.write(message)
    return

def main():
    port = glob.glob("/dev/ttyUSB*")[0]
    ser = serial.Serial(port, 115200)
    ser.timeout = 0.5
    # Initialize communication
    ser.write("2".encode())
    time.sleep(2)
    answer = ser.read(50)
    print(answer)
    ## Calibrate ESC.
    set_speed(ser, 100)
    time.sleep(3)
    set_speed(ser, 11)
    time.sleep(3)
    answer = ser.read(50)
    print(answer)
    time.sleep(1)
    # Start the main loop, where user is asked for set points
    stop=False
    while (not stop):
        message = get_user_input()
        if message in ("S", "s", "stop", "Stop"):
            set_speed(ser, 0)
            ser.write("3".encode())
            time.sleep(1)
            answer = ser.read(50)
            print(answer)
            stop = True
        else:
            try:
                speed = int(message)
            except ValueError:
                pass
            else:
                set_speed(ser, speed)
    return


if __name__ == "__main__":
    main()