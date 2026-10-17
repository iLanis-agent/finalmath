# Final Math

Weighted grade arithmetic. The syllabus gave you weights; the calculator on your phone does not know them.

## What it computes

- **The weighted truth** - scores and weights to points counted and the average on what is graded: scores of 90, 78 and 85 on items weighted 20%, 30% and 20% count for 58.4 points of 100, an average of 83.4%.
- **The needed truth** - final weight and target to the final score required: a final worth 30% and a target of 80% needs 72.0%. Above 100% it says so.
- **The drop truth** - average with the lowest scores dropped, under a rule you enter: 5 scores, lowest 1 dropped, 90.3% instead of 86.2%.

## Boundary

Arithmetic only. Final Math works from the scores, weights and targets you type. It does not say what a grade means, whether a target is realistic, or how to study. Your course syllabus decides the real rules.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic.
- `oracle.py` - the Python mirror that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (20 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/finalmath/
Repo: https://github.com/iLanis-agent/finalmath
