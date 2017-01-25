# NetRank

from bokeh.plotting import *
import datetime as dt

def visualize_results(OUTPUT_FILE, DATES, ACCURACIES, SPEARMANS, \
                      COMPUTATION_TIMES):
    '''
    Renders a time-series plot of how our computed rankings perform with 
    respect to retrodictive accuracy throughout the course of a given season.
    '''
    output_file(OUTPUT_FILE)

    a = figure(x_axis_type = "datetime", 
               title = "Retrodictive Accuracy of Computed Power Rankings")
    a.yaxis.axis_label     = "Retrodictive Accuracy (%)"
    a.xaxis.axis_label     = "Date"
    a.line(DATES, ACCURACIES, line_width = 5, color = "red")

    s = figure(x_axis_type = "datetime", \
               title = "Spearman Coefficient of Computed Power Rankings")
    s.yaxis.axis_label     = "Correlation Coefficient"
    s.xaxis.axis_label     = "Date"
    s.line(DATES, SPEARMANS, line_width = 5, color = "blue")

    c = figure(x_axis_type = "datetime", \
               title = "Time to Compute Power Rankings")
    c.yaxis.axis_label     = "Elapsed Computation Time (sec)"
    c.xaxis.axis_label     = "Date"
    c.line(DATES, COMPUTATION_TIMES, line_width = 5, color = "green")

    show(vplot(a, s, c))