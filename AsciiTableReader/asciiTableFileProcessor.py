import sys
import os
import matplotlib.pyplot as plt
import matplotlib.patches as m_patches
import numpy as np
import json
import getopt


# function to get input arguments
def get_inputs(argv):
    in_file = None
    try:
        opts, args = getopt.getopt(argv, "hi:", ["ifile="])
    except getopt.GetoptError:
        print('Error in defining input arguments --> asciiTableFileProcessor.py -i <inputfile> ')
        sys.exit(-1)
    for opt, arg in opts:
        if opt == '-h':
            print('asciiTableFileProcessor.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            in_file = arg
    return in_file


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


# class to read an array for a given column in ASCII file
class TableValues:
    def __init__(self, file_path, start_line, end_line, value_column, plot_title):
        self.file_path = file_path
        self.start_line = start_line
        self.end_line = end_line
        self.value_column = value_column
        self.plot_title = plot_title

    # get values from ascii table
    def get_values(self):
        # setting type
        valueFromFile = []
        # check if file exists
        if not os.path.isfile(self.file_path):
            print("File path {} does not exist. Exiting...".format(self.file_path))
            sys.exit()
        # open file and read line by line with start and end line, where splitting shall happen
        try:
            with open(self.file_path) as fp:
                dataAscii = fp.readlines()
                for line in dataAscii[self.start_line:self.end_line]:
                    lineSplit = line.split()
                    valueFromFile.append(lineSplit[self.value_column])
        except IndexError:
            print('Indexes are incorrect: ', self.start_line, self.end_line, self.value_column)
            sys.exit(-1)
        except IOError:
            print('Can´t open file: ', self.file_path)
            sys.exit(-1)
        except Exception as e1:
            print('Unknown bug: ', e1)
            sys.exit(-1)

        valueFromFile = list(np.float_(valueFromFile))
        # turn string array into float array
        return valueFromFile


# main call
try:
    input_file = get_inputs(sys.argv[1:])
except Exception as e:
    print('Unknown bug: ', e)
    sys.exit(-1)
# opening input file
try:
    with open(input_file, 'r') as json_file:
        data = json.load(json_file)
except IOError:
    print('Can´t open file: ', json_file)
    sys.exit(-1)
except json.JSONDecodeError:
    print("JSON input file is corrupt: ", json_file)
except Exception as e:
    print('Unknown bug: ', e)
    sys.exit(-1)
try:
    for x in range(len(data['asciiFiles'])):
        # Set1 post processing
        setXAxis = TableValues(data['asciiFiles']['fileSet' + str(x)][0], data['startLine'], data['endLine'], 0, None)
        set1 = TableValues(data['asciiFiles']['fileSet' + str(x)][0], data['startLine'], data['endLine'],
                           data['valueColumn'], data['asciiFiles']['fileSet' + str(x)][2])
        set2 = TableValues(data['asciiFiles']['fileSet' + str(x)][1], data['startLine'], data['endLine'],
                           data['valueColumn'], data['asciiFiles']['fileSet' + str(x)][2])

        # Getting percentage difference between SR2 and SR3
        percentageDifferenceSet1Set2 = calculate_percentage(set1.get_values(), set2.get_values())

        # plotting power curves
        plotting_curve(setXAxis.get_values(), set1.get_values(), 'Set1', setXAxis.get_values(), set2.get_values(),
                       'Set2', set2.plot_title)

        # plotting differences in percentage in bar plot
        plotting_bar(percentageDifferenceSet1Set2, setXAxis.get_values(), set2.plot_title)

except Exception as e:
    print('Unknown bug: ', e)
    sys.exit(-1)
