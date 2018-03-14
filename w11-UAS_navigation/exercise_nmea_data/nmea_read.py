#!/usr/bin/python
#/****************************************************************************
# nmea read function
# Copyright (c) 2018, Kjeld Jensen <kj@kjen.dk>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the copyright holder nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#****************************************************************************/
'''
2018-03-13 Kjeld First version, that reads in CSV data
2018-03-14 Per Breum - add plot function
'''

from pylab import ion
import matplotlib.pyplot as plt
import numpy as np
import math
from datetime import datetime
import time

class nmea_class:
    def __init__(self):
        self.data = []

    def import_file(self, file_name):
        file_ok = True
        try:
          # read all lines from the file and strip \n
          lines = [line.rstrip() for line in open(file_name)]
        except:
          file_ok = False
        if file_ok == True:
          pt_num = 0
          for i in range(len(lines)): # for all lines
            if len(lines[i]) > 0 and lines[i][0] != '#': # if not a comment or empty line
              csv = lines[i].split (',') # split into comma separated list
              self.data.append(csv)

    def print_data(self):
        for i in range(len(self.data)):
          print self.data[i]

    # use timestamp to calculate seconds for time axis
    def get_time_array(self):
        time = []
        start_time = self.data[0][1]
        seconds_start = 60 * 60 * int(start_time[0:2]) + 60 * int(start_time[2:4]) + int(start_time[4:6])

        for i in range(len(self.data)-1):
            hour = int(self.data[i][1][0:2]) * 60 * 60
            minutes = int(self.data[i][1][2:4]) * 60
            seconds = int(self.data[i][1][4:6])
            time = np.append(time, (hour + minutes + seconds)-seconds_start)
        return time

    def get_column(self, col_num):
        column = []
        for i in range(len(self.data)-1):
            column = np.append(column, self.data[i][col_num])
        return column

    def plot_data(self, x, y, title, xlabel, ylabel, filename_save):
        plt.figure(1)
        plt.title(title, fontsize=23)
        plt.plot(x, y, linewidth=1.0)

        y_max = np.asfarray(max(y), int) * 1.1
        y_min = np.asfarray(min(y), int) * 0.9
        print(y_max)
        plt.ylim(y_min, y_max)
        plt.xlim(0, x[-1])
        plt.xlabel(xlabel, fontsize=20)
        plt.ylabel(ylabel, fontsize=20)
        plt.show()
        plt.savefig(filename_save)
        print('Press enter to quit')
        input()

    def plot_nmea_data(self):
        ion()

        # get seconds from timestamp difference from column 1
        time = self.get_time_array()

        # get altitude from column 9
        altitude_msl = self.get_column(9)

        # get number of satellites tracked from column
        tracked_satellites = self.get_column(7)
        print(tracked_satellites)

        self.plot_data(time, altitude_msl, "Altitude above MSL measured over time", "Time in seconds", "Height in meters", "altitude_above_msl_measured_over_time")


if __name__ == "__main__":
  print 'Importing file'
  nmea = nmea_class()
  nmea.import_file ('nmea_trimble_gnss_eduquad_flight.txt')

  #nmea.print_data()

  nmea.plot_nmea_data()
