import sys
import csv


def second_order_iir(input: float, b0: float, b1: float, b2: float, a1: float, a2: float, prev_input1: float, prev_input2: float, prev_output1: float, prev_output2: float)-> float:
    input_temp = input*b0 + prev_input1*b1 + prev_input2*b2
    output_temp = prev_output1*a1 + prev_output2*a2

    output = input_temp - output_temp
    return output


if __name__ == '__main__':
    # Check inputs
    num_args = len(sys.argv)
    if num_args < 8:
        print(
            "Usage: python verifier.py [input csv] [output csv] [b0] [b1] [b2] [a1] [a2]\n")
        exit()
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    b0 = float(sys.argv[3])
    b1 = float(sys.argv[4])
    b2 = float(sys.argv[5])
    a1 = float(sys.argv[6])
    a2 = float(sys.argv[7])

    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        input_raw_data = list(reader)[0]
        input_data = [float(i) for i in input_raw_data]

    prev_input1 = 0
    prev_input2 = 0
    prev_output1 = 0
    prev_output2 = 0
    outputs = []

    for input in input_data:
        output = second_order_iir(input, b0, b1, b2, a1, a2, prev_input1, prev_input2, prev_output1, prev_output2)
        outputs.append(output)
        prev_input2 = prev_input1
        prev_input1 = input
        prev_output2 = prev_output1
        prev_output1 = output

    with open(output_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(outputs)

