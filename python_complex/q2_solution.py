"""
CS108 — End Semester Examination
Question 2: Project SENTRY — Quantum Beacon Analysis

*** SOLUTION FILE — NOT FOR DISTRIBUTION ***
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


# =============================================================================
# PROVIDED DATA
# =============================================================================

np.random.seed(42)

T = 10
B = 7
C = 12

signals           = np.random.randn(T, B, C) * 15 + 50
safe_signature    = np.random.randn(B, C) * 8 + 50
probe_sensitivity = np.random.uniform(0.8, 1.4, size=T)

for t in [2, 5, 8]:
    signals[t] += np.random.randn(B, C) * 50

TAU = 1.6


# =============================================================================
# PROVIDED MATPLOTLIB FUNCTION
# =============================================================================

def plot_threat_map(norm_threat, compromised, beacon_names, timeline_labels):
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
# TASK 1 — Signal Calibration
# =============================================================================

def calibrate(signals, probe_sensitivity):
    """
    KEY INSIGHT: probe_sensitivity has shape (T,).
    Direct division signals / probe_sensitivity would broadcast (T,B,C) / (T,)
    and fail — numpy aligns from the RIGHT, so (T,) aligns with the C axis.
    Solution: reshape to (T, 1, 1) so it broadcasts over B and C.
    """
    # Reshape (T,) → (T, 1, 1) so it broadcasts across B and C axes
    calibrated = signals / probe_sensitivity[:, np.newaxis, np.newaxis]  # (T, B, C)

    # Mean over timelines (axis 0) and channels (axis 2) → shape (B,)
    # then argmax gives the beacon index
    top_beacon = int(calibrated.mean(axis=(0, 2)).argmax())              # scalar

    return calibrated, top_beacon


# =============================================================================
# TASK 2 — Threat Scoring
# =============================================================================

def compute_threat(calibrated, safe_signature, tau):
    """
    KEY INSIGHTS:

    Step 1:
      calibrated     shape  (T, B, C)
      safe_signature shape     (B, C)
      diff = calibrated - safe_signature
      NumPy aligns from the RIGHT: (T,B,C) - (B,C) → (T,B,C)  ✓
      This is the non-trivial broadcast — students who loop over t are wrong.

    Step 2 — normalise:
      threat         shape  (T, B)
      threat.mean(axis=0) → shape (B,)
      norm_threat = threat / threat.mean(axis=0)
      (T, B) / (B,) → (T, B)  ✓  again aligns from right, non-trivial.
    """
    # Step 1 — RMS deviation
    # (T,B,C) - (B,C) → (T,B,C)  [non-trivial broadcast]
    diff    = calibrated - safe_signature                     # (T, B, C)
    threat  = np.sqrt((diff ** 2).mean(axis=2))              # (T, B)

    # Step 2 — normalise each beacon across timelines
    # (T,B) / (B,)  [non-trivial broadcast — mean over axis=0 gives (B,)]
    norm_threat = threat / threat.mean(axis=0)               # (T, B)

    # Step 3 — compromised timelines: any beacon exceeds tau
    compromised = np.where((norm_threat > tau).any(axis=1))[0]  # (K,)

    return norm_threat, compromised


# =============================================================================
# TASK 3 — Visualisation
# =============================================================================

def run_sentry(signals, safe_signature, probe_sensitivity, tau):
    # 3a
    calibrated, top_beacon = calibrate(signals, probe_sensitivity)
    print(f"Top beacon: Beacon-{top_beacon}")

    # 3b
    norm_threat, compromised = compute_threat(calibrated, safe_signature, tau)
    print(f"Compromised timelines: {compromised.tolist()}")

    # 3c
    beacon_names    = [f"Beacon-{b}"   for b in range(B)]
    timeline_labels = [f"T-{t:04d}"   for t in range(T)]

    # 3d
    plot_threat_map(norm_threat, compromised, beacon_names, timeline_labels)


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    run_sentry(signals, safe_signature, probe_sensitivity, TAU)
