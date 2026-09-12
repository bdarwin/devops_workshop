"""Mock external services (flights, hotels, weather, insurance, payments, profiles)."""

FARE = {"Tokyo": 890, "Bangkok": 310, "Seoul": 640, "Bali": 275}
RATE = {"Tokyo": 240, "Bangkok": 95, "Seoul": 160, "Bali": 130}
WEATHER = {"Tokyo": "14C clear", "Bangkok": "33C storms", "Seoul": "9C windy", "Bali": "29C rain"}
VISA = {"Tokyo": "visa-free 90 days", "Bangkok": "visa-free 30 days",
        "Seoul": "K-ETA required", "Bali": "visa on arrival"}


def search_flights(city, party=1):
    price = FARE.get(city, 500) * party
    return {"flight": "GE100", "city": city, "price_sgd": price}


def search_hotels(city, nights=3):
    rate = RATE.get(city, 150)
    return {"hotel": f"Go East {city}", "nightly_sgd": rate, "nights": nights,
            "total_sgd": rate * nights}


def get_weather(city):
    return {"city": city, "forecast": WEATHER.get(city, "22C fair")}


def get_visa(city):
    return {"city": city, "rule": VISA.get(city, "check the embassy")}


def quote_insurance(trip_value):
    return {"plan": "Voyager Plus", "premium_sgd": round(max(38.0, trip_value * 0.045), 2)}


def charge(amount, customer):
    return {"status": "authorized", "ref": f"PAY-{abs(hash((customer, amount))) % 10**6:06d}"}


def get_profile(customer):
    return {"customer": customer, "tier": "gold" if customer.endswith("1") else "standard"}


def rebook(city):
    return {"city": city, "new_flight": "GE100R", "departs_in_hours": 4, "fee_sgd": 0}
