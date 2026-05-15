"""Generated from Jupyter notebook: 2025-08-01 phmsa safety

Magics and shell lines are commented out. Run with a normal Python interpreter."""


# --- code cell ---

import glob
import os

import pandas as pd

# Path where your CSV files are stored
path = "*.csv"

# List of all CSV files
csv_files = glob.glob(path)

# Read and concatenate all CSV files into one DataFrame, adding source file name
df = pd.concat(
    (
        pd.read_csv(f, encoding="latin1").assign(source_file=os.path.basename(f))
        for f in csv_files
    ),
    ignore_index=True,
)

# Save the merged DataFrame to Parquet
df.to_parquet(
    "2015-2024 PHMSA IM Performance data for Gas Transmission.parquet", index=False
)

print(f"Merged {len(csv_files)} files into merged_data.parquet")


# --- code cell ---

import pandas as pd

file = "2015-2024 PHMSA IM Performance data for Gas Transmission.parquet"
# Load the merged parquet file
df = pd.read_parquet(file)

df.head()


# --- code cell ---

import pandas as pd

# Load the parquet file
file = "2015-2024 PHMSA IM Performance data for Gas Transmission.parquet"
df = pd.read_parquet(file)

# Clean column names
df.columns = df.columns.str.strip().str.replace("ï»¿", "", regex=True)

# Calculate issues per mile for each type (HCA, Non-HCA, MCA)
df["HCA Issues per Mile"] = (
    df["HCA Failures"].fillna(0) + df["HCA Leaks"].fillna(0)
) / df["HCA Miles"].replace(0, pd.NA)
df["Non-HCA Issues per Mile"] = df["Non-HCA Leaks"].fillna(0) / df[
    "Non-HCA Miles"
].replace(0, pd.NA)
df["MCA Issues per Mile"] = df["MCA Leaks"].fillna(0) / df["MCA Miles"].replace(
    0, pd.NA
)

# Group by operator and take mean issues per mile across years
operator_perf = (
    df.groupby(["Operator ID", "Operator Name"])
    .agg(
        {
            "HCA Issues per Mile": "mean",
            "Non-HCA Issues per Mile": "mean",
            "MCA Issues per Mile": "mean",
        }
    )
    .reset_index()
)

# Calculate an overall performance score (weighted average or simple mean)
operator_perf["Overall Issues per Mile"] = operator_perf[
    ["HCA Issues per Mile", "Non-HCA Issues per Mile", "MCA Issues per Mile"]
].mean(axis=1, skipna=True)

# Sort operators by best performance (fewest issues per mile)
best_operators = operator_perf.sort_values("Overall Issues per Mile", ascending=True)


# --- code cell ---

best_operators


# --- code cell ---

import pandas as pd

# Load parquet (requires pyarrow or fastparquet installed)
file = "2015-2024 PHMSA IM Performance data for Gas Transmission.parquet"
df = pd.read_parquet(file)

# Clean column names
df.columns = df.columns.str.strip().str.replace("ï»¿", "", regex=True)

# Clamp negative leak/failure counts to zero
for col in ["HCA Failures", "HCA Leaks", "Non-HCA Leaks", "MCA Leaks"]:
    df[col] = df[col].clip(lower=0)

# Filter out rows where miles are too small (to avoid inflated ratios)
df = df[(df["HCA Miles"].isna()) | (df["HCA Miles"] >= 0.1)]
df = df[(df["Non-HCA Miles"].isna()) | (df["Non-HCA Miles"] >= 0.1)]
df = df[(df["MCA Miles"].isna()) | (df["MCA Miles"] >= 0.1)]

# Compute issues per mile safely
df["HCA Issues per Mile"] = (df["HCA Failures"] + df["HCA Leaks"]) / df[
    "HCA Miles"
].replace(0, pd.NA)
df["Non-HCA Issues per Mile"] = df["Non-HCA Leaks"] / df["Non-HCA Miles"].replace(
    0, pd.NA
)
df["MCA Issues per Mile"] = df["MCA Leaks"] / df["MCA Miles"].replace(0, pd.NA)

# Group by operator and average across years
operator_perf = (
    df.groupby(["Operator ID", "Operator Name"])
    .agg(
        {
            "HCA Issues per Mile": "mean",
            "Non-HCA Issues per Mile": "mean",
            "MCA Issues per Mile": "mean",
        }
    )
    .reset_index()
)

# Compute overall issues per mile as mean across available categories
operator_perf["Overall Issues per Mile"] = operator_perf[
    ["HCA Issues per Mile", "Non-HCA Issues per Mile", "MCA Issues per Mile"]
].mean(axis=1, skipna=True)

# Sort best to worst (fewer issues per mile = better)
best_operators = operator_perf.sort_values("Overall Issues per Mile", ascending=True)

print(best_operators.head(5))


# --- code cell ---

import pandas as pd

# Load parquet file
file = "2015-2024 PHMSA IM Performance data for Gas Transmission.parquet"
df = pd.read_parquet(file)

# Clean column names
df.columns = df.columns.str.strip().str.replace("ï»¿", "", regex=True)

# Clamp negative values to zero
for col in ["HCA Failures", "HCA Leaks", "Non-HCA Leaks", "MCA Leaks"]:
    df[col] = df[col].clip(lower=0)

# Group by year and compute DOT-style metrics
dot_metrics = (
    df.groupby("Year")
    .apply(
        lambda x: pd.Series(
            {
                # HCA metrics
                "HCA Miles": x["HCA Miles"].sum(),
                "Significant Incidents per 10k HCA Miles": (
                    x["Significant Incident Reports"].sum() / x["HCA Miles"].sum()
                )
                * 10000
                if x["HCA Miles"].sum() > 0
                else None,
                "Failures per 5k HCA Miles": (
                    x["HCA Failures"].sum() / x["HCA Miles"].sum()
                )
                * 5000
                if x["HCA Miles"].sum() > 0
                else None,
                "Leaks per 1k HCA Miles": (x["HCA Leaks"].sum() / x["HCA Miles"].sum())
                * 1000
                if x["HCA Miles"].sum() > 0
                else None,
                # Non-HCA metrics
                "Non-HCA Miles": x["Non-HCA Miles"].sum(),
                "Leaks per 1k Non-HCA Miles": (
                    x["Non-HCA Leaks"].sum() / x["Non-HCA Miles"].sum()
                )
                * 1000
                if x["Non-HCA Miles"].sum() > 0
                else None,
                # MCA metrics
                "MCA Miles": x["MCA Miles"].sum(),
                "Significant Incidents per 10k MCA Miles": (
                    x["Significant Incident Reports"].sum() / x["MCA Miles"].sum()
                )
                * 10000
                if x["MCA Miles"].sum() > 0
                else None,
                "Leaks per 1k MCA Miles": (x["MCA Leaks"].sum() / x["MCA Miles"].sum())
                * 1000
                if x["MCA Miles"].sum() > 0
                else None,
            }
        )
    )
    .reset_index()
)

print(dot_metrics)


# --- code cell ---

import matplotlib.pyplot as plt
import pandas as pd

# Load parquet file
file = "2015-2024 PHMSA IM Performance data for Gas Transmission.parquet"
df = pd.read_parquet(file)

# Clean column names
df.columns = df.columns.str.strip().str.replace("ï»¿", "", regex=True)

# Clamp negative values
for col in ["HCA Failures", "HCA Leaks", "Non-HCA Leaks", "MCA Leaks"]:
    df[col] = df[col].clip(lower=0)

# Compute DOT-style metrics per year
dot_metrics = (
    df.groupby("Year")
    .apply(
        lambda x: pd.Series(
            {
                "HCA Miles": x["HCA Miles"].sum(),
                "Significant Incidents per 10k HCA Miles": (
                    x["Significant Incident Reports"].sum() / x["HCA Miles"].sum()
                )
                * 10000
                if x["HCA Miles"].sum() > 0
                else None,
                "Failures per 5k HCA Miles": (
                    x["HCA Failures"].sum() / x["HCA Miles"].sum()
                )
                * 5000
                if x["HCA Miles"].sum() > 0
                else None,
                "Leaks per 1k HCA Miles": (x["HCA Leaks"].sum() / x["HCA Miles"].sum())
                * 1000
                if x["HCA Miles"].sum() > 0
                else None,
                "Non-HCA Miles": x["Non-HCA Miles"].sum(),
                "Leaks per 1k Non-HCA Miles": (
                    x["Non-HCA Leaks"].sum() / x["Non-HCA Miles"].sum()
                )
                * 1000
                if x["Non-HCA Miles"].sum() > 0
                else None,
                "MCA Miles": x["MCA Miles"].sum(),
                "Significant Incidents per 10k MCA Miles": (
                    x["Significant Incident Reports"].sum() / x["MCA Miles"].sum()
                )
                * 10000
                if x["MCA Miles"].sum() > 0
                else None,
                "Leaks per 1k MCA Miles": (x["MCA Leaks"].sum() / x["MCA Miles"].sum())
                * 1000
                if x["MCA Miles"].sum() > 0
                else None,
            }
        )
    )
    .reset_index()
)

# Set font and style for minimalist plots
plt.rcParams.update(
    {"font.family": "serif", "axes.spines.top": False, "axes.spines.right": False}
)


# Helper plotting function
def plot_metric(df, column, ylabel):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["Year"], df[column], marker="o", color="black", label=column)
    ax.spines["left"].set_position(("outward", 5))
    ax.spines["bottom"].set_position(("outward", 5))
    ax.set_xlabel("Year")
    ax.set_ylabel(ylabel)
    ax.set_title(column)
    ax.grid(False)
    plt.savefig(f"{column.replace(' ', '_').lower()}.png", dpi=300, bbox_inches="tight")
    plt.show()



def main():
    # Plot each DOT metric
    plot_metric(
        dot_metrics,
        "Significant Incidents per 10k HCA Miles",
        "Incidents per 10k HCA Miles",
    )
    plot_metric(dot_metrics, "Failures per 5k HCA Miles", "Failures per 5k HCA Miles")
    plot_metric(dot_metrics, "Leaks per 1k HCA Miles", "Leaks per 1k HCA Miles")
    plot_metric(dot_metrics, "Leaks per 1k Non-HCA Miles", "Leaks per 1k Non-HCA Miles")
    plot_metric(
        dot_metrics,
        "Significant Incidents per 10k MCA Miles",
        "Incidents per 10k MCA Miles",
    )
    plot_metric(dot_metrics, "Leaks per 1k MCA Miles", "Leaks per 1k MCA Miles")


    # --- code cell ---

    import pandas as pd

    # Load the uploaded files
    file_summary = "GT IM Performance National Summary.csv"
    file_incidents = "GT HCA Incidents by Cause from Incidents.csv"
    file_leaks = "GT HCA Leaks by Cause.csv"
    file_failures = "GT HCA Failures by Cause.csv"

    summary_df = pd.read_csv(file_summary)
    incidents_df = pd.read_csv(file_incidents)
    leaks_df = pd.read_csv(file_leaks)
    failures_df = pd.read_csv(file_failures)


    # Summarize causes across incidents, leaks, and failures over time

    # Summarize incidents by cause
    incidents_summary = (
        incidents_df.groupby("Cause Category")["Unnamed: 2"].sum().reset_index()
    )
    incidents_summary.columns = ["Cause", "Incident Count"]

    # Summarize leaks by cause
    leaks_cause_cols = [
        c
        for c in leaks_df.columns
        if c not in ["Calendar Year", "Total HCA Leaks", "Cause Category"]
    ]
    leaks_summary = leaks_df[leaks_cause_cols].sum().reset_index()
    leaks_summary.columns = ["Cause", "Leak Count"]

    # Summarize failures by cause
    failures_cause_cols = [
        c
        for c in failures_df.columns
        if c not in ["Calendar Year", "Total HCA Failures", "Cause Category"]
    ]
    failures_summary = failures_df[failures_cause_cols].sum().reset_index()
    failures_summary.columns = ["Cause", "Failure Count"]

    # Merge into a single cause table
    cause_summary = pd.merge(incidents_summary, leaks_summary, on="Cause", how="outer")
    cause_summary = pd.merge(
        cause_summary, failures_summary, on="Cause", how="outer"
    ).fillna(0)

    # Compute totals and percentages
    cause_summary["Total Count"] = cause_summary[
        ["Incident Count", "Leak Count", "Failure Count"]
    ].sum(axis=1)
    total_all = cause_summary["Total Count"].sum()
    cause_summary["Percent of Total"] = (cause_summary["Total Count"] / total_all) * 100


    # --- code cell ---

    import matplotlib.pyplot as plt

    # Pie chart for cause proportions
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(
        cause_summary["Percent of Total"],
        labels=cause_summary["Cause"],
        autopct="%1.1f%%",
        startangle=140,
        colors=["#222222", "#555555", "#888888", "#aaaaaa", "#cccccc"],
    )
    ax.set_title("Proportion of Causes (Incidents, Leaks, Failures Combined)")
    plt.savefig("cause_proportion_pie.png", dpi=300, bbox_inches="tight")
    plt.show()

    # Stacked bar chart for incidents, leaks, and failures by cause
    fig, ax = plt.subplots(figsize=(10, 6))
    bar_width = 0.6

    ax.bar(
        cause_summary["Cause"],
        cause_summary["Incident Count"],
        label="Incidents",
        color="#222222",
    )
    ax.bar(
        cause_summary["Cause"],
        cause_summary["Leak Count"],
        bottom=cause_summary["Incident Count"],
        label="Leaks",
        color="#777777",
    )
    ax.bar(
        cause_summary["Cause"],
        cause_summary["Failure Count"],
        bottom=cause_summary["Incident Count"] + cause_summary["Leak Count"],
        label="Failures",
        color="#bbbbbb",
    )

    ax.set_ylabel("Count")
    ax.set_title("Stacked Causes: Incidents, Leaks, Failures")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xticklabels(cause_summary["Cause"], rotation=45, ha="right")
    ax.legend()

    plt.savefig("cause_stacked_bar.png", dpi=300, bbox_inches="tight")
    plt.show()


    # --- code cell ---

    # Sort cause summary by total count descending
    cause_summary_sorted = cause_summary.sort_values("Total Count", ascending=False)

    # Pie chart sorted
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(
        cause_summary_sorted["Percent of Total"],
        labels=cause_summary_sorted["Cause"],
        autopct="%1.1f%%",
        startangle=140,
        colors=["#222222", "#555555", "#888888", "#aaaaaa", "#cccccc"],
    )
    ax.set_title("Proportion of Causes (Sorted by Total Issues)")
    plt.savefig("cause_proportion_pie_sorted.png", dpi=300, bbox_inches="tight")
    plt.show()

    # Stacked bar sorted
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(
        cause_summary_sorted["Cause"],
        cause_summary_sorted["Incident Count"],
        label="Incidents",
        color="#222222",
    )
    ax.bar(
        cause_summary_sorted["Cause"],
        cause_summary_sorted["Leak Count"],
        bottom=cause_summary_sorted["Incident Count"],
        label="Leaks",
        color="#777777",
    )
    ax.bar(
        cause_summary_sorted["Cause"],
        cause_summary_sorted["Failure Count"],
        bottom=cause_summary_sorted["Incident Count"] + cause_summary_sorted["Leak Count"],
        label="Failures",
        color="#bbbbbb",
    )

    ax.set_ylabel("Count")
    ax.set_title("Stacked Causes: Incidents, Leaks, Failures (Sorted by Total)")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xticks(range(len(cause_summary_sorted["Cause"])))
    ax.grid(False)
    ax.set_xticklabels(cause_summary_sorted["Cause"], rotation=45, ha="right")
    ax.legend()

    plt.savefig("cause_stacked_bar_sorted.png", dpi=300, bbox_inches="tight")
    plt.show()


    # --- code cell ---

    # Create a clean minimalist line chart showing equipment vs. all other causes in gray

    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot all other causes in light gray
    for cause in pivot_percent.columns:
        if cause != "Equipment":
            ax.plot(
                pivot_percent.index,
                pivot_percent[cause],
                color="#cccccc",
                linewidth=1,
                alpha=0.7,
            )

    # Plot equipment in black
    ax.plot(
        pivot_percent.index,
        pivot_percent["Equipment"],
        color="black",
        linewidth=2,
        marker="o",
        label="Equipment",
    )

    # Annotate equipment percentage at each year
    for year, value in zip(pivot_percent.index, pivot_percent["Equipment"]):
        ax.text(year, value + 1, f"{value:.1f}%", ha="center", va="bottom", fontsize=9)

    # Minimalist styling
    ax.set_ylabel("Percent of Annual Issues")
    ax.set_xlabel("Year")
    ax.set_title("Equipment vs. Other Causes (Share of Annual Issues)")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_position(("outward", 5))
    ax.spines["bottom"].set_position(("outward", 5))

    ax.grid(False)
    ax.legend().set_visible(False)

    plt.tight_layout()
    plt.savefig("equipment_dominance_trend.png", dpi=300, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    main()
