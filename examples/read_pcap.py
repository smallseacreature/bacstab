"""Usage: python examples/read_pcap.py capture.pcap"""
import argparse
from scapy.all import PcapReader, UDP
from bacstab import process_udp_payload, print_dictionary


def main():
    parser = argparse.ArgumentParser(description="Parse BACnet UDP payloads from a capture")
    parser.add_argument("capture")
    args = parser.parse_args()
    with PcapReader(args.capture) as packets:
        for number, packet in enumerate(packets, 1):
            if UDP not in packet:
                continue
            result = process_udp_payload(packet[UDP])
            if result is not None:
                print(f"Packet {number}")
                print_dictionary(result)


if __name__ == "__main__":
    main()
