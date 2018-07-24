
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.lines as lines
from itertools import izip, count

def look_nice(ax, xticks):

    # ax.axes.get_xaxis().set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    ax.yaxis.grid(True, zorder=0)

    xaxis = list(range(len(xticks)))
    ax.set_xticks(xaxis)
    ax.set_xticklabels(xticks)

    ax.margins(0.1)

    ax.xaxis.set_ticks_position('none') 
    ax.yaxis.set_ticks_position('none') 

    return


def add_line(ax, x1, x2, y1, y2, color='g', ls='-'):

    l = lines.Line2D([x1, x2], [y1, y2], ls=ls, color=color, linewidth=1)
    ax.add_line(l)

    return


def add_energy_path(ax, energies, color=None, label=None, epsilon=0.1):

    xs = np.array([0 - epsilon, 0 + epsilon])
    ys = np.array([0, 0])

    # plot the first energy level and set color
    p = plt.plot(xs, ys+energies[0], color=color, label=label, linewidth=2)
    if not color: color = p[0].get_color()

    for i, energy in enumerate(energies[1:]):
        plt.plot(xs+i+1, ys+energy, color=color, linewidth=2)

    for i, energy_1, energy_2 in izip(count(), energies[:-1], energies[1:]):
        add_line(ax, i+epsilon, i+1-epsilon, energy_1, energy_2, color=color)

    return


def test():

    fig = plt.figure()
    ax = fig.add_subplot(111)

    names = ["R", "TS", "P"]
    xaxis = list(range(len(names)))

    path = [0, 23.2, -8.1]
    add_energy_path(ax, path, label="path 1")

    path = [0, 10.2, -5.4]
    add_energy_path(ax, path, label="path 2")

    look_nice(ax, xaxis, names)

    if True:
        leg = ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        leg.get_frame().set_linewidth(0.0)
        leg.get_frame().set_facecolor('none')

    filename = "testing"

    plt.savefig(filename+'.png', bbox_inches='tight')

    return


def read_csv(filename):

    with open(filename, 'r') as f:

        header = next(f)
        header = header.strip()
        header = header.split(",")
        path = header[1:]

        path_names = []
        path_energies = []

        for line in f:
            line = line.strip()
            line = line.split(",")
            name = line[0]
            values = line[1:]
            values = [float(val) for val in values]
            path_names.append(name)
            path_energies.append(values)

    return path, path_names, path_energies

if __name__ == "__main__":

    import sys
    args = sys.argv[1:]
    filename = args[0]

    path, path_names, path_energies = read_csv(filename)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    for name, energies in zip(path_names, path_energies):
        add_energy_path(ax, energies, label=name)

    look_nice(ax, path)

    if True:
        # leg = ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        leg = ax.legend(loc="best", borderaxespad=0., framealpha=1.0, fancybox=False, borderpad=1)
        leg.get_frame().set_linewidth(0.0)
        leg.get_frame().set_facecolor('#ffffff')

    filename = filename.replace(".csv", "")

    plt.savefig(filename+'.png', bbox_inches='tight')


