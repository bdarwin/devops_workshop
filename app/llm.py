"""Claude access. Falls back to a keyword stub when no API key is set,
so tests and the CI eval gate run offline and free."""

import os
import re

from app import prompts

MODEL = os.environ.get("CONCIERGE_MODEL", "claude-opus-5")

RULES = [
    ("disruption", r"cancel|delay|stuck|stranded|missed"),
    ("flight", r"flight|fly"),
    ("hotel", r"hotel|room|stay"),
    ("advisory", r"visa|weather|insurance|safe"),
    ("plan", r"plan|trip|itinerar|holiday"),
]

CITIES = ["Tokyo", "Bangkok", "Seoul", "Bali"]


def live():
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


def _client():
    import anthropic

    return anthropic.Anthropic()


def classify(message):
    """Return one of: plan, flight, hotel, advisory, disruption."""
    if live():
        reply = _ask(prompts.SUPERVISOR, message).lower().strip()
        if reply in {"plan", "flight", "hotel", "advisory", "disruption"}:
            return reply
    for intent, pattern in RULES:
        if re.search(pattern, message.lower()):
            return intent
    return "plan"


def city(message):
    for name in CITIES:
        if name.lower() in message.lower():
            return name
    return "Tokyo"


def compose(facts, message):
    """Turn tool facts into a reply."""
    context = "\n".join(f"- {k}: {v}" for k, v in facts.items())
    if live():
        return _ask(prompts.REPLY, f"Traveller: {message}\n\nFacts:\n{context}")
    return f"Here's what I found:\n{context}"


def _ask(system, user):
    response = _client().messages.create(
        model=MODEL,
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return "".join(b.text for b in response.content if b.type == "text").strip()
