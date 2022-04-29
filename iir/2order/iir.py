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

    b0 = int(input('Input b_0: '))
    b1 = int(input('Input b_1: '))
    b2 = int(input('Input b_2: '))
    a1 = int(input('Input a_1: '))
    a2 = int(input('Input a_2: '))

    while True:
        s = input('> ')
        if s == "quit":
            break
        # print(s)
        try:
            pkt = Ether(dst='00:04:00:00:00:00', type=0x1234) / P4calc(b0=b0,
                                              b1=b1,
                                              b2=b2,
                                              a1=a1,
                                              a2=a2,
                                              input=int(s))
            pkt = pkt/' '

            pkt.show()
            resp = srp1(pkt, iface=iface, timeout=1, verbose=False)
            if resp:
                p4calc=resp[P4calc]
                if p4calc:
                    print(p4calc.result)
                else:
                    print("cannot find P4calc header in the packet")
            else:
                print("Didn't receive response")
        except Exception as error:
            print(error)


if __name__ == '__main__':
    main()
