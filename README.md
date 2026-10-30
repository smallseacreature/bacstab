# BACstab

A modular Python toolkit for parsing BACnet packets and building small, custom BACnet tools.

BACstab handles the protocol parsing so your scripts can focus on filtering, inspecting, and analyzing traffic. Built to work with Scapy, it returns parsed data as nested Python dictionaries.

## Installation

Requires **Python 3.10 or newer**. Scapy is installed automatically as a dependency.

Clone the repository and install:

```bash
git clone https://github.com/smallseacreature/bacstab.git
cd bacstab
python -m pip install .
```

For development, use an editable installation:

```bash
python -m pip install -e .
```

Changes to the source files will be available without reinstalling. Keep the repository in a stable location when using editable mode.

## Quick Start

### Parse BACnet bytes

Pass a complete BVLC message to `process_bvlc()`:

```python
from bacstab import process_bvlc, print_dictionary

# BVLC-Result: successful completion
payload = bytes.fromhex("81 00 00 06 00 00")

result = process_bvlc(payload)

if result is not None:
    print_dictionary(result)
```

### Read a packet capture

```python
from scapy.all import PcapReader, UDP
from bacstab import process_udp_payload

with PcapReader("capture.pcap") as packets:
    for packet in packets:
        if UDP not in packet:
            continue

        result = process_udp_payload(packet[UDP])

        if result is None:
            continue

        print(result["function_name"])
```

`PcapReader` processes the capture one packet at a time without loading the entire file into memory.

### Inspect the full parsed record

```python
from bacstab import print_dictionary

print_dictionary(result)
```

For a string you can save or display elsewhere:

```python
from bacstab import format_dictionary

text = format_dictionary(result)
print(text)
```

### Run the included example

```bash
python examples/read_pcap.py capture.pcap
```

## Modules

| Module | Purpose |
|---|---|
| `bacstab.bvlc` | Parse BVLC headers and supported function bodies |
| `bacstab.npdu` | Parse NPDU headers and routing information |
| `bacstab.apdu` | Parse APDU headers and service metadata |
| `bacstab.constants` | Protocol constants and lookup tables |
| `bacstab.layers` | Extract Scapy layer fields and parse UDP payloads |
| `bacstab.capture` | Read capture metadata and calculate file hashes |
| `bacstab.utils` | Format and print nested parser results |

Individual protocol parsers are also available directly:

```python
from bacstab import process_bvlc, process_npdu, process_apdu
```

Each expects bytes beginning at its corresponding protocol header.

## Working With Results

The parsers return dictionaries containing decoded fields, nested protocol records, and retained raw bytes.

For messages carrying an application PDU, you can access the nested layers:

```python
npdu = result.get("npdu")

if npdu is not None:
    apdu = npdu.get("apdu")

    if apdu is not None:
        print(apdu.get("service_name"))
```

Not every BACnet message contains an NPDU or APDU.

Malformed or unsupported input may return `None` or a partial record. Check fields such as:

- `length_valid`
- `body_parse_valid`
- `body_parse_error`
- `unsupported_reason`
- `npdu_parse_valid`
- `apdu_parse_valid`

These fields belong to their respective layer records. A returned dictionary—or a valid outer header—does not guarantee that all nested content was decoded successfully.

## Current Scope

BACstab currently focuses on decoding BACnet/IP traffic.

It includes:

- IPv4 BVLC header and supported function-body parsing
- Broadcast Distribution Table and Foreign Device Table entry parsing
- NPDU routing-field extraction
- APDU header and service identification
- Scapy UDP payload integration
- Capture metadata and readable result formatting

Current limitations:

- BACnet/IPv6 function-body decoding is not implemented.
- Complete security-wrapper decoding is not implemented.
- Network-message bodies and most application-service data remain raw.
- Segmented APDUs are not reassembled.
- Packet construction, request sending, and response tracking are not implemented.

## Validation

The initial package was tested with Python 3.12 and Scapy 2.8.0.

Checks covered basic BVLC parsing, truncated input, a synthetic Who-Is message, and non-BACnet UDP data. A supplied capture containing 24,718 packets produced 13,969 BACnet records without parser exceptions.

These checks do not establish complete protocol conformance. The test environment required disabling Scapy interface discovery for offline testing; live capture was not tested.