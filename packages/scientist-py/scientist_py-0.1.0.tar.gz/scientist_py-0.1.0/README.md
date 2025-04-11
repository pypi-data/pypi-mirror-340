# Scientist-Py

A lightweight, async-compatible Python port of GitHub's [Scientist](https://github.com/github/scientist) for testing candidate code paths against a control in production without affecting users.

## Features
- 🧪 Run control and candidate functions safely
- ⏱️ Measure execution time of each path
- ⚠️ Compare results and log mismatches
- ✅ Support for `async` functions
- 🎯 Sampling to control experiment frequency
- 🛡️ Ignore known exceptions
- 📊 Metric logging out-of-the-box

### What are Control and Candidate in Scientist?
    Control = The current, trusted, production logic.

    Candidate = The new or experimental logic you're testing against the control.

### Why use this?
It’s the safest way to test new implementations without breaking stuff. You can:

    Rewrite a function (e.g., old regex → new parser)

    Replace a service call (e.g., REST → GraphQL)

    Try a new algorithm or optimization

All while continuing to serve the real user with the proven control.

---

## Installation

Simply copy the `Experiment` class into your project. No external dependencies required.

---


## Usage

### Basic Example
```python
from experiment import Experiment

exp = Experiment("add-function")

@exp.control
def control():
    return 2 + 2

@exp.candidate
def candidate():
    return 2 + 2  # or some experimental logic

result = await exp.run()
```

### With `async` functions
```python
@exp.control
async def control():
    await asyncio.sleep(0.1)
    return 2 + 2

@exp.candidate
async def candidate():
    await asyncio.sleep(0.1)
    return 4
```

### Add a custom comparator
```python
exp.compare_with(lambda a, b: round(a, 2) == round(b, 2))
```

### Ignore known exceptions
```python
exp.ignore_exceptions(ValueError)
```

### Enable sampling (e.g. 10% of the time)
```python
exp.sample(0.1)
```

---

## Logging Output
When a mismatch is found, logs look like:
```
[Experiment: add-function] Mismatch detected!
 - Control result: 4
 - Candidate result: 5
[Experiment: add-function] Metrics:
 - Control duration: 0.000120 sec
 - Candidate duration: 0.000150 sec
 - Match: False
```

---

## License
MIT (or adapt as needed for internal tools)

---

## Inspired By
- [GitHub Scientist](https://github.com/github/scientist)
- [Scientist Ruby](https://github.com/github/scientist/blob/main/docs/scientist/README.md)

---

## TODO
- Persistent result storage (e.g., file/DB)
- Dashboard or reporting
- Integration with Prometheus or StatsD

