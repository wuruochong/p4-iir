#!/usr/bin/env python3

import re
import csv

from scapy.all import (
    Ether,
    SignedIntField,
    Packet,
    StrFixedLenField,
    XByteField,
    bind_layers,
    srp1
)


class P4calc(Packet):
    name = "P4iir"
    fields_desc = [ StrFixedLenField("P", "P", length=1),
                    StrFixedLenField("Four", "4", length=1),
                    XByteField("version", 0x01),
                    SignedIntField("b0", 1),
                    SignedIntField("b1", 1),
                    SignedIntField("b2", 1),
                    SignedIntField("a1", 1),
                    SignedIntField("a2", 1),
                    SignedIntField("input", 0),
                    SignedIntField("result", 0)]

bind_layers(Ether, P4calc, type=0x1234)


def main():

    s = ''
    iface = 'eth0'

    b0 = int(float(input('Input b_0: ')) * (1 << 8))
    b1 = int(float(input('Input b_1: ')) * (1 << 8))
    b2 = int(float(input('Input b_2: ')) * (1 << 8))
    a1 = int(float(input('Input a_1: ')) * (1 << 8))
    a2 = int(float(input('Input a_2: ')) * (1 << 8))
    file_name = input('Input csv file name containing inputs: ')
    output_name = input('Input csv file name to store outputs: ')
    with open(file_name, 'r') as f:
        data = f.read()
        data = data.split(',')
        inputs = [int(i) for i in data]

    outputs = []
    progress = 0

    for num in inputs:
        try:
            pkt = Ether(dst='00:04:00:00:00:00', type=0x1234) / P4calc(b0=b0,
                                              b1=b1,
                                              b2=b2,
                                              a1=a1,
                                              a2=a2,
                                              input=num<<8)
            pkt = pkt/' '

            # pkt.show()
            resp = srp1(pkt, iface=iface, timeout=1, verbose=False)
            if resp:
                p4calc=resp[P4calc]
                if p4calc:
                    # print(p4calc.result)
                    outputs.append(int(p4calc.result) / float(1<<8))
                    print(progress)
                    progress += 1
                else:
                    print("cannot find P4calc header in the packet")
            else:
                print("Didn't receive response")
        except Exception as error:
            print(error)

    # print(outputs)
    with open(output_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(outputs)


if __name__ == '__main__':
    main()
