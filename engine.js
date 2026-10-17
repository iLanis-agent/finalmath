// Final Math engine - weighted grade arithmetic from numbers the owner enters.
// Mirrored by oracle.py; keep the op order identical.

function _num(x) {
  return String(x);
}

function _tenths(x) {
  var t = Math.floor(x * 10 + 0.5);
  return Math.floor(t / 10) + "." + (t % 10);
}

function _cats(scores, weights) {
  var sumsw = 0, w = 0;
  for (var i = 0; i < scores.length; i++) {
    if (!isFinite(scores[i]) || scores[i] < 0 || scores[i] > 200) throw new Error("scores must be between 0 and 200");
    if (!isFinite(weights[i]) || weights[i] < 0) throw new Error("weights must be 0 or more");
    sumsw = sumsw + scores[i] * weights[i];
    w = w + weights[i];
  }
  if (w <= 0) throw new Error("enter a weight over 0 for at least one graded item");
  return { sumsw: sumsw, w: w };
}

// The weighted truth: what the graded items count for so far.
function weightedTruth(scores, weights) {
  var c = _cats(scores, weights);
  return "Counted so far: " + _tenths(c.sumsw / 100) + " points of 100, over " + _num(c.w) +
    "% of the grade, an average of " + _tenths(c.sumsw / c.w) + "% on what is graded.";
}

// The needed truth: the final score that lands on the target.
function neededTruth(scores, weights, finalWeight, target) {
  var c = _cats(scores, weights);
  if (!isFinite(finalWeight) || finalWeight <= 0) throw new Error("final weight must be over 0");
  if (!isFinite(target) || target < 0 || target > 100) throw new Error("target must be between 0 and 100");
  var total = c.w + finalWeight;
  if (Math.abs(total - 100) > 1e-9) throw new Error("weights must add up to 100, they add up to " + _num(total));
  var need = (target * 100 - c.sumsw) / finalWeight;
  var lead = "To finish at " + _num(target) + "%, ";
  if (need > 100) return lead + "the final would need " + _tenths(need) + "%, which is above 100%.";
  if (need <= 0) return lead + "the final would need 0% or less: the target is already met before the final.";
  return lead + "the final (" + _num(finalWeight) + "% of the grade) needs " + _tenths(need) + "%.";
}

// The drop truth: average with the lowest scores dropped, per a rule the owner names.
function dropTruth(scores, drop) {
  var n = scores.length;
  if (n < 2) throw new Error("enter at least 2 scores");
  var all = 0;
  for (var i = 0; i < n; i++) {
    if (!isFinite(scores[i]) || scores[i] < 0 || scores[i] > 200) throw new Error("scores must be between 0 and 200");
    all = all + scores[i];
  }
  if (!isFinite(drop) || drop % 1 !== 0 || drop < 0) throw new Error("drop count must be a whole number, 0 or more");
  if (drop >= n) throw new Error("drop count must be less than the number of scores");
  var sorted = scores.slice().sort(function (a, b) { return a - b; });
  var kept = 0;
  for (var j = drop; j < n; j++) kept = kept + sorted[j];
  var avgAll = _tenths(all / n);
  if (drop === 0) return n + " scores, none dropped: average " + avgAll + "%.";
  return n + " scores, lowest " + drop + " dropped: average " + _tenths(kept / (n - drop)) + "% instead of " + avgAll + "%.";
}
