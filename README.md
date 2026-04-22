# Zigbee Wi-Fi Interference Simulation (NS-3)

## Description
This project implements an interference-aware channel switching algorithm for IEEE 802.15.4 networks using NS-3.

## Features
- Energy Detection based interference detection
- Automatic channel switching
- Throughput monitoring using FlowMonitor

## Files
- zigbee-wifi-interference.cc → NS-3 simulation code
- throughput.tr → simulation output
- plot_graphs.py → graph generation script
- final_throughput.png → result graph

## How to Run
1. Place `.cc` file inside NS-3 scratch folder
2. Run:
   ./ns3 run scratch/zigbee-wifi-interference.cc
3. Generate graph:
   python plot_graphs.py
