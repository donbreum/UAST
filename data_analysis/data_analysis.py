#!/usr/bin/python3
# Standard libraries
import bokeh.plotting as bkplot
import numpy as np


def plot_data(input_data, title="Test title", fname="result"):
    bkplot.output_file("./results/{}.html".format(fname))
    p = bkplot.figure(title=title, x_axis_label='duty cycle',
               y_axis_label='thust')
    x = input_data[0, :, 0]
    y0 = input_data[0, :, 1]
    y1 = input_data[1, :, 1]
    y2 = input_data[2, :, 1]

    p.line(x, y0, legend="test 1", line_color="green")
    p.circle(x, y0, legend="test 1", fill_color="white", line_color="green", size=8)
    p.line(x, y1, legend="test 2", line_color="blue")
    p.circle(x, y2, legend="test 3", fill_color="red", line_color="red", size=6)
    p.line(x, y2, legend="test 3", line_color="orange", line_dash="4 4")

    bkplot.show(p)
    return


def main():
    filename = "./resources/motor_test.csv"
    data = np.loadtxt(filename, delimiter=";")
    # Re-arange the data in an array for each propeller, divided in a
    # sub-array for each test
    prop_8cw = data[0:63, :].reshape((3, 21, 2))
    prop_10cw = data[63:126, :].reshape((3, 21, 2))
    prop_ccw = data[126:189, :].reshape((3, 21, 2))
    # Plot the values
    plot_data(prop_8cw, title="8 inch CW propeller", fname="cw_8inch")
    plot_data(prop_10cw, title="10 inch CW propeller", fname="cw_10inch")
    plot_data(prop_ccw, title="CCW propeller", fname="ccw")
    return


if __name__ == "__main__":
    main()