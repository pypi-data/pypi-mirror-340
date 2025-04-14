from maphrs.statistics.descriptive import sqrt, standard_deviation


def uncertainty_a(values: list[int | float]):
    std = standard_deviation(values)
    return std / sqrt(len(values))


def uncertainty_c(values: list[int | float], instrument_uncertainty: float):
    return sqrt(uncertainty_a(values) ** 2 + instrument_uncertainty ** 2)
