from dataclasses import dataclass


@dataclass
class GeneObservation:
    """Single observation of a gene's frequency at a given time index."""
    time_index: int
    phase: str
    gene: str
    frequency: float


@dataclass
class ForecastResult:
    """Simple forecast output for a single gene and horizon."""
    gene: str
    horizon: int
    forecast: float
