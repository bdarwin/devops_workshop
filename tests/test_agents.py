import pytest

from app import agents, tools


@pytest.mark.parametrize("message,expected", [
    ("plan a holiday in Bangkok", "plan"),
    ("book a flight to Tokyo", "flight"),
    ("I need a hotel room in Seoul", "hotel"),
    ("do I need a visa for Bali", "advisory"),
    ("my flight was cancelled", "disruption"),
])
def test_routing(message, expected):
    assert agents.handle(message)["intent"] == expected


def test_booking_charges_payment():
    out = agents.handle("book a flight to Tokyo", "cust1")
    assert out["facts"]["payment"]["status"] == "authorized"


def test_reply_is_grounded_in_tool_facts():
    out = agents.handle("do I need a visa for Seoul")
    assert "K-ETA" in out["reply"]


def test_tools_return_expected_keys():
    assert set(tools.search_flights("Tokyo")) == {"flight", "city", "price_sgd"}
    assert tools.get_weather("Bali")["forecast"] == "29C rain"
