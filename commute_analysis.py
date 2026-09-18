"""Lab 1 / Topic 1: a small commute-time analysis using illustrative data.

Run: python3 commute_analysis.py
The figure is saved beside this script; no network or display is required.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # Save figures even in a terminal without a display.
import matplotlib.pyplot as plt
import numpy as np


# Hand-created examples, NOT observations collected from real students.
# Each value represents one dorm-to-classroom trip, measured in minutes.
TRAVEL_TIMES = np.array([
    22, 25, 24, 28, 23, 26, 30, 24, 27, 25,
    21, 29, 26, 24, 32, 25, 28, 23, 27, 35,
    24, 26, 29, 25, 31, 22, 28, 40, 27, 33,
])


def main():
    mean_time = np.mean(TRAVEL_TIMES)
    median_time = np.median(TRAVEL_TIMES)
    p95 = np.percentile(TRAVEL_TIMES, 95)
    suggested_buffer = int(np.ceil(p95))
    covered_trips = int(np.sum(TRAVEL_TIMES <= suggested_buffer))
    coverage = covered_trips / len(TRAVEL_TIMES) * 100

    # Count a trip as on time when its duration is at most the time available.
    buffers = np.arange(20, 46)
    on_time_rates = np.array([
        np.mean(TRAVEL_TIMES <= minutes) * 100 for minutes in buffers
    ])

    plt.rcParams.update({"font.size": 12, "axes.spines.top": False,
                         "axes.spines.right": False, "figure.facecolor": "white"})
    fig, (ax1, ax2) = plt.subplots(figsize=(14, 7.875), ncols=2)
    fig.subplots_adjust(left=0.08, right=0.97, bottom=0.21, top=0.72, wspace=0.30)
    fig.suptitle("When should I leave for class?", fontsize=25, fontweight="bold", y=0.94)
    fig.text(0.5, 0.87, f"{len(TRAVEL_TIMES)} illustrative dorm-to-classroom trips",
             ha="center", color="#56616d")
    fig.text(0.5, 0.80,
             f"Average: {mean_time:.1f} min     |     Suggested buffer: {suggested_buffer} min"
             f"     |     Sample coverage: {covered_trips}/{len(TRAVEL_TIMES)} trips",
             ha="center", fontsize=14, color="#176b64")

    ax1.hist(TRAVEL_TIMES, bins=np.arange(20, 46, 2), color="#78b8c4", edgecolor="white")
    ax1.axvline(mean_time, color="#374151", linestyle="--", linewidth=2,
                label=f"Mean: {mean_time:.1f} min")
    ax1.axvline(suggested_buffer, color="#c77b19", linewidth=2,
                label=f"Suggested: {suggested_buffer} min")
    ax1.set(title="Most trips are short; a few take longer", xlabel="Travel time (minutes)",
            ylabel="Number of trips", xlim=(20, 45), yticks=np.arange(0, 9, 2))
    ax1.legend(frameon=False, fontsize=11)

    ax2.step(buffers, on_time_rates, where="post", linewidth=2.5, color="#176b64",
             label="On-time share of sample trips")
    ax2.axhline(95, color="#89929d", linestyle=":", linewidth=1.5, label="95% reference")
    ax2.scatter([suggested_buffer], [coverage], color="#c77b19", s=65, zorder=3)
    ax2.annotate(f"{suggested_buffer} min: {coverage:.1f}% of sample trips",
                 xy=(suggested_buffer, coverage), xytext=(29, 55), fontsize=11,
                 arrowprops={"arrowstyle": "->", "color": "#c77b19"})
    ax2.set(title="More time allows more trips to finish", xlabel="Minutes before class you leave",
            ylabel="Sample trips arriving on time (%)", xlim=(20, 45), ylim=(0, 105))
    ax2.legend(loc="lower right", frameon=False, fontsize=10)
    for ax in (ax1, ax2):
        ax.set_axisbelow(True)
        ax.grid(axis="y", alpha=0.18)

    fig.text(0.08, 0.10, "Suggested buffer = sample 95th percentile, rounded up to a whole minute.",
             fontsize=11, color="#56616d")
    fig.text(0.08, 0.06, "Illustrative data only. Sample coverage does not guarantee future punctuality.",
             fontsize=11, color="#56616d")
    output_path = Path(__file__).resolve().with_name("commute_analysis.png")
    fig.savefig(output_path, dpi=180, facecolor="white")
    plt.close(fig)

    print(f"DATA: {len(TRAVEL_TIMES)} hand-created illustrative trips, not real observations.")
    print(f"Mean travel time:       {mean_time:.2f} minutes")
    print(f"Median travel time:     {median_time:.2f} minutes")
    print(f"95th percentile:        {p95:.2f} minutes")
    print(f"Suggested buffer:      {suggested_buffer} minutes before class")
    print(f"Sample on-time share:  {covered_trips}/{len(TRAVEL_TIMES)} ({coverage:.1f}%)")
    print("This is a sample-based illustration, not a guarantee for future trips.")
    print(f"Figure saved to: {output_path}")


if __name__ == "__main__":
    main()
