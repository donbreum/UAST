#!/usr/bin/python3
# Standard libraries
import bokeh.plotting as bkplot
import numpy as np


def plot_data(input_data, show_result=True, title="Title", fname="result"):
    bkplot.output_file("./results/{}.html".format(fname))
    plt = bkplot.figure(title=title, x_axis_label='duty cycle',
                        y_axis_label='thust')
    # Parse the values to plot from the input data.
    x = input_data[0, :, 0]
    y0 = input_data[0, :, 1]
    y1 = input_data[1, :, 1]
    y2 = input_data[2, :, 1]
    y_mean = input_data[:, :, 1].mean(axis=0)
    # Get the polynomial fitting for the data average
    poly_coefs = np.polyfit(x, y_mean, 2)
    poly_parser = np.poly1d(poly_coefs)
    y_fitted = poly_parser(x)
    # Draw the plots on a bakeh figure
    plt.circle(x, y0, legend="test 1", fill_color="white", line_color="green",
               size=6)
    plt.circle(x, y1, legend="test 2", fill_color="orange", line_color="black",
               size=6)
    plt.circle(x, y2, legend="test 3", fill_color="red", line_color="red",
               size=6)
    plt.line(x, y_mean, legend="average", line_color="blue")
    plt.line(x, y_fitted, legend="fitted", line_color="red", line_width=2)
    plt.legend.location = "bottom_right"
    if show_result:
        bkplot.show(plt)
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
