import argparse
from .loader import load_observations, group_by_gene
from .forecasting import moving_average_forecast, trend_forecast

LINE = "─" * 60


def fmt(x: float) -> str:
    return f"{x:.3f}"


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="mcgf",
        description="Market Cycle Gene Forecasting Engine – forecast tokenomic gene frequencies over time.",
    )

    parser.add_argument("csv", help="Path to CSV file of historical gene observations.")
    parser.add_argument("--gene", help="Limit forecast to a single gene (optional).")
    parser.add_argument(
        "--horizon",
        type=int,
        default=1,
        help="Forecast horizon (steps ahead). Default: 1",
    )
    parser.add_argument(
        "--method",
        choices=["ma", "trend"],
        default="trend",
        help="Forecast method: moving-average or trend. Default: trend",
    )
    parser.add_argument(
        "--window",
        type=int,
        default=3,
        help="Moving-average window (only used with --method ma).",
    )

    args = parser.parse_args()

    # Load CSV
    observations = load_observations(args.csv)
    if not observations:
        print("No observations found in:", args.csv)
        return

    by_gene = group_by_gene(observations)
    target_genes = [args.gene] if args.gene else sorted(by_gene.keys())

    # HEADER
    print(LINE)
    print(f" MARKET CYCLE GENE FORECAST – {args.horizon} STEP AHEAD  (method: {args.method})")
    print(LINE)
    print(f"\nTotal observations : {len(observations)}")
    print(f"Total genes        : {len(by_gene)}\n")

    # TABLE HEADER
    print(f"{'Gene':30} {'Last Freq':>12} {'Forecast(+{})'.format(args.horizon):>15}")
    print(LINE)

    # PROCESS EACH GENE
    for g in target_genes:
        series = by_gene.get(g)
        if not series:
            continue

        if args.method == "ma":
            res = moving_average_forecast(series, horizon=args.horizon, window=args.window)
        else:
            res = trend_forecast(series, horizon=args.horizon)

        last = series[-1]

        print(
            f"{g:30} {fmt(last.frequency):>12} {fmt(res.forecast):>15}"
        )

    print(LINE)
    print("\nDone.\n")
