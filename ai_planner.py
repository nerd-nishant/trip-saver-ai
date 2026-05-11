"""
ai_planner.py — Groq API integration for Trip Saver
Hardcoded API key, streaming output.
"""
from groq import Groq

# ── Hardcoded API key ──────────────────────────────────────────
DEFAULT_API_KEY = "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"

def generate_itinerary(
    destination: str,
    duration: int,
    budget_per_person: int,
    group_size: int,
    travel_style: str,
    departure_city: str,
    preferences: str = "",
    api_key: str = DEFAULT_API_KEY,
    stream_callback=None,   # callable(text_chunk) for live streaming
) -> str:
    """
    Generate itinerary using Groq. If stream_callback is provided, chunks are sent as they arrive.
    Returns the full combined text.
    """
    client = Groq(api_key=api_key or DEFAULT_API_KEY)

    prefs_line = f"Preferences: {preferences}" if preferences else ""

    prompt = f"""You are an expert Indian travel planner for budget-savvy college students.
Create a {duration}-day trip plan for:
• Destination: {destination}, India
• From: {departure_city}
• Budget/person: ₹{budget_per_person:,} | Group: {group_size} students | Style: {travel_style}
{prefs_line}

Format your response as follows:

## 🚀 TRIP OVERVIEW
(Best route from {departure_city}, key highlights, one-line cost summary)

## 📅 DAY-BY-DAY ITINERARY
For each Day 1 to Day {duration}:
### Day X — [Theme]
**Morning:** activity + cost
**Afternoon:** activity + lunch spot + cost
**Evening:** activity + dinner spot + cost
**Stay:** budget accommodation + INR/night

## 💰 BUDGET BREAKDOWN (per person)
| Category | Cost (₹) |
|---|---|
| Transport | ₹X |
| Accommodation | ₹X |
| Food | ₹X |
| Activities | ₹X |
| Misc | ₹X |
| **TOTAL** | **₹X** |

## 🎒 PACKING LIST
(8 items for {destination})

## 💡 STUDENT MONEY HACKS
(5 tips to save money at {destination})

## ⚠️ SAFETY TIPS
(3 key tips)

Be friendly, use emojis, reference real Indian places and prices in INR (2024-25 rates).
"""

    try:
        full_text = ""
        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a professional travel planner."},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                full_text += content
                if stream_callback:
                    stream_callback(content)
        
        return full_text if full_text else "⚠️ Empty response received. Please try again."
    except Exception as e:
        err = str(e)
        if "api_key" in err.lower() or "invalid_api_key" in err.lower():
            return "❌ Invalid Groq API key. Please check and try again."
        elif "insufficient_quota" in err.lower():
            return "❌ Groq API quota exceeded. Please check your billing/balance."
        return f"❌ Error: {err}"
