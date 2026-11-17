"""Small input-safe helpers for the Lab 7 loan eligibility fuzzing exercise."""

from math import isfinite
import re

CATEGORIES = {"P": "Individual", "C": "Company", "H": "HUF", "F": "Firm"}


def parse_income(income):
    """Parse a non-negative integer income, allowing correctly grouped commas.

    Invalid or unsupported inputs return None so callers can handle fuzzed data
    without an uncaught conversion exception.
    """
    if not isinstance(income, str):
        return None
    value = income.strip()
    if not re.fullmatch(r"(?:\d+|\d{1,3}(?:,\d{3})+)", value):
        return None
    return int(value.replace(",", ""))


def monthly_emi(details):
    """Return monthly EMI for ``principal,annual_rate_percent,years`` or None."""
    if not isinstance(details, str):
        return None
    parts = details.split(",")
    if len(parts) != 3:
        return None
    try:
        principal, annual_rate, years = (float(part.strip()) for part in parts)
    except (TypeError, ValueError, OverflowError):
        return None
    if not all(isfinite(v) for v in (principal, annual_rate, years)):
        return None
    if principal <= 0 or annual_rate < 0 or years <= 0:
        return None
    try:
        months = int(years * 12)
    except (OverflowError, ValueError):
        return None
    if months <= 0 or months != years * 12:
        return None
    if annual_rate == 0:
        return round(principal / months, 2)
    rate = annual_rate / 1200
    try:
        factor = (1 + rate) ** months
        amount = principal * rate * factor / (factor - 1)
        return round(amount, 2) if isfinite(amount) else None
    except (OverflowError, ZeroDivisionError):
        return None


def pan_category(pan):
    """Return the category for a structurally valid PAN, otherwise None."""
    if not isinstance(pan, str):
        return None
    normalized = pan.strip().upper()
    if not re.fullmatch(r"[A-Z]{5}[0-9]{4}[A-Z]", normalized):
        return None
    return CATEGORIES.get(normalized[3])


def main():
    print("==== Running parse_income ====")
    result = parse_income(input("Enter monthly income (e.g. 50,000): "))
    print("Income:", result if result is not None else "Invalid income")

    print("\n==== Running monthly_emi ====")
    result = monthly_emi(input("Enter principal,rate,years (e.g. 500000,10,5): "))
    print("Monthly EMI:", result if result is not None else "Invalid loan details")

    print("\n==== Running pan_category ====")
    result = pan_category(input("Enter a PAN number (e.g. ABCPE1234F): "))
    print("PAN Category:", result if result is not None else "Invalid PAN")


if __name__ == "__main__":
    main()
