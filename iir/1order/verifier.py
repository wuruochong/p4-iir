import sys
import csv


def first_order_iir(input: float, b0: float, a1: float, prev_output1: float)-> float:
    output = b0*input + a1*prev_output1
    return output


if __name__ == '__main__':
    # Check inputs
    num_args = len(sys.argv)
    if num_args < 4:
        print(
            "Usage: python verifier.py [input csv] [output csv] [b0]\n")
        exit()
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    b0 = float(sys.argv[3])
    a1 = 1 - b0

    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        input_raw_data = list(reader)[0]
        input_data = [float(i) for i in input_raw_data]

    prev_output1 = 0
    outputs = []

    for input in input_data:
        output = first_order_iir(input, b0, a1, prev_output1)
        outputs.append(output)
        prev_output1 = output

    with open(output_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(outputs)

