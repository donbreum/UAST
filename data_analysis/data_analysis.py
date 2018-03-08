#!/usr/bin/python3
# Standard libraries
import bokeh.plotting as bkplot
import numpy as np


def plot_data(input_data, show_result=True, title="Title", fname="result"):
    """
    Function for parsing input data and plot it using bokeh library.

    The data is supossed to contain the results of 3 different tests for
    a experiment. Hence, it is divided in three arrays where the results
    for each test is isolated. It is also found the average values and a
    polynomial curve that fits the given data.

    The plot is calculated and saved to the given file, and plotted if
    desired to the screen.

    Finally, it is also calculated the polynomial function that fits the
    x values (duty cycle), according to the y_mean (thrust), reversing
    the function direction. This way, a function for estimating the
    duty cycle can be obtained. This coeficients are returned.
    """
    bkplot.output_file("./results/{}.html".format(fname))
    plt = bkplot.figure(title=title, x_axis_label='duty cycle[%]',
                        y_axis_label='thrust[g]')
    # Parse the values to plot from the input data.
    x = input_data[0, :, 0]
    y0 = input_data[0, :, 1]
    y1 = input_data[1, :, 1]
    y2 = input_data[2, :, 1]
    y_mean = input_data[:, :, 1].mean(axis=0)
    # Get the polynomial fitting for the data average for the 5th and 2nd order.
    poly2_coefs = np.polyfit(x, y_mean, 2)
    poly5_coefs = np.polyfit(x, y_mean, 5)
    poly2_parser = np.poly1d(poly2_coefs)
    poly5_parser = np.poly1d(poly5_coefs)
    y_poly2 = poly2_parser(x)
    y_poly5 = poly5_parser(x)
    # Draw the plots on a bakeh figure
    plt.circle(x, y0, legend="test 1", fill_color="white", line_color="green",
               size=6)
    plt.circle(x, y1, legend="test 2", fill_color="orange", line_color="black",
               size=6)
    plt.circle(x, y2, legend="test 3", fill_color="magenta", line_color="gold",
               size=6)
    plt.line(x, y_mean, legend="average", line_color="red", line_width=2)
    plt.line(x, y_poly2, legend="fitted 2nd", line_color="blue", line_width=2)
    plt.line(x, y_poly5, legend="fitted 5th", line_color="green", line_width=2)
    plt.legend.location = "bottom_right"
    if show_result:
        bkplot.show(plt)
    # Obtain the polynomial for fitting the duty cycle according to the thrust.
    polyinv_coefs = np.polyfit(y_mean, x, 2)
    return polyinv_coefs


def main():
    filename = "./resources/motor_test.csv"
    data = np.loadtxt(filename, delimiter=";")
    # Re-arange the data in an array for each propeller, divided in a
    # sub-array for each test
    prop_8cw = data[0:63, :].reshape((3, 21, 2))
    prop_10cw = data[63:126, :].reshape((3, 21, 2))
    prop_ccw = data[126:189, :].reshape((3, 21, 2))
    # Plot the values
    coefs_8cw = plot_data(prop_8cw, title="8 inch CW propeller", fname="cw_8inch")
    coefs_10cw = plot_data(prop_10cw, title="10 inch CW propeller", fname="cw_10inch")
    coefs_ccw = plot_data(prop_ccw, title="CCW propeller", fname="ccw")
    coeficients = np.vstack((coefs_8cw, coefs_10cw, coefs_ccw))
    file_header = "Coeficient A\t\tCoeficient B\t\tCoeficient C"
    np.savetxt("./results/coeficients.txt", coeficients, fmt='%.6e',
               delimiter="\t\t", header=file_header)
    return


if __name__ == "__main__":
    main()
