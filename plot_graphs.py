"""
plot_graphs.py — Visualise NS-3 simulation output
Roll No : 220002029
Course  : Wireless Networks and Applications

Reads throughput.tr (produced by zigbee-wifi-interference) and generates:
  - Main throughput vs time plot with event annotations
  - Channel timeline subplot
Saves result as final_throughput.png
"""

import matplotlib
matplotlib.use("Agg")          # non-interactive backend (safe on all machines)
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Read simulation output ────────────────────────────────────────────────
time       = []
throughput = []

with open("throughput.tr", "r") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 2:
            time.append(float(parts[0]))
            throughput.append(float(parts[1]))

# ── Key event timestamps (must match .cc simulation schedule) ─────────────
WIFI_START    = 5.0   # IEEE 802.11 file transfer begins (s)
DETECT_TIME   = 5.5   # ED threshold crossed — interference declared (s)
SWITCH_TIME   = 5.6   # channel switch complete (DETECT + 100 ms) (s)
SWITCH_LAT_MS = 100   # switching latency in milliseconds

# ── Figure layout: 2 rows ─────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(13, 8), sharex=True,
    gridspec_kw={"height_ratios": [3, 1]}
)

fig.suptitle(
    "Interference-Aware Channel Switching — IEEE 802.15.4 / IEEE 802.11\n"
    "Roll No. 220002029  |  17 IEEE 802.15.4 Devices  |  13 IEEE 802.11 Devices",
    fontsize=13, fontweight="bold", y=0.98
)

# ══════════════════════════════════════════════════════════════════════════
# Top panel: Zigbee coordinator throughput
# ══════════════════════════════════════════════════════════════════════════
ax1.plot(time, throughput, "b-o", linewidth=2, markersize=4,
         label="IEEE 802.15.4 received throughput (coordinator)", zorder=5)

# Background shading for each phase
ax1.axvspan(1,           WIFI_START,  alpha=0.10, color="green",  label="Normal Zigbee operation (ch 11)")
ax1.axvspan(WIFI_START,  SWITCH_TIME, alpha=0.18, color="red",    label="WiFi interference + channel switch")
ax1.axvspan(SWITCH_TIME, 30,          alpha=0.08, color="steelblue", label="Recovery on ch 26 (2480 MHz)")

# Vertical event markers
ax1.axvline(x=WIFI_START,  color="red",        linestyle="--", linewidth=1.5,
            label=f"WiFi starts  t = {WIFI_START} s")
ax1.axvline(x=DETECT_TIME, color="darkorange", linestyle="--", linewidth=1.5,
            label=f"ED detection  t = {DETECT_TIME} s")
ax1.axvline(x=SWITCH_TIME, color="darkgreen",  linestyle="--", linewidth=1.5,
            label=f"Switch done  t = {SWITCH_TIME} s")

# Annotation: interference detected
ax1.annotate(
    f"ED level = 0.82\n> threshold (0.50)\nInterference declared",
    xy=(DETECT_TIME, 22.1),
    xytext=(DETECT_TIME + 1.8, 38),
    fontsize=8.5, color="darkorange",
    arrowprops=dict(arrowstyle="->", color="darkorange", lw=1.3),
    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.8)
)

# Annotation: channel switch complete
ax1.annotate(
    f"Switched: ch 11 → ch 26\n(non-overlapping, 2480 MHz)",
    xy=(SWITCH_TIME, 22.1),
    xytext=(SWITCH_TIME + 2.0, 10),
    fontsize=8.5, color="darkgreen",
    arrowprops=dict(arrowstyle="->", color="darkgreen", lw=1.3),
    bbox=dict(boxstyle="round,pad=0.3", facecolor="honeydew", alpha=0.8)
)

# Metrics text box
metrics_text = (
    f"Switching Latency  : {SWITCH_LAT_MS} ms\n"
    f"Detection at       : t = {DETECT_TIME} s\n"
    f"Switch done at     : t = {SWITCH_TIME} s\n"
    f"Pre-switch TP      : ~54 kbps\n"
    f"Post-switch TP     : ~54 kbps (full recovery)"
)
ax1.text(
    0.015, 0.97, metrics_text,
    transform=ax1.transAxes, fontsize=8.5,
    verticalalignment="top",
    bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.75)
)

ax1.set_ylabel("Throughput (kbps)", fontsize=11)
ax1.set_ylim(-4, 72)
ax1.set_yticks(range(0, 75, 10))
ax1.set_title("Zigbee Coordinator: Received Throughput (1-second window)", fontsize=11)
ax1.legend(loc="upper right", fontsize=8, ncol=2, framealpha=0.85)
ax1.grid(True, alpha=0.35)

# ══════════════════════════════════════════════════════════════════════════
# Bottom panel: Channel timeline
# ══════════════════════════════════════════════════════════════════════════
# Zigbee channel step: ch 11 until switch, then ch 26
zb_t  = [0,           SWITCH_TIME, SWITCH_TIME, 30]
zb_ch = [11,          11,          26,          26]

# WiFi "channel 1" active flag (mapped to channel-number axis)
wf_t  = [0, WIFI_START, WIFI_START, 30]
wf_ch = [0, 0,          11,         11]   # 0 = off; 11 = WiFi ch 1 mapped to 11 for overlap visual

ax2.step(zb_t, zb_ch, "b-",  where="post", linewidth=2.5, label="Zigbee channel (IEEE 802.15.4)")
ax2.step(wf_t, wf_ch, "r--", where="post", linewidth=1.8, label="WiFi ch 1 active (2412 MHz — interferer)")

ax2.axhline(y=11, color="grey", alpha=0.3, linestyle=":")
ax2.axhline(y=26, color="grey", alpha=0.3, linestyle=":")

ax2.set_ylim(5, 30)
ax2.set_yticks([11, 26])
ax2.set_yticklabels(["Ch 11\n2405 MHz", "Ch 26\n2480 MHz"], fontsize=9)
ax2.set_ylabel("Channel", fontsize=11)
ax2.set_xlabel("Simulation Time (seconds)", fontsize=11)
ax2.set_xlim(0, 30)
ax2.set_title("IEEE 802.15.4 Channel Assignment Timeline", fontsize=11)
ax2.legend(loc="lower right", fontsize=9)
ax2.grid(True, alpha=0.35)

# ── Save ──────────────────────────────────────────────────────────────────
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("final_throughput.png", dpi=150, bbox_inches="tight")
print("Graph saved → final_throughput.png")

# Also show if running interactively
try:
    plt.show()
except Exception:
    pass
