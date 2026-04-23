# Interference-Aware Channel Switching in IEEE 802.15.4 (NS-3)

**Course:** Wireless Networks and Applications
**Roll No:** 220002029

---

## Overview

This project implements an **interference-aware channel switching algorithm** for IEEE 802.15.4 (Zigbee) networks using **NS-3**.

A Zigbee coordinator continuously monitors **Energy Detection (ED)** levels. When interference from IEEE 802.11 (Wi-Fi) is detected, the network **autonomously switches to a non-overlapping channel**, restoring throughput.

---

## Topology Parameters (derived from Roll No. 220002029)

| Parameter | Calculation | Value |
|-----------|-------------|-------|
| IEEE 802.15.4 devices | sum of ALL digits: 2+2+0+0+0+2+0+2+9 | **17** (1 coordinator + 16 end-devices) |
| IEEE 802.11 devices | sum of LAST FOUR digits: 2+0+2+9 | **13** (1 AP + 12 STAs) |

---

## Channel Overlap (2.4 GHz ISM Band)

| IEEE 802.15.4 Channel | Centre Freq | Overlaps IEEE 802.11 |
|----------------------|-------------|----------------------|
| 11 (initial)         | 2405 MHz    | WiFi Channel 1 (2412 MHz) — interference source |
| 15 – 18              | 2425–2445 MHz | WiFi Channel 6 (2437 MHz) |
| 19 – 21              | 2445–2455 MHz | WiFi Channel 11 (2462 MHz) |
| **26 (target)**      | **2480 MHz**| **None — non-overlapping — switch destination** |

---

## Algorithm

```
t = 0 s  : Zigbee PAN starts, all 17 nodes on channel 11 (2405 MHz)
t = 1 s  : End-devices begin uplink packets to coordinator (10 pkt/s each)
t = 5 s  : IEEE 802.11 AP begins 5 Mbps UDP file transfer (channel 1 / 2412 MHz)
t = 5.5 s: Coordinator ED scan returns 0.82 > threshold (0.50) → interference declared
t = 5.6 s: All 17 Zigbee nodes switch to channel 26 (2480 MHz) — 100 ms latency
t = 6+ s : Throughput fully recovers on non-overlapping channel
```

---

## Results

| Metric | Value |
|--------|-------|
| Interference Detection Time | 5.5 s |
| Channel Switch Completion   | 5.6 s |
| **Switching Latency**       | **100 ms** |
| Pre-interference Throughput | ~54 kbps |
| Post-switch Throughput      | ~54 kbps (full recovery) |

---

## Features

* Energy Detection (ED) based interference detection
* Automatic channel switching to non-overlapping channel 26 (2480 MHz)
* Switching latency measurement
* Throughput monitoring via coordinator data-indication callback
* Graph generation using Python (Matplotlib)

---

## System Requirements

* macOS or Linux
* Python 3 + matplotlib (`pip install matplotlib`)
* C++ compiler (clang/gcc), CMake, Ninja
* NS-3 version 3.38 or above

---

## Installation

### macOS

```bash
# Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew install cmake ninja gcc python3 pkg-config

git clone https://gitlab.com/nsnam/ns-3-dev.git
cd ns-3-dev
./ns3 configure
./ns3 build
```

### Linux (Ubuntu)

```bash
sudo apt update
sudo apt install build-essential git python3 cmake ninja-build

git clone https://gitlab.com/nsnam/ns-3-dev.git
cd ns-3-dev
./ns3 configure
./ns3 build
```

---

## How to Run

### 1. Run the NS-3 simulation

```bash
cp zigbee-wifi-interference.cc /path/to/ns-3-dev/scratch/

cd /path/to/ns-3-dev
./ns3 run scratch/zigbee-wifi-interference
```

This produces `throughput.tr` in the NS-3 root directory.

### 2. Generate the graph

```bash
pip install matplotlib
python3 plot_graphs.py
# Output: final_throughput.png
```

---

## NS-3 Modules Required

```
lr-wpan   wifi   mobility   internet   applications   flow-monitor
```

All included in the default NS-3 build.

---

## Files

| File | Purpose |
|------|---------|
| `zigbee-wifi-interference.cc` | NS-3 C++ simulation source |
| `throughput.tr` | Simulation output: `time(s)  throughput(kbps)` per second |
| `plot_graphs.py` | Python script — reads `.tr` and generates graph |
| `final_throughput.png` | Result graph (throughput + channel timeline) |

---

## Conclusion

The proposed algorithm successfully:

* Detects interference autonomously using Energy Detection (ED)
* Switches all 17 Zigbee devices to channel 26 (2480 MHz) in 100 ms
* Fully restores network throughput after channel switch
