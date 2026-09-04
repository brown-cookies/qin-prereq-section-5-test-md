import copy
import pytest


# Depotwatch
BASE_SHIPMENTS = [
    {"id": 1,  "destination": "north", "packing": "crated", "weight_kg": 120},
    {"id": 2,  "destination": "south", "packing": "loose",  "weight_kg": 40},
    {"id": 3,  "destination": "east",  "packing": "crated", "weight_kg": 310},
    {"id": 4,  "destination": "west",  "packing": "crated", "weight_kg": 5},
    {"id": 5,  "destination": "north", "packing": "loose",  "weight_kg": 75},
    {"id": 6,  "destination": "south", "packing": "crated", "weight_kg": 210},
    {"id": 7,  "destination": "east",  "packing": "loose",  "weight_kg": 33},
    {"id": 8,  "destination": "west",  "packing": "crated", "weight_kg": "42"},
    {"id": 9,  "destination": "north", "packing": "crated", "weight_kg": 150},
    {"id": 10, "destination": "south", "packing": "loose",  "weight_kg": None},
    {"id": 11, "destination": "east",  "packing": "crated", "weight_kg": 60},
    {"id": 12, "destination": "south", "packing": "loose",  "weight_kg": -50},
    {"id": 13, "destination": "north", "packing": "crated", "weight_kg": 275},
    {"id": 14, "destination": "south", "packing": "crated", "weight_kg": 18},
    {"id": 15, "destination": "east",  "packing": "loose",  "weight_kg": 0},
    {"id": 16, "destination": "west",  "packing": "crated", "weight_kg": 99.5},
    {"id": 17, "destination": "north", "packing": "crated", "weight_kg": None},
    {"id": 18, "destination": "south", "packing": "loose",  "weight_kg": None},
    {"id": 19, "destination": "east",  "packing": "crated"},
    {"id": 20, "destination": "west",  "packing": "crated", "weight_kg": 9999},
    {"id": 21,  "destination": "south", "packing": "crated", "weight_kg": True},
    {"id": 22,  "destination": "east",  "packing": "loose",  "weight_kg": 33},
    {"id": 23,  "destination": "west",  "packing": "crated", "weight_kg": 500},
    {"id": 24,  "destination": "north",
        "packing": "crated", "weight_kg": "Hello, World!"},
]


@pytest.fixture
def shipments():
    return copy.deepcopy(BASE_SHIPMENTS)


@pytest.fixture
def no_qualified_shipments():
    return [
        {"id": 1,  "destination": "north", "packing": "crated", "weight_kg": 1},
        {"id": 2,  "destination": "south", "packing": "loose",  "weight_kg": 2},
        {"id": 3,  "destination": "east",  "packing": "crated", "weight_kg": 3},
        {"id": 4,  "destination": "west",  "packing": "crated", "weight_kg": 4},
        {"id": 5,  "destination": "north", "packing": "loose",  "weight_kg": 5},
        {"id": 6,  "destination": "south", "packing": "crated", "weight_kg": 6},
        {"id": 7,  "destination": "east",  "packing": "loose",  "weight_kg": 7},
        {"id": 8,  "destination": "west",  "packing": "crated", "weight_kg": 8},
        {"id": 9,  "destination": "north", "packing": "crated", "weight_kg": 0},
        {"id": 10, "destination": "south", "packing": "loose",  "weight_kg": None},
    ]


@pytest.fixture
def qualified_shipments():
    return [
        {"id": 1,  "destination": "north", "packing": "crated", "weight_kg": 120},
        {"id": 2,  "destination": "south", "packing": "loose",  "weight_kg": 110},
        {"id": 3,  "destination": "east",  "packing": "crated", "weight_kg": 310},
        {"id": 4,  "destination": "west",  "packing": "crated", "weight_kg": 150},
        {"id": 5,  "destination": "north", "packing": "loose",  "weight_kg": 160},
        {"id": 6,  "destination": "south", "packing": "crated", "weight_kg": 210},
        {"id": 7,  "destination": "east",  "packing": "loose",  "weight_kg": 400},
        {"id": 8,  "destination": "west",  "packing": "crated", "weight_kg": 500},
    ]


@pytest.fixture
def sorted_qualified_shipments():
    return [
        {"id": 8, "destination": "west",  "packing": "crated", "weight_kg": 500},
        {"id": 7, "destination": "east",  "packing": "loose",  "weight_kg": 400},
        {"id": 3, "destination": "east",  "packing": "crated", "weight_kg": 310},
        {"id": 6, "destination": "south", "packing": "crated", "weight_kg": 210},
        {"id": 5, "destination": "north", "packing": "loose",  "weight_kg": 160},
        {"id": 4, "destination": "west",  "packing": "crated", "weight_kg": 150},
        {"id": 1, "destination": "north", "packing": "crated", "weight_kg": 120},
        {"id": 2, "destination": "south", "packing": "loose",  "weight_kg": 110},
    ]


# Logsweeps
@pytest.fixture
def tmp_log_dir(tmp_path):
    (tmp_path / "log-1.log").write_text(
        "INFO  depot opened\nINFO  van 1 loaded\nWARN  van 2 late\nINFO  van 2 loaded\nERROR crate 88 damaged\nINFO  depot closed\n"
    )
    (tmp_path / "log-2.log").write_text(
        "INFO  depot opened\nINFO  van 1 loaded\nINFO  van 2 loaded\nINFO  depot closed\n"
    )
    (tmp_path / "log-3.log").write_text(
        "INFO  depot opened\nERROR scanner offline\nERROR scanner offline\nWARN  falling back to paper\nERROR crate 12 missing\nINFO  depot closed\n"
    )

    return tmp_path


@pytest.fixture
def tmp_log_dir_with_empty_logs(tmp_path):
    (tmp_path / "log-1.log").write_text("")
    (tmp_path / "log-2.log").write_text("")
    (tmp_path / "log-3.log").write_text("")

    return tmp_path


@pytest.fixture
def tmp_log_dir_with_non_log_file(tmp_log_dir):
    (tmp_log_dir / "log-4.txt").write_text(
        "INFO  depot opened\nINFO  van 1 loaded\nWARN  van 2 late\nINFO  van 2 loaded\nERROR crate 88 damaged\nINFO  depot closed\n"
    )
    (tmp_log_dir / "log-5.md").write_text(
        "INFO  depot opened\nINFO  van 1 loaded\nINFO  van 2 loaded\nINFO  depot closed\n"
    )

    return tmp_log_dir


@pytest.fixture
def tmp_log_dir_with_tie_error(tmp_path):
    (tmp_path / "log-1.log").write_text("ERROR crate 88 damaged\nERROR scanner offline\n")
    (tmp_path / "log-2.log").write_text("ERROR crate 12 missing\nERROR crate 105 damaged\n")

    return tmp_path


# Receipt
@pytest.fixture
def manifest_long():
    rows = [
        ("north",  "loose",   78.0),
        ("south",  "crated",  142.0),
        ("east",   "loose",  205.0),
        ("west",   "crated",  9.0),
        ("north",  "crated", 100.0),
        ("south",  "loose",   77.0),
        ("east",   "crated",  15.0),
        ("west",   "loose",  333.0),
        ("north",  "loose",    48.0),
        ("south",  "crated", 190.0),
        ("north",   "crated", 120.0),
        ("south",   "loose",   40.0),
        ("east",    "crated", 310.0),
    ]

    return rows


@pytest.fixture
def manifest_short():
    rows = [
        ("north",  "loose",   78.0),
        ("south",  "crated",  142.0),
        ("east",   "loose",  205.0),
        ("west",   "crated",  9.0),
        ("north",  "crated", 100.0),
        ("south",  "loose",   77.0),
        ("east",   "crated",  15.0),
        ("west",   "loose",  333.0),
        ("north",  "loose",    48.0),
    ]

    return rows
