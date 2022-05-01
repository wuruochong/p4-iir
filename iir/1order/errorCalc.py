import csv
import numpy as np
import sys


def main():
    num_args = len(sys.argv)
    if num_args < 3:
        print(
            "Usage: python errorCalc.py [reference csv] [output csv]\n")
        exit()
    reference_name = sys.argv[1]
    output_name = sys.argv[2]
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
    max_error = max(error)
    av_error = np.mean(error)
    print(f'Avg. Percent Error: {av_error * 100}%')
    print(f'Max Percent Error: {max_error * 100}%')
    # for i in difference:
    #     if i > 0:
    #         print(i)


if __name__ == '__main__':
    main()
