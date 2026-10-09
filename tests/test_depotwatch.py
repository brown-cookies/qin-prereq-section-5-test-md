import pytest
import requests
from depotwatch import fetch_shipments, heavy_shipments, unweighed


@pytest.mark.parametrize("weight, threshold, is_included", [
    (50, 10, True),
    (100, 150, False),
    (999, 150, True),
    (75, 50, True),
    (20, 10, True),
    (11, 10, True),
    (100, 100, True),
    (320, 500, False),
    (10, 1, True),
    (40, 39, True),
])
def test_shipment_above_or_equal_to_threshold_is_included(weight, threshold, is_included):
    shipment = {"id": 1,
                "destination": "x",
                "packing": "loose",
                "weight_kg": weight
                }
    result = heavy_shipments([shipment], threshold)
    included = any(s["id"] == 1 for s in result)
    assert included == is_included


@pytest.mark.parametrize("weight, threshold, is_excluded", [
    (50, 10, False),
    (100, 150, True),
    (999, 150, False),
    (75, 50, False),
    (20, 10, False),
    (50, 10, False),
    (100, 100, False),
    (320, 500, True),
    (10, 1, False),
    (40, 39, False),
])
def test_shipment_below_the_threshold_is_excluded(weight, threshold, is_excluded):
    shipment = {"id": 1,
                "destination": "x",
                "packing": "loose",
                "weight_kg": weight
                }
    result = heavy_shipments([shipment], threshold)
    excluded = not any(s["id"] == 1 for s in result)
    assert excluded == is_excluded


@pytest.mark.parametrize("weight, threshold, is_excluded", [
    (0, 10, True),
])
def test_shipment_with_no_weight_is_should_be_excluded(weight, threshold, is_excluded):
    shipment = {"id": 1,
                "destination": "x",
                "packing": "loose",
                "weight_kg": weight
                }
    result = heavy_shipments([shipment], threshold)
    excluded = not any(s["id"] == 1 for s in result)
    assert excluded == is_excluded


# def test_shipment_should_not_have_negative_weight(shipments):
#     for s in shipments:
#         assert s["weight_kg"] > 0


def test_empty_shipments_returns_empty_list():
    assert heavy_shipments([], threshold_kg=100) == []


def test_shipment_qualify_count(shipments):
    result = heavy_shipments(shipments, threshold_kg=100)
    assert len(result) == 8


def test_shipment_not_qualified(no_qualified_shipments):
    result = heavy_shipments(no_qualified_shipments, threshold_kg=100)
    assert len(result) == 0


def test_shipment_sort(qualified_shipments, sorted_qualified_shipments):
    result = heavy_shipments(qualified_shipments, threshold_kg=100)
    assert result == sorted_qualified_shipments


def test_unweighed_return_id_of_non_int_float(shipments):
    result = unweighed(shipments)
    assert result == [8, 10, 17, 18, 19, 21, 24]


# -- Mocking --
def test_fetch_returns_json(monkeypatch, shipments):
    class FakeResponse():
        def raise_for_status(self):
            ...

        def json(self):
            return shipments

    def fake_get(url, timeout):
        return FakeResponse()

    monkeypatch.setattr(requests, "get", fake_get)

    result = fetch_shipments()
    assert isinstance(result, list)


def test_fetch_should_raise_http_error(monkeypatch):
    class FakeResponse():
        def raise_for_status(self):
            raise requests.HTTPError("500")

    def fake_get(url, timeout):
        return FakeResponse()

    monkeypatch.setattr(requests, "get", fake_get)

    with pytest.raises(requests.HTTPError):
        fetch_shipments()


def test_fetch_should_raise_request_exception_error(monkeypatch):
    class FakeResponse():
        def raise_for_status(self):
            raise requests.RequestException("Connection Error")

    def fake_get(url, timeout):
        return FakeResponse()

    monkeypatch.setattr(requests, "get", fake_get)

    with pytest.raises(requests.RequestException):
        fetch_shipments()
