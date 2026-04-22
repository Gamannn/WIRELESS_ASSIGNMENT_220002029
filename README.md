# 📡 Interference-Aware Channel Switching in IEEE 802.15.4 (NS-3)

## 📌 Overview

This project implements an **interference-aware channel switching algorithm** for IEEE 802.15.4 (Zigbee) networks using **NS-3**.

A Zigbee coordinator continuously monitors **Energy Detection (ED)** levels. When interference from IEEE 802.11 (Wi-Fi) is detected, the network **autonomously switches to a non-overlapping channel**, improving performance.

---

## ⚙️ Features

* Energy Detection (ED) based interference detection
* Automatic channel switching
* Switching latency measurement
* Throughput monitoring using FlowMonitor
* Graph generation using Python (Matplotlib)

---

## 🖥️ System Requirements

* macOS or Linux
* Python 3
* Git
* C++ compiler (clang/gcc)
* CMake, Ninja

---

## 🚀 Installation

### 🍎 macOS

#### 1. Install Homebrew (if not installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 2. Install Dependencies

```bash
brew install cmake ninja gcc python3 pkg-config
```

#### 3. Clone NS-3

```bash
git clone https://gitlab.com/nsnam/ns-3-dev.git
cd ns-3-dev
```

#### 4. Build NS-3

```bash
./ns3 configure
./ns3 build
```

---

### 🐧 Linux (Ubuntu)

```bash
sudo apt update
sudo apt install build-essential git python3 cmake ninja-build

git clone https://gitlab.com/nsnam/ns-3-dev.git
cd ns-3-dev

./ns3 configure
./ns3 build
```

---

## ▶️ Running the Simulation

### 1. Place the file

Copy:

```
zigbee-wifi-interference.cc
```

into:

```
ns-3-dev/scratch/
```

---

### 2. Run simulation

```bash
./ns3 run scratch/zigbee-wifi-interference.cc
```

---

## 📊 Output

After running:

* `throughput.tr` → Throughput data
* Console output → Detection time, switch time, latency

Example:

```
WiFi started at: 5s
Interference detected at: 6s
Channel switched at: 6.1s

Switching Latency: 0.1 s
```

---

## 📈 Graph Generation

### 1. Install matplotlib

```bash
pip install matplotlib
```

### 2. Run script

```bash
python plot_graphs.py
```

### 3. Output

* `final_throughput.png`

---

## 📉 Results

* Interference detected at ≈ 6 seconds
* Channel switched at ≈ 6.1 seconds
* Switching latency ≈ **0.1 seconds**
* Throughput stabilizes after switching

---

## 📁 Project Structure

```
zigbee-interference-ns3/
│
├── zigbee-wifi-interference.cc
├── throughput.tr
├── plot_graphs.py
├── final_throughput.png
└── README.md
```

---

## 🎯 Conclusion

The proposed algorithm successfully:

* Detects interference using ED
* Switches channels autonomously
* Minimizes switching latency
* Restores network throughput

