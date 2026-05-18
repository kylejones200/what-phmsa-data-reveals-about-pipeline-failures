"""Generated from Jupyter notebook: 2025-08-01 phmsa safety

Magics and shell lines are commented out. Run with a normal Python interpreter."""

import glob
import os

import matplotlib.pyplot as plt
import pandas as pd


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


def path_where_your_csv_files_are_stored() -> None:
    path = "*.csv"
    csv_files = glob.glob(path)
    df = pd.concat(
        (
            pd.read_csv(f, encoding="latin1").assign(source_file=os.path.basename(f))
            for f in csv_files
        ),
        ignore_index=True,
    )
    df.to_parquet(
        "2015-2024 PHMSA IM Performance data for Gas Transmission.parquet", index=False
    )
    print(f"Merged {len(csv_files)} files into merged_data.parquet")


def load_the_merged_parquet_file() -> None:
    file = "2015-2024 PHMSA IM Performance data for Gas Transmission.parquet"
    df = pd.read_parquet(file)
    df.head()


def load_the_parquet_file() -> None:
    file = "2015-2024 PHMSA IM Performance data for Gas Transmission.parquet"
    df = pd.read_parquet(file)
    df.columns = df.columns.str.strip().str.replace("ï»¿", "", regex=True)
    df["HCA Issues per Mile"] = (
        df["HCA Failures"].fillna(0) + df["HCA Leaks"].fillna(0)
    ) / df["HCA Miles"].replace(0, pd.NA)
    df["Non-HCA Issues per Mile"] = df["Non-HCA Leaks"].fillna(0) / df[
        "Non-HCA Miles"
    ].replace(0, pd.NA)
    df["MCA Issues per Mile"] = df["MCA Leaks"].fillna(0) / df["MCA Miles"].replace(
        0, pd.NA
    )
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
    operator_perf["Overall Issues per Mile"] = operator_perf[
        ["HCA Issues per Mile", "Non-HCA Issues per Mile", "MCA Issues per Mile"]
    ].mean(axis=1, skipna=True)
    operator_perf.sort_values("Overall Issues per Mile", ascending=True)


def notebook_step_004() -> None:
    best_operators


def load_parquet_requires_pyarrow_or_fastparquet_ins() -> None:
    file = "2015-2024 PHMSA IM Performance data for Gas Transmission.parquet"
    df = pd.read_parquet(file)
    df.columns = df.columns.str.strip().str.replace("ï»¿", "", regex=True)
    for col in ["HCA Failures", "HCA Leaks", "Non-HCA Leaks", "MCA Leaks"]:
        df[col] = df[col].clip(lower=0)

    df = df[df["HCA Miles"].isna() | (df["HCA Miles"] >= 0.1)]
    df = df[df["Non-HCA Miles"].isna() | (df["Non-HCA Miles"] >= 0.1)]
    df = df[df["MCA Miles"].isna() | (df["MCA Miles"] >= 0.1)]
    df["HCA Issues per Mile"] = (df["HCA Failures"] + df["HCA Leaks"]) / df[
        "HCA Miles"
    ].replace(0, pd.NA)
    df["Non-HCA Issues per Mile"] = df["Non-HCA Leaks"] / df["Non-HCA Miles"].replace(
        0, pd.NA
    )
    df["MCA Issues per Mile"] = df["MCA Leaks"] / df["MCA Miles"].replace(0, pd.NA)
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
    operator_perf["Overall Issues per Mile"] = operator_perf[
        ["HCA Issues per Mile", "Non-HCA Issues per Mile", "MCA Issues per Mile"]
    ].mean(axis=1, skipna=True)
    best_operators = operator_perf.sort_values(
        "Overall Issues per Mile", ascending=True
    )
    print(best_operators.head(5))


def load_parquet_file() -> None:
    file = "2015-2024 PHMSA IM Performance data for Gas Transmission.parquet"
    df = pd.read_parquet(file)
    df.columns = df.columns.str.strip().str.replace("ï»¿", "", regex=True)
    for col in ["HCA Failures", "HCA Leaks", "Non-HCA Leaks", "MCA Leaks"]:
        df[col] = df[col].clip(lower=0)

    dot_metrics = (
        df.groupby("Year")
        .apply(
            lambda x: pd.Series(
                {
                    "HCA Miles": x["HCA Miles"].sum(),
                    "Significant Incidents per 10k HCA Miles": x[
                        "Significant Incident Reports"
                    ].sum()
                    / x["HCA Miles"].sum()
                    * 10000
                    if x["HCA Miles"].sum() > 0
                    else None,
                    "Failures per 5k HCA Miles": x["HCA Failures"].sum()
                    / x["HCA Miles"].sum()
                    * 5000
                    if x["HCA Miles"].sum() > 0
                    else None,
                    "Leaks per 1k HCA Miles": x["HCA Leaks"].sum()
                    / x["HCA Miles"].sum()
                    * 1000
                    if x["HCA Miles"].sum() > 0
                    else None,
                    "Non-HCA Miles": x["Non-HCA Miles"].sum(),
                    "Leaks per 1k Non-HCA Miles": x["Non-HCA Leaks"].sum()
                    / x["Non-HCA Miles"].sum()
                    * 1000
                    if x["Non-HCA Miles"].sum() > 0
                    else None,
                    "MCA Miles": x["MCA Miles"].sum(),
                    "Significant Incidents per 10k MCA Miles": x[
                        "Significant Incident Reports"
                    ].sum()
                    / x["MCA Miles"].sum()
                    * 10000
                    if x["MCA Miles"].sum() > 0
                    else None,
                    "Leaks per 1k MCA Miles": x["MCA Leaks"].sum()
                    / x["MCA Miles"].sum()
                    * 1000
                    if x["MCA Miles"].sum() > 0
                    else None,
                }
            )
        )
        .reset_index()
    )
    print(dot_metrics)


def load_parquet_file_2() -> None:
    file = "2015-2024 PHMSA IM Performance data for Gas Transmission.parquet"
    df = pd.read_parquet(file)
    df.columns = df.columns.str.strip().str.replace("ï»¿", "", regex=True)
    for col in ["HCA Failures", "HCA Leaks", "Non-HCA Leaks", "MCA Leaks"]:
        df[col] = df[col].clip(lower=0)

    dot_metrics = (
        df.groupby("Year")
        .apply(
            lambda x: pd.Series(
                {
                    "HCA Miles": x["HCA Miles"].sum(),
                    "Significant Incidents per 10k HCA Miles": x[
                        "Significant Incident Reports"
                    ].sum()
                    / x["HCA Miles"].sum()
                    * 10000
                    if x["HCA Miles"].sum() > 0
                    else None,
                    "Failures per 5k HCA Miles": x["HCA Failures"].sum()
                    / x["HCA Miles"].sum()
                    * 5000
                    if x["HCA Miles"].sum() > 0
                    else None,
                    "Leaks per 1k HCA Miles": x["HCA Leaks"].sum()
                    / x["HCA Miles"].sum()
                    * 1000
                    if x["HCA Miles"].sum() > 0
                    else None,
                    "Non-HCA Miles": x["Non-HCA Miles"].sum(),
                    "Leaks per 1k Non-HCA Miles": x["Non-HCA Leaks"].sum()
                    / x["Non-HCA Miles"].sum()
                    * 1000
                    if x["Non-HCA Miles"].sum() > 0
                    else None,
                    "MCA Miles": x["MCA Miles"].sum(),
                    "Significant Incidents per 10k MCA Miles": x[
                        "Significant Incident Reports"
                    ].sum()
                    / x["MCA Miles"].sum()
                    * 10000
                    if x["MCA Miles"].sum() > 0
                    else None,
                    "Leaks per 1k MCA Miles": x["MCA Leaks"].sum()
                    / x["MCA Miles"].sum()
                    * 1000
                    if x["MCA Miles"].sum() > 0
                    else None,
                }
            )
        )
        .reset_index()
    )
    plt.rcParams.update(
        {"font.family": "serif", "axes.spines.top": False, "axes.spines.right": False}
    )
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


def load_the_uploaded_files() -> None:
    file_summary = "GT IM Performance National Summary.csv"
    file_incidents = "GT HCA Incidents by Cause from Incidents.csv"
    file_leaks = "GT HCA Leaks by Cause.csv"
    file_failures = "GT HCA Failures by Cause.csv"
    pd.read_csv(file_summary)
    incidents_df = pd.read_csv(file_incidents)
    leaks_df = pd.read_csv(file_leaks)
    failures_df = pd.read_csv(file_failures)
    incidents_summary = (
        incidents_df.groupby("Cause Category")["Unnamed: 2"].sum().reset_index()
    )
    incidents_summary.columns = ["Cause", "Incident Count"]
    leaks_cause_cols = [
        c
        for c in leaks_df.columns
        if c not in ["Calendar Year", "Total HCA Leaks", "Cause Category"]
    ]
    leaks_summary = leaks_df[leaks_cause_cols].sum().reset_index()
    leaks_summary.columns = ["Cause", "Leak Count"]
    failures_cause_cols = [
        c
        for c in failures_df.columns
        if c not in ["Calendar Year", "Total HCA Failures", "Cause Category"]
    ]
    failures_summary = failures_df[failures_cause_cols].sum().reset_index()
    failures_summary.columns = ["Cause", "Failure Count"]
    cause_summary = pd.merge(incidents_summary, leaks_summary, on="Cause", how="outer")
    cause_summary = pd.merge(
        cause_summary, failures_summary, on="Cause", how="outer"
    ).fillna(0)
    cause_summary["Total Count"] = cause_summary[
        ["Incident Count", "Leak Count", "Failure Count"]
    ].sum(axis=1)
    total_all = cause_summary["Total Count"].sum()
    cause_summary["Percent of Total"] = cause_summary["Total Count"] / total_all * 100


def pie_chart_for_cause_proportions() -> None:
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
    fig, ax = plt.subplots(figsize=(10, 6))
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


def sort_cause_summary_by_total_count_descending() -> None:
    cause_summary_sorted = cause_summary.sort_values("Total Count", ascending=False)
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
        bottom=cause_summary_sorted["Incident Count"]
        + cause_summary_sorted["Leak Count"],
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


def create_a_clean_minimalist_line_chart_showing_equ() -> None:
    fig, ax = plt.subplots(figsize=(12, 6))
    for cause in pivot_percent.columns:
        if cause != "Equipment":
            ax.plot(
                pivot_percent.index,
                pivot_percent[cause],
                color="#cccccc",
                linewidth=1,
                alpha=0.7,
            )

    ax.plot(
        pivot_percent.index,
        pivot_percent["Equipment"],
        color="black",
        linewidth=2,
        marker="o",
        label="Equipment",
    )
    for year, value in zip(pivot_percent.index, pivot_percent["Equipment"]):
        ax.text(year, value + 1, f"{value:.1f}%", ha="center", va="bottom", fontsize=9)

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


def main() -> None:
    path_where_your_csv_files_are_stored()
    load_the_merged_parquet_file()
    load_the_parquet_file()
    notebook_step_004()
    load_parquet_requires_pyarrow_or_fastparquet_ins()
    load_parquet_file()
    load_parquet_file_2()
    load_the_uploaded_files()
    pie_chart_for_cause_proportions()
    sort_cause_summary_by_total_count_descending()
    create_a_clean_minimalist_line_chart_showing_equ()


if __name__ == "__main__":
    main()
