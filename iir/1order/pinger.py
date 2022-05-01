import time

from scapy.layers.inet import ICMP, IP
from scapy.sendrecv import sr1, sr

def ping(ip):
    packet = IP(dst=ip) / ICMP()
    a = sr1(packet)
    timestamp = a.time - packet.sent_time

    return timestamp

if __name__ == '__main__':
    count = 500
    delays = []
    for i in range(count):
        print(f'Ping #{i}')
        delays.append(ping('10.0.1.1'))

    max_delay = max(delays)
    avg_delay = sum(delays)/len(delays)
    print(f'Average Delay: {avg_delay}')
    print(f'Max Delay: {max_delay}')