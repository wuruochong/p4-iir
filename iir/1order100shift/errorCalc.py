import csv
import numpy as np


def main():

    reference_name = input('Input csv file name containing reference: ')
    output_name = input('Input csv file name containing outputs: ')
    with open(reference_name, 'r') as f:
        reader = csv.reader(f)
        reference_raw_data = list(reader)[0]
        reference_data = [float(i) for i in reference_raw_data]
        reference_data = np.array(reference_data)

    with open(output_name, 'r') as f:
        reader = csv.reader(f)
        output_raw_data = list(reader)[0]
        output_data = [float(i) for i in output_raw_data]
        output_data = np.array(output_data)

    difference = np.abs(output_data - reference_data)
    error = difference / output_data
    av_error = np.mean(error)
    print(av_error)
    # for i in difference:
    #     if i > 0:
    #         print(i)


if __name__ == '__main__':
    main()