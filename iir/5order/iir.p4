/* -*- P4_16 -*- */

#include <core.p4>
#include <v1model.p4>

/*
 * Define the headers the program will recognize
 */

/*
 * Standard Ethernet header
 */
header ethernet_t {
    bit<48> dstAddr;
    bit<48> srcAddr;
    bit<16> etherType;
}

/*
 * This is a custom protocol header.
 */
const bit<16> P4CALC_ETYPE = 0x1234;
const bit<8>  P4CALC_P     = 0x50;   // 'P'
const bit<8>  P4CALC_4     = 0x34;   // '4'
const bit<8>  P4CALC_VER   = 0x01;   // v0.1

header p4calc_t {
    bit<8>  p;
    bit<8>  four;
    bit<8>  ver;
    int<32> b0;
    int<32> b1;
    int<32> b2;
    int<32> b3;
    int<32> b4;
    int<32> b5;
    int<32> a1;
    int<32> a2;
    int<32> a3;
    int<32> a4;
    int<32> a5;
    int<32> input;
    int<32> res;
}

/*
 * All headers, used in the program needs to be assembled into a single struct.
 * We only need to declare the type, but there is no need to instantiate it,
 * because it is done "by the architecture", i.e. outside of P4 functions
 */
struct headers {
    ethernet_t   ethernet;
    p4calc_t     p4calc;
}

/*
 * All metadata, globally used in the program, also  needs to be assembled
 * into a single struct. As in the case of the headers, we only need to
 * declare the type, but there is no need to instantiate it,
 * because it is done "by the architecture", i.e. outside of P4 functions
 */

struct metadata {
    /* In our case it is empty */
}

/*************************************************************************
 ***********************  P A R S E R  ***********************************
 *************************************************************************/
parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {
    state start {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            P4CALC_ETYPE : check_p4iir;
            default      : accept;
        }
    }

    state check_p4iir {

        transition select(packet.lookahead<p4calc_t>().p,
        packet.lookahead<p4calc_t>().four,
        packet.lookahead<p4calc_t>().ver) {
            (P4CALC_P, P4CALC_4, P4CALC_VER) : parse_p4iir;
            default                          : accept;
        }

    }

    state parse_p4iir {
        packet.extract(hdr.p4calc);
        transition accept;
    }
}

/*************************************************************************
 ************   C H E C K S U M    V E R I F I C A T I O N   *************
 *************************************************************************/
control MyVerifyChecksum(inout headers hdr,
                         inout metadata meta) {
    apply { }
}

/*************************************************************************
 **************  I N G R E S S   P R O C E S S I N G   *******************
 *************************************************************************/
control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {
    register<int<32>>(1) prev_input1;
    register<int<32>>(1) prev_input2;
    register<int<32>>(1) prev_input3;
    register<int<32>>(1) prev_input4;
    register<int<32>>(1) prev_input5;
    register<int<32>>(1) prev_output1;
    register<int<32>>(1) prev_output2;
    register<int<32>>(1) prev_output3;
    register<int<32>>(1) prev_output4;
    register<int<32>>(1) prev_output5;
    int<32> prev_input1_val;
    int<32> prev_input2_val;
    int<32> prev_input3_val;
    int<32> prev_input4_val;
    int<32> prev_input5_val;
    int<32> prev_output1_val;
    int<32> prev_output2_val;
    int<32> prev_output3_val;
    int<32> prev_output4_val;
    int<32> prev_output5_val;

    action send_back(int<32> result) {
        bit<48> tmp;
         // Put the result back in
         hdr.p4calc.res = result;

         // Swap the MAC addresses
         tmp = hdr.ethernet.dstAddr;
         hdr.ethernet.dstAddr = hdr.ethernet.srcAddr;
         hdr.ethernet.srcAddr = tmp;

         // Send the packet back to the port it came from
         standard_metadata.egress_spec = standard_metadata.ingress_port;
    }


    action filter() {
        int<32> inputTemp;  // Variable to store accumulation of prev inputs
        int<32> outputTemp; // Variable to store accumulation of prev outputs
        int<32> output;

        // Read the previous values
        prev_input1.read(prev_input1_val, 0);
        prev_input2.read(prev_input2_val, 0);
        prev_input3.read(prev_input3_val, 0);
        prev_input4.read(prev_input4_val, 0);
        prev_input5.read(prev_input5_val, 0);
        prev_output1.read(prev_output1_val, 0);
        prev_output2.read(prev_output2_val, 0);
        prev_output3.read(prev_output3_val, 0);
        prev_output4.read(prev_output4_val, 0);
        prev_output5.read(prev_output5_val, 0);

        inputTemp = ((hdr.p4calc.b1 * prev_input1_val)>>8) +
                    ((hdr.p4calc.b2 * prev_input2_val)>>8) +
                    ((hdr.p4calc.b3 * prev_input3_val)>>8) +
                    ((hdr.p4calc.b4 * prev_input4_val)>>8) +
                    ((hdr.p4calc.b5 * prev_input5_val)>>8);
        outputTemp = ((hdr.p4calc.a1 * prev_output1_val)>>8) +
                     ((hdr.p4calc.a2 * prev_output2_val)>>8) +
                     ((hdr.p4calc.a3 * prev_output3_val)>>8) +
                     ((hdr.p4calc.a4 * prev_output4_val)>>8) +
                     ((hdr.p4calc.a5 * prev_output5_val)>>8);
        output = ((hdr.p4calc.b0 * hdr.p4calc.input)>>8) + inputTemp - outputTemp;

        // Store new previous values
        prev_output5.write(0, prev_output4_val);
        prev_output4.write(0, prev_output3_val);
        prev_output3.write(0, prev_output2_val);
        prev_output2.write(0, prev_output1_val);
        prev_output1.write(0, output);
        prev_input5.write(0, prev_input4_val);
        prev_input4.write(0, prev_input3_val);
        prev_input3.write(0, prev_input2_val);
        prev_input2.write(0, prev_input1_val);
        prev_input1.write(0, hdr.p4calc.input);

        send_back(output);
    }

    action operation_drop() {
        mark_to_drop(standard_metadata);
    }

    apply {
        if (hdr.p4calc.isValid()) {
            filter();
        } else {
            operation_drop();
        }
    }
}

/*************************************************************************
 ****************  E G R E S S   P R O C E S S I N G   *******************
 *************************************************************************/
control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {
    apply { }
}

/*************************************************************************
 *************   C H E C K S U M    C O M P U T A T I O N   **************
 *************************************************************************/

control MyComputeChecksum(inout headers hdr, inout metadata meta) {
    apply { }
}

/*************************************************************************
 ***********************  D E P A R S E R  *******************************
 *************************************************************************/
control MyDeparser(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.p4calc);
    }
}

/*************************************************************************
 ***********************  S W I T C H **********************************
 *************************************************************************/

V1Switch(
MyParser(),
MyVerifyChecksum(),
MyIngress(),
MyEgress(),
MyComputeChecksum(),
MyDeparser()
) main;
