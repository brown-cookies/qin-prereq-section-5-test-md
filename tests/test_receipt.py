import pytest
from receipt import billable_units, line_cost_pence, discount_pence, total_pence, format_pence


@pytest.mark.parametrize("weight_kg, expected", [
    (25, 1),
    (30, 2),
    (50, 2),
    (60, 3),
    (75, 3),
    (90, 4),
    (100, 4),
])
def test_billable_units_returns_rounds_up(weight_kg, expected):
    result = billable_units(weight_kg)

    assert result == expected


@pytest.mark.parametrize("weight_kg", [0, -10, -50, -100, -99999])
def test_billable_units_should_raise_error(weight_kg):
    with pytest.raises(ValueError):
        billable_units(weight_kg)


@pytest.mark.parametrize("weight_kg, expected", [
    (25, 275),
    (30, 550),
    (50, 550),
    (60, 825),
    (75, 825),
    (90, 1100),
    (100, 1100),
])
def test_cost_pence_with_loose(weight_kg, expected):
    result = line_cost_pence("loose", weight_kg)

    assert result == expected


@pytest.mark.parametrize("weight_kg, expected", [
    (25, 425),
    (30, 700),
    (50, 700),
    (60, 975),
    (75, 975),
    (90, 1250),
    (100, 1250),
])
def test_cost_pence_with_crate(weight_kg, expected):
    result = line_cost_pence("crated", weight_kg)

    assert result == expected


def test_discount_pence_no_discount_under_a_threshold():
    random_subtotal = 1000
    row_count = 9

    result = discount_pence(random_subtotal, row_count)

    assert result == 0


@pytest.mark.parametrize("subtotal, expected", [
    (150, 7),
    (400, 20),
    (550, 27),
    (800, 40),
    (950, 47),
])
def test_discount_pence_returns_discounted_value_from_subtotal(subtotal, expected):
    result = discount_pence(subtotal, 10)

    assert result == expected


def test_total_pence_with_discount_applied(manifest_long):
    result = total_pence(manifest_long)

    assert result == 20069


def test_total_pence_with_no_discount_applied(manifest_short):
    result = total_pence(manifest_short)

    assert result == 12975


# @pytest.mark.parametrize("pence", [121050, 554134, 6743452, 1240063, 23959745, 2467942, 22306467])
def test_format_pence_properly_converting_pence_to_pounds():
    pence = 2512312
    pound = "25123.12"

    result = format_pence(pence)

    assert pound == result


@pytest.mark.parametrize("pence", [-1, -125.7, -99.34])
def test_format_pence_when_pence_is_less_than_zero(pence):
    assert format_pence(pence).startswith("-")


def test_format_pence_when_zero():
    assert "0.00" == format_pence(0)
