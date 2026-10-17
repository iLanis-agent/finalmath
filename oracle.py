#!/usr/bin/env python3
# Final Math oracle - mirrors engine.js.
import json, math

def _num(x):
    return str(int(x)) if x == int(x) else repr(x)

def _tenths(x):
    t = math.floor(x * 10 + 0.5)
    return f"{t // 10}.{t % 10}"

def _cats(scores, weights):
    sumsw = 0
    w = 0
    for s, wt in zip(scores, weights):
        if not math.isfinite(s) or s < 0 or s > 200:
            raise ValueError("scores must be between 0 and 200")
        if not math.isfinite(wt) or wt < 0:
            raise ValueError("weights must be 0 or more")
        sumsw = sumsw + s * wt
        w = w + wt
    if w <= 0:
        raise ValueError("enter a weight over 0 for at least one graded item")
    return sumsw, w

def weighted_truth(scores, weights):
    sumsw, w = _cats(scores, weights)
    return (f"Counted so far: {_tenths(sumsw / 100)} points of 100, over {_num(w)}% of the grade, "
            f"an average of {_tenths(sumsw / w)}% on what is graded.")

def needed_truth(scores, weights, final_weight, target):
    sumsw, w = _cats(scores, weights)
    if not math.isfinite(final_weight) or final_weight <= 0:
        raise ValueError("final weight must be over 0")
    if not math.isfinite(target) or target < 0 or target > 100:
        raise ValueError("target must be between 0 and 100")
    total = w + final_weight
    if abs(total - 100) > 1e-9:
        raise ValueError(f"weights must add up to 100, they add up to {_num(total)}")
    need = (target * 100 - sumsw) / final_weight
    lead = f"To finish at {_num(target)}%, "
    if need > 100:
        return lead + f"the final would need {_tenths(need)}%, which is above 100%."
    if need <= 0:
        return lead + "the final would need 0% or less: the target is already met before the final."
    return lead + f"the final ({_num(final_weight)}% of the grade) needs {_tenths(need)}%."

def drop_truth(scores, drop):
    n = len(scores)
    if n < 2:
        raise ValueError("enter at least 2 scores")
    all_ = 0
    for s in scores:
        if not math.isfinite(s) or s < 0 or s > 200:
            raise ValueError("scores must be between 0 and 200")
        all_ = all_ + s
    if not math.isfinite(drop) or drop % 1 != 0 or drop < 0:
        raise ValueError("drop count must be a whole number, 0 or more")
    if drop >= n:
        raise ValueError("drop count must be less than the number of scores")
    srt = sorted(scores)
    kept = 0
    for j in range(int(drop), n):
        kept = kept + srt[j]
    avg_all = _tenths(all_ / n)
    d = int(drop)
    if d == 0:
        return f"{n} scores, none dropped: average {avg_all}%."
    return f"{n} scores, lowest {d} dropped: average {_tenths(kept / (n - d))}% instead of {avg_all}%."

FNS = {"weightedTruth": weighted_truth, "neededTruth": needed_truth, "dropTruth": drop_truth}

CASES = [
    ("weightedTruth", [[90, 78, 85], [20, 30, 20]]),
    ("weightedTruth", [[100, 100, 100], [10, 10, 10]]),
    ("weightedTruth", [[70, 0, 0], [50, 0, 0]]),
    ("weightedTruth", [[90, 78, 85], [0, 0, 0]]),
    ("weightedTruth", [[90, 78, 250], [20, 30, 20]]),
    ("weightedTruth", [[90, 78, 85], [20, -1, 20]]),
    ("neededTruth", [[90, 78, 85], [20, 30, 20], 30, 80]),
    ("neededTruth", [[90, 78, 85], [20, 30, 20], 30, 95]),
    ("neededTruth", [[95, 95, 95], [20, 30, 20], 30, 70]),
    ("neededTruth", [[90, 78, 85], [20, 30, 20], 20, 80]),
    ("neededTruth", [[90, 78, 85], [20, 30, 20], 0, 80]),
    ("neededTruth", [[90, 78, 85], [20, 30, 20], 30, 101]),
    ("neededTruth", [[90, 78, 85], [20, 30, 20], 30, 72.5]),
    ("dropTruth", [[92, 85, 70, 96, 88], 1]),
    ("dropTruth", [[92, 85, 70, 96, 88], 0]),
    ("dropTruth", [[92, 85, 70, 96, 88], 2]),
    ("dropTruth", [[92, 85, 70, 96, 88], 5]),
    ("dropTruth", [[92, 85, 70, 96, 88], 1.5]),
    ("dropTruth", [[92], 0]),
    ("dropTruth", [[50, 100], 1]),
]

out = []
for fn, args in CASES:
    try:
        exp = FNS[fn](*args)
    except ValueError as e:
        exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(len(out), "cases")
