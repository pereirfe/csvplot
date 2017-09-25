#!/usr/bin/python

import sys
import re
import json
import time
import math
import numpy
import os
import csv
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt

def alpha_to_int(col):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    n = 0
    for char in col:
        for i in range(len(alphabet)):
            if alphabet[i] == char:
                n = n*len(alphabet) + i
                break

    return n


def column_input(t_table, text, silence=False, x_index=-1, type_val='X'):
    if silence == False:
        x_index = alpha_to_int(raw_input(text+"\n"))
        type_val = raw_input("[I]nt, [F]loat or [S]tring?\n")

    if type_val in ['i', 'I']:
        for i, x in enumerate(t_table[x_index]):
            t_table[x_index][i] = int(x)
    elif type_val in ['f', 'F']:
        for i, x in enumerate(t_table[x_index]):
            t_table[x_index][i] = float(x)

    return x_index, type_val


def interactive_plotter(inputdata, outputplot, recipe, load_recipe=False):

    t_table = []

    with open(inputdata, 'r') as inv:
        csvin = csv.reader(inv)

        for _, line in enumerate(csvin):
            if _ == 0:
                for x in line:
                    t_table.append([])

            for i, x in enumerate(line):
                t_table[i].append(x)

    confidence_mult = 0
    title = 0
    x_axis = 0
    r_y_axis = []
    r_y_axis_err = []
    r_y_axis_type = []
    r_y_axis_err_type = []
    r_fmt = []

    if load_recipe == False:
        recipe['confidence_mult'] = float(raw_input("Set Confidence Interval Multiplier\n"))

        recipe['title'] = raw_input("Set Title\n")
        recipe['x_axis'], recipe['x_axis_type'] = column_input(t_table,
                                                               "Set X axis column")
        recipe['numplots'] = int(raw_input("How many Plots?\n"))

        for i in range(recipe['numplots']):
            y_axis, y_axis_type = column_input(t_table, "\t"+str(i+1)+") Set Y axis column\t")
            r_y_axis.append(y_axis)
            r_y_axis_type.append(y_axis_type)

            y_axis_err, y_axis_err_type = column_input(t_table,
                                                       "\t"+str(i+1)+") Set Y-error axis column\t")

            r_y_axis_err.append(y_axis_err)
            r_y_axis_err_type.append(y_axis_err_type)

            fmt = raw_input("\t"+str(i+1)+") Set Format: (Return to use default)\n\t")
            r_fmt.append(fmt)

            print ""

        recipe['y_axis'] = r_y_axis
        recipe['y_axis_type'] = r_y_axis_type
        recipe['y_axis_err'] = r_y_axis_err
        recipe['y_axis_err_type'] = r_y_axis_err_type
        recipe['fmt'] = r_fmt


    else:
        column_input(t_table, "", True, recipe['x_axis'], recipe['x_axis_type'])

        for i in range(recipe['numplots']):
            column_input(t_table, "", True,
                         recipe['y_axis'][i],
                         recipe['y_axis_type'][i])

            column_input(t_table, "", True,
                         recipe['y_axis_err'][i],
                         recipe['y_axis_err_type'][i])


    for i in range(recipe['numplots']):
        y_axis_err = int(recipe['y_axis_err'][i])
        confidence_mult = recipe['confidence_mult']

        for j, v in enumerate(t_table[y_axis_err]):
            t_table[y_axis_err][j] = confidence_mult*v



    plt.figure()
    plt.title(title)

    for i in range(recipe['numplots']):
        x_axis = recipe['x_axis']
        y_axis = recipe['y_axis'][i]
        y_axis_err = recipe['y_axis_err'][i]
        fmt = recipe['fmt'][i]

        print x_axis, y_axis, y_axis_err, fmt
        print t_table[y_axis]
        print t_table[y_axis_err]

        if fmt == '':
            plt.errorbar(t_table[x_axis], t_table[y_axis], yerr=t_table[y_axis_err])
        else:
            plt.errorbar(t_table[x_axis], t_table[y_axis], yerr=t_table[y_axis_err], fmt=fmt)

    plt.show()
    plt.savefig(outputplot)
    return recipe


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print "Usage:", sys.argv[0],
        print "inputdata.csv outputplot [-i|-o recipefile]"
        print "\t-i use a recipefile as input"
        print "\t-o run the script and save the recipefile"

    recipe = {}
    if sys.argv[3] == '-i':
        with open(sys.argv[4], 'r') as recipe_fp:
            recipe = json.load(recipe_fp)
        interactive_plotter(sys.argv[1], sys.argv[2], recipe, True)

    elif sys.argv[3] == '-o':
        interactive_plotter(sys.argv[1], sys.argv[2], recipe, False)
        with open(sys.argv[4], 'w') as recipe_fp:
            json.dump(recipe, recipe_fp)

# TODO: Include stylesheet
