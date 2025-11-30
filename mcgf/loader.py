import csv
from typing import Dict, List
from .models import GeneObservation


def load_observations(path: str) -> List[GeneObservation]:
    """Load gene observations from a CSV file.

    Expected columns:
      - time_index
      - phase
      - gene
      - frequency
    """
    observations: List[GeneObservation] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            gene = row.get("gene")
            if not gene:
                continue
            try:
                t = int(row["time_index"])
                freq = float(row["frequency"])
            except (KeyError, ValueError):
                continue
            phase = (row.get("phase") or "").strip()
            observations.append(
                GeneObservation(
                    time_index=t,
                    phase=phase,
                    gene=gene.strip(),
                    frequency=freq,
                )
            )
    return observations


def group_by_gene(observations: List[GeneObservation]) -> Dict[str, List[GeneObservation]]:
    """Group observations into time series by gene key."""
    by_gene: Dict[str, List[GeneObservation]] = {}
    for ob in observations:
        by_gene.setdefault(ob.gene, []).append(ob)
    # sort each gene series by time index
    for key, series in by_gene.items():
        series.sort(key=lambda o: o.time_index)
    return by_gene
