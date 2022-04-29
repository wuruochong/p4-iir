#!/usr/bin/env python3

import re

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
                    SignedIntField("input", 0),
                    SignedIntField("result", 0)]

bind_layers(Ether, P4calc, type=0x1234)

def main():

    s = ''
    iface = 'eth0'

    b0 = float(input('Input b_0 (1>b_0>0): '))
    b0 = b0 * 10
    b0 = int(b0)
    file_name = input('Input file name containing inputs: ')
    with open(file_name, 'r') as f:
        lines = f.readlines()
        inputs = [int(i) for i in lines]

    outputs = []

    for num in inputs:
        try:
            pkt = Ether(dst='00:04:00:00:00:00', type=0x1234) / P4calc(b0=b0,
                                              input=num*10)
            pkt = pkt/' '

            # pkt.show()
            resp = srp1(pkt, iface=iface, timeout=1, verbose=False)
            if resp:
                p4calc=resp[P4calc]
                if p4calc:
                    # print(p4calc.result)
                    outputs.append(int(p4calc.result)/10)
                else:
                    print("cannot find P4calc header in the packet")
            else:
                print("Didn't receive response")
        except Exception as error:
            print(error)

    print(outputs)


if __name__ == '__main__':
    main()
