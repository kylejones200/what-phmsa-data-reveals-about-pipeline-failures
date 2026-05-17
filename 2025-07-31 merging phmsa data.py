"""Generated from Jupyter notebook: 2025-07-31 merging phmsa data

Magics and shell lines are commented out. Run with a normal Python interpreter."""

import glob
import os

import pandas as pd


def main():
    path = "*.csv"
    csv_files = glob.glob(path)
    df = pd.concat(
        (
            pd.read_csv(f, encoding="latin1").assign(source_file=os.path.basename(f))
            for f in csv_files
        ),
        ignore_index=True,
    )
    df.to_parquet("merged_data.parquet", index=False)
    print(f"Merged {len(csv_files)} files into merged_data.parquet")
    import pandas as pd

    df = pd.read_parquet("merged_data.parquet")
    df["FILING_DATE"] = pd.to_datetime(df["FILING_DATE"], errors="coerce")
    df["filing_ym"] = df["FILING_DATE"].dt.to_period("M")
    report_counts = df.groupby("filing_ym").size().reset_index(name="report_count")
    print(report_counts)
    report_counts.to_csv("report_counts_by_month.csv", index=False)
    import pandas as pd

    df = pd.read_parquet("merged_data.parquet")
    df["FILING_DATE"] = pd.to_datetime(df["FILING_DATE"], errors="coerce")
    df["filing_ym"] = df["FILING_DATE"].dt.to_period("M")
    df["REPORT_SUBMISSION_TYPE"] = df["REPORT_SUBMISSION_TYPE"].fillna("UNKNOWN")
    counts = (
        df.groupby(["filing_ym", "REPORT_SUBMISSION_TYPE"])
        .size()
        .reset_index(name="count")
        .sort_values(["filing_ym", "REPORT_SUBMISSION_TYPE"])
    )
    pivot = counts.pivot_table(
        index="filing_ym",
        columns="REPORT_SUBMISSION_TYPE",
        values="count",
        fill_value=0,
        aggfunc="sum",
    )
    pivot["TOTAL"] = pivot.sum(axis=1)
    pivot = pivot.reset_index()
    print(pivot)
    import matplotlib.pyplot as plt

    df_plot = pivot.copy()
    df_plot["filing_ym"] = df_plot["filing_ym"].astype(str)
    plt.figure(figsize=(12, 6))
    plt.bar(
        df_plot["filing_ym"],
        df_plot["INITIAL"],
        label="Initial",
        color="#333333",
        alpha=0.85,
    )
    plt.bar(
        df_plot["filing_ym"],
        df_plot["SUPPLEMENTAL"],
        bottom=df_plot["INITIAL"],
        label="Supplemental",
        color="#bbbbbb",
        alpha=0.85,
    )
    plt.ylabel("Number of Reports")
    plt.xlabel("Year-Month")
    plt.xticks(rotation=90, fontsize=8)
    plt.title("Monthly Initial and Supplemental Report Counts")
    plt.legend()
    plt.tight_layout()
    plt.savefig("initial_vs_supplemental_by_month.png")
    plt.show()
    import matplotlib.pyplot as plt

    df_plot = pivot.copy()
    df_plot["filing_ym"] = df_plot["filing_ym"].astype(str)
    df_plot["filing_dt"] = pd.to_datetime(df_plot["filing_ym"])
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(
        df_plot["filing_dt"],
        df_plot["INITIAL"],
        width=25,
        label="Initial",
        color="#333333",
        alpha=0.85,
    )
    ax.bar(
        df_plot["filing_dt"],
        df_plot["SUPPLEMENTAL"],
        width=25,
        bottom=df_plot["INITIAL"],
        label="Supplemental",
        color="#bbbbbb",
        alpha=0.85,
    )
    ax.set_ylabel("Number of Reports")
    ax.set_xlabel("Year-Month")
    ax.set_title("Monthly Initial and Supplemental Report Counts")
    ax.legend()
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(axis="x")
    fig.tight_layout()
    fig.savefig("initial_vs_supplemental_by_month.png")
    plt.show()
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt

    df_plot = pivot.copy()
    df_plot["filing_dt"] = pd.to_datetime(
        df_plot["filing_ym"].astype(str), format="%Y-%m"
    )
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.bar(
        df_plot["filing_dt"],
        df_plot["INITIAL"],
        width=20,
        label="Initial",
        color="#222222",
    )
    ax.bar(
        df_plot["filing_dt"],
        df_plot["SUPPLEMENTAL"],
        width=20,
        bottom=df_plot["INITIAL"],
        label="Supplemental",
        color="#bbbbbb",
    )
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.set_ylabel("Number of Reports")
    ax.set_xlabel("Year-Month")
    ax.set_title("Monthly Initial and Supplemental Report Counts")
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    plt.xticks(rotation=90, fontsize=9)
    ax.legend()
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig("initial_vs_supplemental_by_month_full.png")
    plt.show()
    import matplotlib.pyplot as plt
    import pandas as pd

    df = pd.read_parquet("merged_data.parquet")
    df["FILING_DATE"] = pd.to_datetime(df["FILING_DATE"], errors="coerce")
    mask = (df["REPORT_SUBMISSION_TYPE"] == "INITIAL") & df[
        "FILING_DATE"
    ].dt.month.isin([2, 3])
    df_feb_mar = df[mask]
    daily_counts = df_feb_mar.groupby(df_feb_mar["FILING_DATE"].dt.date).size()
    plt.figure(figsize=(12, 6))
    daily_counts.plot(kind="bar", width=1, color="#444444")
    plt.xlabel("Filing Date")
    plt.ylabel("Number of Initial Reports")
    plt.title("Daily Filing Counts of Initial Reports (February & March)")
    plt.xticks(rotation=90, fontsize=7)
    plt.tight_layout()
    plt.savefig("initial_report_daily_hist_feb_mar.png")
    plt.show()
    import matplotlib.pyplot as plt
    import pandas as pd

    df = pd.read_parquet("merged_data.parquet")
    df["FILING_DATE"] = pd.to_datetime(df["FILING_DATE"], errors="coerce")
    df = df[df["REPORT_SUBMISSION_TYPE"] == "INITIAL"]
    mask = (
        df["FILING_DATE"].dt.month.isin([2, 3])
        & (df["FILING_DATE"].dt.day >= 1)
        & (df["FILING_DATE"].dt.day <= 31)
    )
    df = df[mask]
    df["plot_day"] = (df["FILING_DATE"].dt.month - 2) * 31 + df["FILING_DATE"].dt.day
    pivot = (
        df.groupby([df["FILING_DATE"].dt.year, "plot_day"]).size().unstack(fill_value=0)
    )
    avg_counts = pivot.mean(axis=0)
    plt.figure(figsize=(12, 6))
    for year in pivot.index:
        plt.plot(
            pivot.columns, pivot.loc[year], color="#cccccc", alpha=0.7, linewidth=1
        )
    plt.plot(pivot.columns, avg_counts, color="black", linewidth=2, label="Average")
    mar1_day = (3 - 2) * 31 + 1
    plt.axvline(mar1_day, color="red", linestyle="--", linewidth=2, label="March 1")
    tick_days = [1, 8, 15, 22, 29, mar1_day, 59]
    tick_labels = ["Feb 1", "Feb 8", "Feb 15", "Feb 22", "Feb 29", "Mar 1", "Mar 31"]
    plt.xticks(tick_days, tick_labels)
    ax.spines[["top", "right"]].set_visible(False)
    plt.ylabel("Initial Report Filings")
    plt.xlabel("Date")
    plt.title("Initial Report Filings: Feb 1–Mar 31 (All Years)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("initial_reports_feb_mar_all_years.png")
    plt.show()
    import pandas as pd

    df = pd.read_parquet("merged_data.parquet")
    df["FILING_DATE"] = pd.to_datetime(df["FILING_DATE"], errors="coerce")
    mask_initial = df["REPORT_SUBMISSION_TYPE"] == "INITIAL"
    df_initial = df[mask_initial]
    march1_15 = df_initial[
        (df_initial["FILING_DATE"].dt.month == 3)
        & (df_initial["FILING_DATE"].dt.day >= 1)
        & (df_initial["FILING_DATE"].dt.day <= 15)
    ]
    total_initial = len(df_initial)
    march1_15_count = len(march1_15)
    percent = march1_15_count / total_initial * 100 if total_initial > 0 else 0
    print(
        f"Filings between March 1–15: {march1_15_count} of {total_initial} ({percent:.1f}%)"
    )
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt

    df_plot = pivot.copy()
    df_plot["filing_dt"] = pd.to_datetime(
        df_plot["filing_ym"].astype(str), format="%Y-%m"
    )
    fig, ax = plt.subplots(figsize=(16, 6))
    ax.bar(
        df_plot["filing_dt"],
        df_plot["INITIAL"],
        width=20,
        label="Initial",
        color="#222222",
    )
    ax.bar(
        df_plot["filing_dt"],
        df_plot["SUPPLEMENTAL"],
        width=20,
        bottom=df_plot["INITIAL"],
        label="Supplemental",
        color="#bbbbbb",
    )
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    plt.xticks(rotation=45, fontsize=9)
    ax.set_ylabel("Number of Reports")
    ax.set_xlabel("Year-Month")
    ax.set_title("Monthly Initial and Supplemental Report Counts")
    ax.legend()
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig("initial_vs_supplemental_by_month_clean.png")
    plt.show()
    import matplotlib.pyplot as plt
    import pandas as pd

    df = pd.read_parquet("merged_data.parquet")
    df["FILING_DATE"] = pd.to_datetime(df["FILING_DATE"], errors="coerce")
    df = df[df["REPORT_SUBMISSION_TYPE"] == "INITIAL"]
    mask = (
        df["FILING_DATE"].dt.month.isin([2, 3])
        & (df["FILING_DATE"].dt.day >= 1)
        & (df["FILING_DATE"].dt.day <= 31)
    )
    df = df[mask]
    df["plot_day"] = (df["FILING_DATE"].dt.month - 2) * 31 + df["FILING_DATE"].dt.day
    pivot = (
        df.groupby([df["FILING_DATE"].dt.year, "plot_day"]).size().unstack(fill_value=0)
    )
    avg_counts = pivot.mean(axis=0)
    plt.figure(figsize=(12, 6))
    for year in pivot.index:
        plt.plot(
            pivot.columns, pivot.loc[year], color="#cccccc", alpha=0.7, linewidth=1
        )
    plt.plot(pivot.columns, avg_counts, color="black", linewidth=2, label="Average")
    plt.axvline(46, color="red", linestyle="--", linewidth=2, label="March 1")
    tick_days = [1, 15, 32, 46, 59]
    tick_labels = ["Feb 1", "Feb 15", "Mar 1", "Mar 15", "Mar 31"]
    plt.xticks(tick_days, tick_labels)
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.ylabel("Initial Report Filings")
    plt.xlabel("Date")
    plt.title("Initial Report Filings: Feb 1–Mar 31 (All Years)")
    plt.tight_layout()
    plt.savefig("initial_reports_feb_mar_all_years_minimal.png")
    plt.show()
    import matplotlib.pyplot as plt
    import pandas as pd

    df = pd.read_parquet("merged_data.parquet")
    df["FILING_DATE"] = pd.to_datetime(df["FILING_DATE"], errors="coerce")
    df = df[df["REPORT_SUBMISSION_TYPE"] == "INITIAL"]
    df["plot_day"] = df["FILING_DATE"].dt.dayofyear
    df["year"] = df["FILING_DATE"].dt.year
    pivot = df.groupby(["year", "plot_day"]).size().unstack(fill_value=0)
    pivot = pivot.reindex(columns=range(1, 367), fill_value=0)
    avg_counts = pivot.mean(axis=0)
    plt.figure(figsize=(14, 6))
    for year in pivot.index:
        plt.plot(
            pivot.columns, pivot.loc[year], color="#cccccc", alpha=0.7, linewidth=1
        )
    plt.plot(pivot.columns, avg_counts, color="black", linewidth=2, label="Average")
    plt.axvline(75, color="red", linestyle="--", linewidth=2, label="March 1")
    month_starts = pd.date_range("2020-01-01", "2020-12-31", freq="MS")
    tick_days = [d.timetuple().tm_yday for d in month_starts]
    tick_labels = [d.strftime("%b") for d in month_starts]
    plt.xticks(tick_days, tick_labels)
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.ylabel("Initial Report Filings")
    plt.xlabel("Month")
    plt.title("Initial Report Filings by Calendar Month (2017-2025) Average in bold")
    plt.tight_layout()
    plt.savefig("initial_reports_by_month_all_years.png")
    plt.show()


def main() -> None:
    main()


if __name__ == "__main__":
    main()
