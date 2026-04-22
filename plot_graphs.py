import matplotlib.pyplot as plt

# Read throughput file
time = []
throughput = []

with open("throughput.tr", "r") as f:
    for line in f:
        t, th = line.split()
        time.append(float(t))
        throughput.append(float(th))

# Plot graph
plt.figure()
plt.plot(time, throughput, marker='o')
plt.title("Throughput vs Time (NS-3 Simulation)")
plt.xlabel("Time (seconds)")
plt.ylabel("Throughput (kbps)")
plt.grid()

# Mark switching point
plt.axvline(x=6, linestyle='--')
plt.text(6, max(throughput)*0.8, 'Channel Switch', rotation=90)

plt.savefig("final_throughput.png")
plt.show()
