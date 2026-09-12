"""The agent mesh: a supervisor routes to one specialist agent."""

import re

from app import llm, tools

BLOCK = re.compile(r"ignore .*instructions|reveal .*prompt|print .*(api[_ ]?key|secret)", re.I)


def planner(message, customer):
    dest = llm.city(message)
    return {
        "flight": tools.search_flights(dest),
        "hotel": tools.search_hotels(dest),
        "weather": tools.get_weather(dest),
    }


def flight_agent(message, customer):
    dest = llm.city(message)
    offer = tools.search_flights(dest)
    return {"flight": offer, "payment": tools.charge(offer["price_sgd"], customer)}


def hotel_agent(message, customer):
    dest = llm.city(message)
    stay = tools.search_hotels(dest)
    return {"hotel": stay, "payment": tools.charge(stay["total_sgd"], customer)}


def advisory(message, customer):
    dest = llm.city(message)
    return {
        "weather": tools.get_weather(dest),
        "visa": tools.get_visa(dest),
        "insurance": tools.quote_insurance(tools.search_flights(dest)["price_sgd"]),
    }


def rescue(message, customer):
    dest = llm.city(message)
    return {"rebooking": tools.rebook(dest), "profile": tools.get_profile(customer)}


AGENTS = {
    "plan": planner,
    "flight": flight_agent,
    "hotel": hotel_agent,
    "advisory": advisory,
    "disruption": rescue,
}


def handle(message, customer="anon"):
    """Supervisor: classify, call the specialist agent, compose the reply."""
    if BLOCK.search(message):
        return {"intent": "blocked", "agent": "guardrail", "facts": {},
                "reply": "I can only help with travel planning, bookings and disruptions."}
    intent = llm.classify(message)
    facts = AGENTS[intent](message, customer)
    return {
        "intent": intent,
        "agent": AGENTS[intent].__name__,
        "facts": facts,
        "reply": llm.compose(facts, message),
    }
