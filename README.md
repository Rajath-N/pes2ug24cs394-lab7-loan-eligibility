# Lab 7 - Loan Eligibility Fuzz Testing

Student: **PES2UG24CS394 - Rajath N Gonda**

This lab uses Hypothesis property-based tests to fuzz three loan utility
functions: income parsing, monthly EMI calculation, and PAN category lookup.
The starter functions were fragile for malformed values. They now return
`None` for unsupported or invalid input, while preserving results for valid
inputs.

## Files

| File | Description |
|------|-------------|
| `loan_eligibility.py` | Input-safe implementations of the three functions |
| `test_loan_eligibility.py` | Hypothesis fuzz and valid-input properties |

## Run

From this directory, install the test dependencies and run pytest:

```sh
python -m pip install -r requirements.txt
python -m pytest -v
```

The repository supplied a short README but no separate lab handout. The
implementation and tests follow the README's Lab 7 fuzz-testing description.
