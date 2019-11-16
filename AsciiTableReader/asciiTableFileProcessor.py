import sys
import os
import matplotlib.pyplot as plt
import matplotlib.patches as m_patches
import numpy as np
import json


# function to return an array for a given column in ASCII file
def get_values(file_path, start_line, end_line, value_column):
    # setting type
    valueFromFile = []
    # check if file exists
    if not os.path.isfile(file_path):
        print("File path {} does not exist. Exiting...".format(file_path))
        sys.exit()
    # open file and read line by line with start and end line, where splitting shall happen
    try:
        with open(file_path) as fp:
            dataAscii = fp.readlines()
            for line in dataAscii[start_line:end_line]:
                lineSplit = line.split()
                valueFromFile.append(lineSplit[value_column])
    except IndexError:
        print('Indexes are incorrect: ', start_line, end_line, value_column)
        sys.exit()
    except IOError:
        print('Can´t open file: ', file_path)
        sys.exit()
    except Exception as e1:
        print('Unknown bug: ', e1)
        sys.exit()

    valueFromFile = list(np.float_(valueFromFile))
    # turn string array into float array
    return valueFromFile


# plotting curves
def plotting_curve(x1, y1, label1, x2, y2, label2, plot_title):
    plt.plot(x1, y1, 'b')
    plt.plot(x2, y2, 'r')
    plt.title(plot_title)
    plt.xlabel('x-Axis')
    plt.ylabel('y-Axis')
    patch1 = m_patches.Patch(color='blue', label=label1)
    patch2 = m_patches.Patch(color='red', label=label2)
    plt.legend(handles=[patch1, patch2])
    plt.savefig('Output/' + plot_title + '.png')
    plt.close()


# plotting bars
def plotting_bar(data1, objects, plot_title):
    objects = np.round(objects, 1)
    y_pos = np.arange(len(objects))
    plt.bar(y_pos, data1, align='center', alpha=0.5)
    plt.title(plot_title)
    plt.xticks(y_pos, objects, rotation=90, fontsize=8)
    plt.xlabel('x-Axis')
    plt.ylabel(' difference in [%]')
    plt.savefig('Output/' + plot_title + '_BarPlot.png')
    plt.close()


# calculating percentage differences for two given arrays, array2 is the reference array
def calculate_percentage(array1, array2):
    # turn into numpy array
    array1NpArray = np.array(array1)
    array2NpArray = np.array(array2)

    # calculate percentage, whereas array2 is the reference
    percentageDifferenceNpArray = np.multiply(np.divide(np.subtract(array1NpArray, array2NpArray), array2NpArray), 100)
    return percentageDifferenceNpArray


if __name__ == '__main__':
    # noinspection PyTypeChecker
    # opening input file

    try:
        with open('Input/Input.json', 'r') as json_file:
            data = json.load(json_file)
    except IOError:
        print('Can´t open file: ', json_file)
        sys.exit()
    except json.JSONDecodeError:
        print("JSON input file is corrupt: ", json_file)
    except Exception as e:
        print('Unknown bug: ', e)
        sys.exit()
    try:
        for x in range(len(data['asciiFiles'])):
            # Set1 post processing
            meanXValueSet1 = get_values(data['asciiFiles']['fileSet' + str(x)][0], data['startLine'], data['endLine'],
                                        0)
            meanYValueSet1 = get_values(data['asciiFiles']['fileSet' + str(x)][0], data['startLine'], data['endLine'],
                                        data['valueColumn'])

            # Set2 post processing
            meanXValueSet2 = get_values(data['asciiFiles']['fileSet' + str(x)][1], data['startLine'], data['endLine'],
                                        0)
            meanYValueSet2 = get_values(data['asciiFiles']['fileSet' + str(x)][1], data['startLine'], data['endLine'],
                                        data['valueColumn'])

            # Getting percentage difference between SR2 and SR3
            percentageDifferenceSet1Set2 = calculate_percentage(meanYValueSet1, meanYValueSet2)

            # plotting power curves
            plotting_curve(meanXValueSet1, meanYValueSet1, 'Set1', meanXValueSet2, meanYValueSet2,
                           'Set2', data['asciiFiles']['fileSet' + str(x)][2])

            # plotting differences in percentage in bar plot
            plotting_bar(percentageDifferenceSet1Set2, meanXValueSet1, data['asciiFiles']['fileSet' + str(x)][2])

    except Exception as e:
        print('Unknown bug: ', e)
        sys.exit()