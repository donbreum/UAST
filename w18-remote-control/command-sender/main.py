#!/usr/bin/python3
# Standard libraries
import serial


def main():
    # Initialize and configure serial port
    port = glob.glob("/dev/ttyUSB*")[0]
    ser =serial.Serial(port, 115200)
    ser.timeout = 0.5
    
    return


if __name__ == "__main__":
    main()