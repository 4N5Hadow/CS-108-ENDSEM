"""
CS108 — End Semester Examination
Question 2: Project SENTRY — Quantum Beacon Analysis

Student Name:   [YOUR NAME HERE]
Roll Number:    [YOUR ROLL NUMBER HERE]

Allowed imports: numpy, matplotlib (only the functions given below)
No loops allowed in Task 1 or Task 2. Use NumPy vectorised operations only.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


# =============================================================================
# PROVIDED DATA  —  do not change
# =============================================================================

np.random.seed(42)

T = 10   # timelines
B = 7    # beacons per timeline
C = 12   # channels per beacon

# Raw beacon signals recorded by SWORD probes
signals = np.random.randn(T, B, C) * 15 + 50          # shape (T, B, C)

# Known safe signature when Ultron is NOT present
safe_signature = np.random.randn(B, C) * 8 + 50        # shape (B, C)

# Probe calibration — each probe has a different sensitivity
probe_sensitivity = np.random.uniform(0.8, 1.4, size=T) # shape (T,)

# Inject anomalies into timelines 2, 5, 8  (Ultron is present there)
for t in [2, 5, 8]:
    signals[t] += np.random.randn(B, C) * 50

TAU = 1.6   # threat threshold


# =============================================================================
# PROVIDED MATPLOTLIB FUNCTION  —  do not change
# =============================================================================

def plot_threat_map(norm_threat, compromised, beacon_names, timeline_labels):
    """
    Visualise the normalised threat matrix as a colour-coded heatmap.

    Parameters
    ----------
    norm_threat      : (T, B) ndarray   normalised threat scores
    compromised      : 1-D array/list   indices of compromised timelines
    beacon_names     : list[str]        label for each beacon  (length B)
    timeline_labels  : list[str]        label for each timeline (length T)
    """
    fig, ax = plt.subplots(figsize=(11, 6))

    cmap  = mcolors.LinearSegmentedColormap.from_list(
        "sentry", ["#1a1a2e", "#16213e", "#f4c430", "#c0392b"])
    im    = ax.imshow(norm_threat, aspect="auto", cmap=cmap, vmin=0, vmax=3)

    ax.set_xticks(range(B));  ax.set_xticklabels(beacon_names, rotation=40, ha="right")
    ax.set_yticks(range(T));  ax.set_yticklabels(timeline_labels)

    for t in compromised:
        for offset in (-0.5, 0.5):
            ax.axhline(t + offset, color="#ff4444", linewidth=2.5, linestyle="--")

    plt.colorbar(im, ax=ax, label="Normalised Threat Score")
    ax.set_title("PROJECT SENTRY  —  Quantum Beacon Threat Map", fontsize=13, pad=12)
    ax.set_xlabel("Beacon ID");  ax.set_ylabel("Timeline")
    plt.tight_layout()
    plt.savefig("threat_map.png", dpi=150)
    plt.show()
    print("Saved: threat_map.png")


# =============================================================================
# TASK 1 — Signal Calibration  [4 marks]
# =============================================================================

def calibrate(signals, probe_sensitivity):
    """
    Each probe has a sensitivity multiplier. Divide every reading by its
    probe's sensitivity to obtain the true signal level.

        calibrated[t, b, c] = signals[t, b, c] / probe_sensitivity[t]

    Parameters
    ----------
    signals           : ndarray, shape (T, B, C)
    probe_sensitivity : ndarray, shape (T,)

    Returns
    -------
    calibrated        : ndarray, shape (T, B, C)
    top_beacon        : int   — index (0-based) of the beacon with the
                                highest mean calibrated signal, averaged
                                across ALL timelines and ALL channels.

    No loops. One return statement returning both values as a tuple.
    """
    # TODO
    pass


# =============================================================================
# TASK 2 — Threat Scoring  [8 marks]
# =============================================================================

def compute_threat(calibrated, safe_signature, tau):
    """
    Step 1 — RMS deviation per (timeline, beacon):
        diff[t, b, c]  = calibrated[t, b, c] - safe_signature[b, c]
        threat[t, b]   = sqrt( mean_c( diff[t, b, c]^2 ) )

    Step 2 — Normalise each beacon's scores across timelines:
        norm_threat[t, b] = threat[t, b] / mean_t( threat[t, b] )

    Step 3 — A timeline is "compromised" if ANY of its beacons has
              norm_threat > tau.

    Parameters
    ----------
    calibrated     : ndarray, shape (T, B, C)
    safe_signature : ndarray, shape (B, C)
    tau            : float   threat threshold

    Returns
    -------
    norm_threat    : ndarray, shape (T, B)
    compromised    : ndarray, shape (K,)  — sorted indices of compromised
                                            timelines (dtype int)

    No loops.
    """
    # TODO
    pass


# =============================================================================
# TASK 3 — Visualisation  [4 marks]
# =============================================================================

def run_sentry(signals, safe_signature, probe_sensitivity, tau):
    """
    Tie everything together and produce the threat map.

    Steps
    -----
    3a. Call calibrate()  to get calibrated and top_beacon.
        Print:  f"Top beacon: Beacon-{top_beacon}"

    3b. Call compute_threat()  to get norm_threat and compromised.
        Print:  f"Compromised timelines: {compromised.tolist()}"

    3c. Build:
        beacon_names    — ["Beacon-0", "Beacon-1", ..., "Beacon-{B-1}"]
                          (use a list comprehension)
        timeline_labels — ["T-0000", "T-0001", ..., "T-{T-1:04d}"]
                          (use a list comprehension with zero-padded numbers)

    3d. Call plot_threat_map(norm_threat, compromised, beacon_names,
                             timeline_labels)

    No return value needed.
    """
    # TODO
    pass


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    run_sentry(signals, safe_signature, probe_sensitivity, TAU)
