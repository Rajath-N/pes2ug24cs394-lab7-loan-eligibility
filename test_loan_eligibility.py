"""Property-based fuzz coverage for malformed and valid loan inputs."""

from hypothesis import given, strategies as st

from loan_eligibility import CATEGORIES, monthly_emi, pan_category, parse_income


@given(st.one_of(st.text(), st.none(), st.integers(), st.floats(allow_nan=True, allow_infinity=True)))
def test_parse_income_fuzz_does_not_crash(value):
    result = parse_income(value)
    assert result is None or (isinstance(result, int) and result >= 0)


@given(st.integers(min_value=0, max_value=10**12))
def test_parse_income_accepts_valid_plain_integer(value):
    assert parse_income(str(value)) == value


@given(st.integers(min_value=0, max_value=10**12))
def test_parse_income_accepts_valid_comma_grouping(value):
    assert parse_income(f"{value:,}") == value


@given(st.one_of(st.text(), st.none(), st.integers(), st.floats(allow_nan=True, allow_infinity=True)))
def test_monthly_emi_fuzz_does_not_crash(value):
    result = monthly_emi(value)
    assert result is None or (isinstance(result, float) and result >= 0)


@given(
    st.integers(min_value=1, max_value=10**9),
    st.integers(min_value=0, max_value=100),
    st.integers(min_value=1, max_value=50),
)
def test_monthly_emi_accepts_valid_loan_terms(principal, annual_rate, years):
    result = monthly_emi(f"{principal},{annual_rate},{years}")
    assert isinstance(result, float)
    assert result >= 0


@given(st.one_of(st.text(), st.none(), st.integers(), st.floats(allow_nan=True, allow_infinity=True)))
def test_pan_category_fuzz_does_not_crash(value):
    result = pan_category(value)
    assert result is None or result in CATEGORIES.values()


@given(st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=3, max_size=3),
       st.sampled_from(list(CATEGORIES)), st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=1, max_size=1),
       st.text(alphabet="0123456789", min_size=4, max_size=4), st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=1, max_size=1))
def test_pan_category_maps_valid_pan_category(prefix, category, fifth_letter, digits, suffix):
    assert pan_category(prefix + category + fifth_letter + digits + suffix) == CATEGORIES[category]
