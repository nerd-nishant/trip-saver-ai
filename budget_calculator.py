"""
budget_calculator.py
Budget estimation utilities for student travel planning.
"""

from destinations import DESTINATIONS


TRANSPORT_COSTS = {
    # (from_city, to_destination): {mode: cost_per_person}
    ("Delhi", "Rishikesh"): {"train": 400, "bus": 550, "flight": None},
    ("Delhi", "Varanasi (Banaras)"): {"train": 450, "bus": 700, "flight": 3500},
    ("Delhi", "Manali"): {"bus": 900, "train": None, "flight": None},
    ("Delhi", "Jaipur"): {"train": 350, "bus": 350, "flight": 2500},
    ("Delhi", "Goa"): {"train": 800, "bus": None, "flight": 3500},
    ("Delhi", "Darjeeling"): {"train": 550, "bus": None, "flight": 4000},
    ("Mumbai", "Goa"): {"train": 500, "bus": 700, "flight": 3000},
    ("Mumbai", "Manali"): {"train": 900, "bus": None, "flight": 5000},
    ("Mumbai", "Varanasi (Banaras)"): {"train": 900, "bus": None, "flight": 5000},
    ("Kolkata", "Darjeeling"): {"train": 400, "bus": None, "flight": 3500},
    ("Varanasi (Banaras)", "Rishikesh"): {"train": 550, "bus": 700, "flight": None},
}

FOOD_COSTS = {
    "budget": 250,    # dhabas, street food
    "mid": 500,       # casual restaurants
    "premium": 1000,  # proper restaurants
}

ACCOMMODATION_COSTS = {
    "budget": 450,     # hostels, dormitories
    "mid": 1200,      # guesthouses
    "premium": 3500,  # hotels / resorts
}

LOCAL_TRANSPORT_PER_DAY = {
    "budget": 100,
    "mid": 250,
    "premium": 500,
}


def estimate_budget(
    destination: str,
    duration: int,
    budget_tier: str,         # "budget", "mid", "premium"
    group_size: int,
    departure_city: str = "Delhi",
) -> dict:
    """
    Returns a per-person and total group budget estimate.
    """
    tier = budget_tier.lower()

    # Accommodation
    accom_daily = ACCOMMODATION_COSTS.get(tier, 450)
    accom_total = accom_daily * duration

    # Food
    food_daily = FOOD_COSTS.get(tier, 250)
    food_total = food_daily * duration

    # Local transport
    local_daily = LOCAL_TRANSPORT_PER_DAY.get(tier, 100)
    local_total = local_daily * duration

    # Activities – use destination average
    dest_data = DESTINATIONS.get(destination, {})
    activity_daily = dest_data.get("avg_budget_per_day", {}).get(tier, 300)
    activity_total = activity_daily * duration * 0.4  # ~40% of daily budget for activities

    # Intercity transport (one-way, estimate return as 2x)
    key = (departure_city, destination)
    transport_options = TRANSPORT_COSTS.get(key, {})
    transport_cost = None
    for mode in ["train", "bus", "flight"]:
        cost = transport_options.get(mode)
        if cost:
            transport_cost = cost * 2  # round trip
            transport_mode = mode
            break
    if transport_cost is None:
        transport_cost = 1200  # default estimate
        transport_mode = "estimated"

    # Shopping & misc – flat estimate
    misc = 500 if tier == "budget" else (1000 if tier == "mid" else 2000)

    subtotal = accom_total + food_total + local_total + activity_total + transport_cost + misc

    return {
        "accommodation": round(accom_total),
        "food": round(food_total),
        "local_transport": round(local_total),
        "activities": round(activity_total),
        "intercity_transport": round(transport_cost),
        "transport_mode": transport_mode,
        "misc": misc,
        "per_person_total": round(subtotal),
        "group_total": round(subtotal * group_size),
        "duration": duration,
        "group_size": group_size,
        "tier": tier,
    }


def format_budget_summary(budget: dict) -> str:
    """Format a budget dict into a readable string."""
    lines = [
        f"💰 BUDGET ESTIMATE ({budget['tier'].upper()} TIER)",
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"  ✈️  Intercity Transport ({budget['transport_mode']}): ₹{budget['intercity_transport']:,}",
        f"  🚌  Local Transport:          ₹{budget['local_transport']:,}",
        f"  🏨  Accommodation:            ₹{budget['accommodation']:,}",
        f"  🍛  Food & Drinks:            ₹{budget['food']:,}",
        f"  🎯  Activities & Entry:       ₹{budget['activities']:,}",
        f"  🛍️  Shopping & Misc:          ₹{budget['misc']:,}",
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"  👤 Per Person Total:    ₹{budget['per_person_total']:,}",
        f"  👥 Group Total ({budget['group_size']} pax): ₹{budget['group_total']:,}",
    ]
    return "\n".join(lines)
