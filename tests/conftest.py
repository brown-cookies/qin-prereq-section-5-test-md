import copy
import pytest

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
