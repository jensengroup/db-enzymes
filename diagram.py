
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.lines as lines
from cycler import cycler

def look_nice(ax, xaxis, xticks):

    # ax.axes.get_xaxis().set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    ax.yaxis.grid(True, zorder=0)

    ax.set_xticks(xaxis)
    ax.set_xticklabels(xticks)

    ax.margins(0.1)

    return


def add_line(ax, x1, x2, y1, y2, color='g', ls='--'):

    l = lines.Line2D([x1, x2], [y1, y2], ls=ls, color=color)
    ax.add_line(l)

    return


def add_energy_path(ax, energies, color):



    return

def next_color():

    color_cycle = plt.rcParams['axes.prop_cycle']
    # colors = color_cycle.by_key()['color']

    for color in color_cycle:
        yield color['color']


    # for color in colors:
    #     yield color
    #
    # yield "#111111"



if __name__ == "__main__":

    fig = plt.figure()
    ax = fig.add_subplot(111)


    color =  next(next_color())

    print color

    path = [0, 20, -10]
    names = ["R", "TS", "P"]
    xaxis = [1, 2, 3]

    epsilon = 0.1

    xs = np.array([1-epsilon, 1+epsilon])
    ys = np.array([0, 0])


    ts = 21.67
    p = -8.4343

    plt.plot(xs, ys, "-", color=color, label="path 2")
    plt.plot(xs+1, ys+ts, "-", color=color)
    plt.plot(xs+2, ys+p, "-", color=color)
    add_line(ax, 1+epsilon, 2-epsilon, 0, ts, color=color)
    add_line(ax, 2+epsilon, 3-epsilon, ts, p, color=color)

    ts = 18.67
    p = -8.4343

    color = next(next_color())
    color = next(next_color())
    color = next(next_color())

    print color
    color='r'

    plt.plot(xs, ys, "-", color=color, label="path 2")
    plt.plot(xs+1, ys+ts, "-", color=color)
    plt.plot(xs+2, ys+p, "-", color=color)
    add_line(ax, 1+epsilon, 2-epsilon, 0, ts, color=color)
    add_line(ax, 2+epsilon, 3-epsilon, ts, p, color=color)

    look_nice(ax, xaxis, names)


    if True:
        leg = ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        leg.get_frame().set_linewidth(0.0)
        leg.get_frame().set_facecolor('none')

    filename = "testing"

    plt.savefig(filename+'.png', bbox_inches='tight')


