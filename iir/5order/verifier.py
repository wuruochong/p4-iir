import sys
import csv


def fifth_order_iir(input: float, b0: float, b1: float, b2: float, b3: float, b4: float, b5: float,
                     a1: float, a2: float, a3: float, a4: float, a5: float,
                     prev_input1: float, prev_input2: float, prev_input3: float, prev_input4: float, prev_input5: float,
                     prev_output1: float, prev_output2: float, prev_output3: float, prev_output4: float, prev_output5: float)-> float:
    input_temp = input*b0 + prev_input1*b1 + prev_input2*b2 + prev_input3*b3 + prev_input4*b4 + prev_input5*b5
    output_temp = prev_output1*a1 + prev_output2*a2 + prev_output3*a3 + prev_output4*a4 + prev_output5*a5

    output = input_temp - output_temp
    return output


if __name__ == '__main__':
    # Check inputs
    num_args = len(sys.argv)
    if num_args < 14:
        print(
            "Usage: python verifier.py [input csv] [output csv] [b0] [b1] [b2] [b3] [b4] [b5] [a1] [a2] [a3] [a4] [a5]\n")
        exit()
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    b0 = float(sys.argv[3])
    b1 = float(sys.argv[4])
    b2 = float(sys.argv[5])
    b3 = float(sys.argv[6])
    b4 = float(sys.argv[7])
    b5 = float(sys.argv[8])
    a1 = float(sys.argv[9])
    a2 = float(sys.argv[10])
    a3 = float(sys.argv[11])
    a4 = float(sys.argv[12])
    a5 = float(sys.argv[13])

    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        input_raw_data = list(reader)[0]
        input_data = [float(i) for i in input_raw_data]

    prev_input1 = 0
    prev_input2 = 0
    prev_input3 = 0
    prev_input4 = 0
    prev_input5 = 0
    prev_output1 = 0
    prev_output2 = 0
    prev_output3 = 0
    prev_output4 = 0
    prev_output5 = 0
    outputs = []

    for input in input_data:
        output = fifth_order_iir(input, b0, b1, b2, b3, b4, b5, a1, a2, a3, a4, a5, prev_input1, prev_input2, prev_input3, prev_input4, prev_input5, prev_output1, prev_output2, prev_output3, prev_output4, prev_output5)
        outputs.append(output)
        prev_input5 = prev_input4
        prev_input4 = prev_input3
        prev_input3 = prev_input2
        prev_input2 = prev_input1
        prev_input1 = input
        prev_output5 = prev_output4
        prev_output4 = prev_output3
        prev_output3 = prev_output2
        prev_output2 = prev_output1
        prev_output1 = output

    with open(output_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(outputs)

