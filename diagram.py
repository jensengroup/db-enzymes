
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.lines as lines
from itertools import izip, count

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


def add_energy_path(ax, energies, color=None, label=None, epsilon=0.1):

    xs = np.array([0 - epsilon, 0 + epsilon])
    ys = np.array([0, 0])

    # plot the first energy level and set color
    p = plt.plot(xs, ys+energies[0], color=color, label=label)
    if not color: color = p[0].get_color()

    for i, energy in enumerate(energies[1:]):
        plt.plot(xs+i+1, ys+energy, color=color)

    for i, energy_1, energy_2 in izip(count(), energies[:-1], energies[1:]):
        add_line(ax, i+epsilon, i+1-epsilon, energy_1, energy_2, color=color)

    return


if __name__ == "__main__":

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


