#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" 
IMU exercise

Copyright (c) 2015-2018 Kjeld Jensen kjen@mmmi.sdu.dk kj@kjen.dk

Main changes:
* Added a main() function for the main code, encapsulating the scope
* Divided the code in various functions, for increasing modularity
* Open the files with the 'with' statement, to make the file management
safer (preventing damage if the script is unexpectedly aborted)
* Change the import of math, so the full namespace is used. This is a
recommended way of importing according to PEP8
* Changed indentation to 4-spaces (PEP8 standard).
* Clustered the accelerometer and gyro measures in 2 arrays, so they can
be manipulated easier, and vectorization can be implemented in the
future.
"""
# Standard libraries
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


def draw_plot(y_data, out_file="imu_exercise_plot.png", title="title"):
    if len(y_data) == 2:
        fig, axes = plt.subplots(2, sharex=True)
        axes[0].plot(y_data[0], linewidth=0.5, color='g')
        axes[1].plot(y_data[1], linewidth=0.5, color='b')
        axes[1].set_ylim( axes[0].get_ylim() )
    else:
        fig, axes = plt.subplots()
        axes.plot(y_data, linewidth=0.5, color='g')
    fig.suptitle(title, fontsize=20)
    fig.text(0.04, 0.5, "Angle [°]", va='center', rotation='vertical')
    fig.savefig("./results/{}".format(out_file))
    plt.show()
    # 
    # plt.ylabel("Angle [°]")
    # plt.title("{} angles for IMU razor".format(angle_name))
    # plt.savefig(out_file)
    # plt.show()
    return


def read_params(line, imu_type, init, ts_now=0):
    """Parse the measured values from a text file line."""
    # split the line into CSV formatted data
    line = line.replace ('*',',') # make the checkum another csv value
    csv = line.split(',')

    # keep track of the timestamps 
    ts_recv = float(csv[0])
    if init: 
        ts_now = ts_recv # only the first time
    ts_prev = ts_now
    ts_now = ts_recv

    if imu_type == 'sparkfun_razor':
        # import data from a SparkFun Razor IMU (SDU firmware)
        acc_x = int(csv[2]) / 1000.0 * 4 * 9.82;
        acc_y = int(csv[3]) / 1000.0 * 4 * 9.82;
        acc_z = int(csv[4]) / 1000.0 * 4 * 9.82;
        gyro_x = int(csv[5]) * 1/14.375 * math.pi/180.0;
        gyro_y = int(csv[6]) * 1/14.375 * math.pi/180.0;
        gyro_z = int(csv[7]) * 1/14.375 * math.pi/180.0;
    elif imu_type == 'vectornav_vn100':
        # import data from a VectorNav VN-100 configured to output $VNQMR
        acc_x = float(csv[9])
        acc_y = float(csv[10])
        acc_z = float(csv[11])
        gyro_x = float(csv[12])
        gyro_y = float(csv[13])
        gyro_z = float(csv[14])
    else:
        acc_x, acc_y, acc_z = (0, 0, 0)
        gyro_x, gyro_y, gyro_z = (0, 0, 0)
    # Cluster the read values in 2 NumPy arrays.
    acc = np.array([acc_x, acc_y, acc_z])
    gyro = np.array([gyro_x, gyro_y, gyro_z])
    return (acc, gyro, ts_now)


def get_angle_values(filename, imu_type, get_pitch=True, get_roll=True):
    """Loop through file and get the desired angle.
    
    TODO: This code should be optimized using vector operations i.e.
    store the each measurement on an array, and calculate the pitch for
    all iterations with a vectorial operation
    (numpy.atan2 instead math.atan2).
    """
    with open(filename, 'r') as f:
        pitch_data = []
        roll_data = []
        init = True
        for line in f:
            acc, gyro, _ = read_params(line, imu_type, init)
            # Set the flag to False after the 1st iteration.
            if init:
                init = False
            # Calculate pitch from the sensor measurements using eq.28
            # Switching pitch-roll naming convention from the provided PDF
            if get_pitch:
                pitch = math.atan2(acc[1], math.sqrt(acc[0]**2+acc[2]**2))
                pitch_data.append(pitch*180.0/math.pi)
            if get_roll:
                roll = math.atan2(-acc[0], acc[2])
                roll_data.append(roll*180.0/math.pi)
    return (pitch_data, roll_data)


def lowpass_filter(data, ksize=3):
    """
    Apply a basic lowpass filter, consisting in the arithmetic mean.
    """
    kernel = np.ones(ksize)
    filtered = signal.convolve(data, kernel, "valid") / ksize
    return filtered


def main():
    ##### Insert initialize code below ###################

    ## Uncomment the file to read ##
    noisy_filename = 'imu_razor_data_static.txt'
    pitch_filename = 'imu_razor_data_pitch_55deg.txt'
    roll_filename = 'imu_razor_data_roll_65deg.txt'
    #filename = 'imu_razor_data_yaw_90deg.txt'

    ## IMU type
    #imu_type = 'vectornav_vn100'
    imu_type = 'sparkfun_razor'

    ## Variables for plotting ##
    show_plot = True

    ## Initialize your variables here ##
    my_value = 0.0

    pitch_data, _ = get_angle_values(pitch_filename, imu_type, get_roll=False)
    _, roll_data = get_angle_values(roll_filename, imu_type, get_pitch=False)
    noisy_pitch, noisy_roll = get_angle_values(noisy_filename, imu_type)
    filtered_pitch = lowpass_filter(noisy_pitch, ksize=40)
    filtered_roll = lowpass_filter(noisy_roll, ksize=40)

    # show the plot
    if show_plot == True:
        draw_plot(pitch_data, "imu_exercise_pitch_plot.png", 
                  "Pitch angles for IMU razor with 55°")
        draw_plot(roll_data, "imu_exercise_roll_plot.png",
                  "Roll angles for  IMU razor with 65°")
        draw_plot((noisy_pitch, filtered_pitch), "imu_noisy_pitch10_plot.png",
                  "Noisy pitch and mean filtered (K = 40x1)")
        draw_plot((noisy_roll, filtered_roll), "imu_noisy_roll10_plot.png",
                  "Noisy roll and mean filtered (K = 40x1)")
    return


if __name__ == "__main__":
    main()
