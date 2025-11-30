from typing import List
from .models import GeneObservation, ForecastResult


def moving_average_forecast(
    series: List[GeneObservation],
    horizon: int = 1,
    window: int = 3,
) -> ForecastResult:
    """Simple moving-average forecast of the last `window` points.

    We don't explicitly model multiple steps; the moving average is treated
    as the expected next frequency at the given horizon.
    """
    if not series:
        raise ValueError("Cannot forecast empty series")

    if window <= 0:
        window = 1

    tail = series[-window:]
    freqs = [o.frequency for o in tail]
    avg = sum(freqs) / len(freqs)
    gene = series[0].gene
    return ForecastResult(gene=gene, horizon=horizon, forecast=avg)


def trend_forecast(
    series: List[GeneObservation],
    horizon: int = 1,
) -> ForecastResult:
    """Fit a simple linear trend and extrapolate by `horizon` steps.

    Uses ordinary least squares for y = a + b * t,
    where t = time_index and y = frequency.
    """
    if not series:
        raise ValueError("Cannot forecast empty series")

    if len(series) == 1:
        # No trend information, fall back to current frequency.
        gene = series[0].gene
        return ForecastResult(gene=gene, horizon=horizon, forecast=series[0].frequency)

    x = [o.time_index for o in series]
    y = [o.frequency for o in series]
    n = len(x)

    sum_x = sum(x)
    sum_y = sum(y)
    sum_xx = sum(v * v for v in x)
    sum_xy = sum(x[i] * y[i] for i in range(n))

    denom = n * sum_xx - sum_x * sum_x
    gene = series[0].gene

    if denom == 0:
        # Degenerate case: no variation in time; fallback to moving average.
        return moving_average_forecast(series, horizon=horizon, window=min(3, len(series)))

    b = (n * sum_xy - sum_x * sum_y) / denom
    a = (sum_y - b * sum_x) / n

    last_t = x[-1]
    t_future = last_t + horizon
    y_future = a + b * t_future

    return ForecastResult(gene=gene, horizon=horizon, forecast=y_future)
