#!/usr/bin/python3
# Standard libraries
import glob
import serial
import struct


def send_integer(value, ser):
    """
    Send through serial port an integer formated as a 16-bit ushort.
    """
    message = struct.pack("I", value)
    ser.write(message)
    return


def main():
    # Initialize and configure serial port
    try:
        port = glob.glob("/dev/ttyUSB*")[0]
    except IndexError:
        print("Any device detected. Aborting ...")
        return
    ser =serial.Serial(port, 115200)
    ser.timeout = 0.5
    # Infinite loop for getting input from user and sending through port.
    while(True):
        usr_input = input("Enter a value between 0 and 65535: ")
        try:
            value = int(usr_input)
        except ValueError:
            print("Non valid input. Only integers")
            continue
        print("Sending {}".format(value))
        send_integer(value, ser)
    return


if __name__ == "__main__":
    main()
