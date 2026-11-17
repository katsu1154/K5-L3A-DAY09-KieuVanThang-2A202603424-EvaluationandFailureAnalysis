"""Statistics students implement (M2 judge calibration, M4 paired bootstrap).

Rules: a judge is a classifier -- measure it like one. A higher mean is not
"better" until the paired CI of the difference excludes 0.
Reference values to self-check are in tests/test_lab9_stats.py.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

POS = "FAIL"   # the judge's job is to FIND failures, so FAIL is the positive class


def _aligned_labels(human: Sequence[str], judge: Sequence[str]) -> tuple[list[str], list[str]]:
    if len(human) != len(judge):
        raise ValueError("human and judge labels must have the same length")
    allowed = {"PASS", POS}
    human_labels = [str(label).strip().upper() for label in human]
    judge_labels = [str(label).strip().upper() for label in judge]
    invalid = sorted((set(human_labels) | set(judge_labels)) - allowed)
    if invalid:
        raise ValueError(f"labels must be PASS or FAIL; got {invalid}")
    return human_labels, judge_labels


def confusion(human: Sequence[str], judge: Sequence[str]) -> dict[str, int]:
    """tp/fp/fn/tn with FAIL as positive."""
    human_labels, judge_labels = _aligned_labels(human, judge)
    return {
        "tp": sum(h == POS and j == POS for h, j in zip(human_labels, judge_labels)),
        "fp": sum(h != POS and j == POS for h, j in zip(human_labels, judge_labels)),
        "fn": sum(h == POS and j != POS for h, j in zip(human_labels, judge_labels)),
        "tn": sum(h != POS and j != POS for h, j in zip(human_labels, judge_labels)),
    }


def precision_recall(human: Sequence[str], judge: Sequence[str]) -> tuple[float, float]:
    cm = confusion(human, judge)
    precision_denominator = cm["tp"] + cm["fp"]
    recall_denominator = cm["tp"] + cm["fn"]
    precision = cm["tp"] / precision_denominator if precision_denominator else 0.0
    recall = cm["tp"] / recall_denominator if recall_denominator else 0.0
    return precision, recall


def cohen_kappa(human: Sequence[str], judge: Sequence[str]) -> float:
    """kappa = (p_o - p_e) / (1 - p_e). Raise ValueError when undefined (p_e == 1):
    a constant judge has no signal and must FAIL calibration, not pass on a technicality."""
    human_labels, judge_labels = _aligned_labels(human, judge)
    n = len(human_labels)
    if not n:
        raise ValueError("kappa is undefined for an empty label set")

    cm = confusion(human_labels, judge_labels)
    observed_agreement = (cm["tp"] + cm["tn"]) / n
    human_fail_rate = (cm["tp"] + cm["fn"]) / n
    judge_fail_rate = (cm["tp"] + cm["fp"]) / n
    expected_agreement = (
        human_fail_rate * judge_fail_rate
        + (1 - human_fail_rate) * (1 - judge_fail_rate)
    )
    denominator = 1 - expected_agreement
    if math.isclose(denominator, 0.0, abs_tol=1e-12):
        raise ValueError("kappa is undefined when expected agreement is 1")
    return (observed_agreement - expected_agreement) / denominator


def rogan_gladen(observed_rate: float, sensitivity: float, specificity: float) -> float:
    """Correct an observed failure rate for judge error; clip to [0, 1]."""
    values = (observed_rate, sensitivity, specificity)
    if any(not math.isfinite(value) or not 0 <= value <= 1 for value in values):
        raise ValueError("observed rate, sensitivity, and specificity must be in [0, 1]")
    denominator = sensitivity + specificity - 1
    if math.isclose(denominator, 0.0, abs_tol=1e-12):
        raise ValueError("Rogan-Gladen correction is undefined when sensitivity + specificity = 1")
    corrected = (observed_rate + specificity - 1) / denominator
    return min(1.0, max(0.0, corrected))


def paired_bootstrap(a: Sequence[float], b: Sequence[float], *, n_resamples: int = 1000,
                     rng: int = 2027, confidence: float = 0.95) -> tuple[float, float, float]:
    """a[i], b[i] = per-item mean over seeds, SAME items, SAME order.
    Return (mean(a)-mean(b), lo, hi) with scipy.stats.bootstrap(paired=True, method="percentile",
    rng=numpy.random.default_rng(rng)). If a == b everywhere return (0.0, 0.0, 0.0)."""
    import numpy as np
    from scipy import stats as scipy_stats

    sample_a = np.asarray(a, dtype=float)
    sample_b = np.asarray(b, dtype=float)
    if sample_a.ndim != 1 or sample_b.ndim != 1:
        raise ValueError("paired bootstrap inputs must be one-dimensional")
    if sample_a.size != sample_b.size:
        raise ValueError("paired bootstrap inputs must have the same length")
    if sample_a.size == 0:
        raise ValueError("paired bootstrap requires at least one pair")
    if not np.isfinite(sample_a).all() or not np.isfinite(sample_b).all():
        raise ValueError("paired bootstrap inputs must contain only finite values")
    if not isinstance(n_resamples, int) or n_resamples < 1:
        raise ValueError("n_resamples must be a positive integer")
    if not math.isfinite(confidence) or not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1")
    if np.array_equal(sample_a, sample_b):
        return 0.0, 0.0, 0.0

    difference = float(np.mean(sample_a - sample_b))
    result = scipy_stats.bootstrap(
        (sample_a, sample_b),
        lambda values_a, values_b: np.mean(values_a - values_b),
        paired=True,
        vectorized=False,
        n_resamples=n_resamples,
        confidence_level=confidence,
        method="percentile",
        rng=np.random.default_rng(rng),
    )
    return difference, float(result.confidence_interval.low), float(result.confidence_interval.high)


def pass_at_k(n: int, c: int, k: int) -> float:
    """Probability that AT LEAST ONE of k trials drawn from n (c of them passing) passes.
    Unbiased estimator (Chen et al. 2021): 1 - C(n-c, k) / C(n, k). Raise ValueError if k > n."""
    # TODO M6
    raise NotImplementedError


def pass_hat_k(n: int, c: int, k: int) -> float:
    """pass^k (tau-bench, Yao et al. 2024): probability that ALL k trials drawn from n pass.
    Unbiased estimator: C(c, k) / C(n, k). Raise ValueError if k > n.
    pass^k <= pass@1 <= pass@k; a reliable agent keeps pass^k close to pass@1."""
    # TODO M6
    raise NotImplementedError
