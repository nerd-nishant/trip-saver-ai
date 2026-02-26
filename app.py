"""
app.py — Trip Saver: AI Travel Planner for Students (Streamlit Web App)
Aesthetic dark design, hardcoded API key, streaming AI output.
"""
import streamlit as st
import time
from destinations import DESTINATIONS
from budget_calculator import estimate_budget
from ai_planner import generate_itinerary, DEFAULT_API_KEY

# ── PAGE CONFIG ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Trip Saver — AI Travel Planner",
    page_icon="🧳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── LOAD CSS ─────────────────────────────────────────────────────
def load_css():
    with open("style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ── APP CONSTANTS ────────────────────────────────────────────────
APP_NAME = "Trip Saver"
APP_ICON = "🧳"
ACCENT = "#f97316"
ACCENT2 = "#6366f1"
SUCCESS = "#10b981"
GOLD = "#fbbf24"
PINK = "#ec4899"
TEAL = "#14b8a6"
TEXT_SEC = "#64748b"

# ── COMPONENTS ──────────────────────────────────────────────────
def section_header(title, emoji="", subtitle=""):
    st.markdown(f"""
    <div style="padding: 10px 0px; margin-bottom: 15px; border-left: 4px solid {ACCENT}; padding-left: 15px;">
        <h2 style="margin: 0;">{emoji} {title}</h2>
        <p style="margin: 0; color: #64748b; font-size: 13px;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def destination_card(name, data, on_dest_click):
    with st.container():
        st.markdown(f"""
        <div class="destination-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div class="destination-emoji">{data['emoji']}</div>
                <div class="budget-badge">₹{data['avg_budget_per_day']['budget']}/day</div>
            </div>
            <div class="destination-title">{name}</div>
            <div class="destination-tagline">{data['tagline']}</div>
            <div style="margin-top: 15px; display: flex; justify-content: space-between; font-size: 11px; color: #64748b;">
                <span>📍 {data['state']}</span>
                <span style="color: {data['color']};">🗓 {data['best_time']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Explore {name}", key=f"btn_{name}", use_container_width=True):
            on_dest_click(name)
            st.rerun()

# ── MAIN APP FUNCTION ───────────────────────────────────────────
def main():
    # ── SESSION STATE ────────────────────────────────────────────────
    if "page" not in st.session_state:
        st.session_state.page = "Home"
    if "selected_dest" not in st.session_state:
        st.session_state.selected_dest = "Rishikesh"
    if "itinerary" not in st.session_state:
        st.session_state.itinerary = None
    if "budget_data" not in st.session_state:
        st.session_state.budget_data = None

    # ── NAVIGATION HELPERS ──────────────────────────────────────────
    def set_page(name):
        st.session_state.page = name

    def on_dest_click(name):
        st.session_state.selected_dest = name
        set_page("Destination Info")

    # ── SIDEBAR ─────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding-bottom: 20px;">
            <div style="font-size: 50px;">{APP_ICON}</div>
            <div style="font-size: 24px; font-weight: bold; color: {ACCENT};">{APP_NAME}</div>
            <div style="font-size: 12px; color: {TEXT_SEC};">for Students</div>
        </div>
        <hr style="border-color: #334155; margin-bottom: 25px;">
        """, unsafe_allow_html=True)

        nav_options = {
            "🏠 Home": "Home",
            "🗺️ Plan Trip": "Plan Trip",
            "📋 Itinerary": "Itinerary",
            "💰 Budget": "Budget",
            "📍 Destination Info": "Destination Info"
        }

        # Find index of current page for radio button
        current_idx = list(nav_options.values()).index(st.session_state.page)
        
        selected_nav = st.sidebar.radio(
            "Navigation",
            options=list(nav_options.keys()),
            index=current_idx,
            label_visibility="collapsed"
        )
        
        st.session_state.page = nav_options[selected_nav]

        st.markdown("""
        <div style="position: fixed; bottom: 20px; left: 20px; font-size: 11px; color: #64748b;">
            Powered by Groq API<br>
            v2.0 • Trip Saver
        </div>
        """, unsafe_allow_html=True)

    # ── PAGES ───────────────────────────────────────────────────────

    # ── HOME PAGE
    if st.session_state.page == "Home":
        st.markdown(f"""
        <div style="text-align: center; padding: 40px 0; background: #151f2e; border-radius: 0 0 20px 20px; margin-top: -65px; margin-bottom: 30px; border-top: 3px solid {ACCENT};">
            <h1 style="font-size: 42px; margin-bottom: 10px;">{APP_ICON} {APP_NAME}</h1>
            <p style="color: #64748b; font-size: 16px;">Budget-friendly itineraries powered by Groq AI</p>
        </div>
        """, unsafe_allow_html=True)

        # Stats pills
        cols = st.columns(4)
        stats = [
            ("📍", "6", "Destinations", ACCENT),
            ("🤖", "AI", "Powered", ACCENT2),
            ("💰", "₹", "Budget Tracking", SUCCESS),
            ("🎒", "Students", "Focused", GOLD),
        ]
        for col, (icon, val, lbl, clr) in zip(cols, stats):
            col.markdown(f"""
            <div style="background: #1a2235; padding: 15px; border-radius: 15px; border: 1px solid #334155; text-align: center;">
                <div style="font-size: 18px; font-weight: bold; color: {clr};">{icon} {val}</div>
                <div style="font-size: 11px; color: #64748b;">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### Choose Your Destination ✈️")
        dest_names = list(DESTINATIONS.keys())
        for i in range(0, len(dest_names), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(dest_names):
                    name = dest_names[i+j]
                    with cols[j]:
                        destination_card(name, DESTINATIONS[name], on_dest_click)

    # ── PLANNER PAGE
    elif st.session_state.page == "Plan Trip":
        section_header("Plan Your Trip", "🗺️", "Fill in the details and let AI craft your itinerary")
        
        with st.form("planner_form"):
            col1, col2 = st.columns(2)
            
            departure = col1.selectbox("🏠 Departure City", 
                ["Delhi", "Mumbai", "Kolkata", "Bangalore", "Hyderabad", "Chennai", "Pune", "Chandigarh", "Siliguri"],
                index=0)
            
            destination = col2.selectbox("📍 Destination", 
                list(DESTINATIONS.keys()), 
                index=list(DESTINATIONS.keys()).index(st.session_state.selected_dest))
            
            duration = col1.slider("📅 Duration (days)", 1, 15, 4)
            group_size = col2.slider("👥 Group Size", 1, 20, 3)
            
            budget_person = col1.number_input("💰 Budget Per Person (₹)", min_value=1000, value=5000, step=500)
            budget_tier = col2.selectbox("🏷️ Budget Tier", ["budget", "mid", "premium"], index=0)
            
            travel_style = col1.selectbox("🎯 Travel Style", [
                "Adventure & Trekking", "Spiritual & Cultural",
                "Relaxation & Sightseeing", "Heritage & History",
                "Food & Shopping", "Backpacker"
            ], index=0)
            
            prefs = st.text_area("✍️ Special Preferences (optional)", 
                placeholder="e.g. vegetarian only, love photography, need wheelchair access…")
            
            submitted = st.form_submit_button(f"{APP_ICON} Generate AI Itinerary →", use_container_width=True)
            
            if submitted:
                st.session_state.selected_dest = destination
                st.session_state.budget_data = estimate_budget(destination, duration, budget_tier, group_size, departure)
                
                # Update state and redirect
                st.session_state.page = "Itinerary"
                st.session_state.gen_params = {
                    "destination": destination,
                    "duration": duration,
                    "budget": budget_person,
                    "group_size": group_size,
                    "travel_style": travel_style,
                    "departure": departure,
                    "preferences": prefs
                }
                st.rerun()

    # ── ITINERARY PAGE
    elif st.session_state.page == "Itinerary":
        section_header("AI Itinerary", "📋", "Generated by Groq API · streams live")
        
        if "gen_params" in st.session_state:
            # Run generation
            params = st.session_state.pop("gen_params")
            
            status = st.empty()
            status.warning("⏳ Connecting to Groq API and streaming response …")
            
            container = st.empty()
            # Use a list to store full_text to make it mutable in the closure
            state = {"full_text": ""}
            
            def on_chunk(chunk):
                state["full_text"] += chunk
                container.markdown(state["full_text"])
                
            result = generate_itinerary(
                destination=params["destination"],
                duration=params["duration"],
                budget_per_person=params["budget"],
                group_size=params["group_size"],
                travel_style=params["travel_style"],
                departure_city=params["departure"],
                preferences=params["preferences"],
                stream_callback=on_chunk
            )
            
            st.session_state.itinerary = result
            status.success("✅ Itinerary ready! Scroll to explore your trip.")
            st.rerun() # Rerun to show static version with copy button
            
        elif st.session_state.itinerary:
            st.markdown(st.session_state.itinerary)
            if st.button("📋 Copy to Clipboard"):
                st.toast("Copied to clipboard!")
                st.code(st.session_state.itinerary, language=None)
        else:
            st.info("👈 Fill the Plan Trip form and click Generate")

    # ── BUDGET PAGE
    elif st.session_state.page == "Budget":
        section_header("Budget Breakdown", "💰", "Instant estimate — no API needed")
        
        if st.session_state.budget_data:
            bd = st.session_state.budget_data
            
            # Summary row
            cols = st.columns(4)
            summary_items = [
                ("Per Person", f"₹{bd['per_person_total']:,}", SUCCESS),
                ("Group Total", f"₹{bd['group_total']:,}", ACCENT),
                ("Duration", f"{bd['duration']} days", ACCENT2),
                ("Tier", bd['tier'].upper(), GOLD),
            ]
            for col, (label, val, clr) in zip(cols, summary_items):
                col.markdown(f"""
                <div style="background: #111827; padding: 20px; border-radius: 15px; border: 1px solid #334155; text-align: center; border-top: 3px solid {clr};">
                    <div style="font-size: 20px; font-weight: bold; color: {clr};">{val}</div>
                    <div style="font-size: 12px; color: #64748b;">{label}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("#### Where Your Money Goes (per person)")
            categories = [
                ("✈️ Intercity Transport", bd["intercity_transport"], ACCENT),
                ("🚌 Local Transport", bd["local_transport"], ACCENT2),
                ("🏨 Accommodation", bd["accommodation"], SUCCESS),
                ("🍛 Food & Drinks", bd["food"], GOLD),
                ("🎯 Activities", bd["activities"], PINK),
                ("🛍️ Shopping & Misc", bd["misc"], TEAL),
            ]
            
            total = bd["per_person_total"]
            for lbl, amt, clr in categories:
                pct = (amt / total) if total else 0
                st.markdown(f"**{lbl}** — ₹{amt:,}")
                st.progress(pct)
                
            st.markdown("---")
            st.markdown("#### 💡 Student Money-Saving Tips")
            tips = [
                "Book train on IRCTC 60 days ahead — cheapest fares available early",
                "Stay at Zostel or Moustache hostels — great vibes, cheapest beds",
                "Eat at dhabas & street stalls — same taste, 3× cheaper",
                "Travel midweek — weekend prices are always inflated",
                "Student ID cards can unlock 25–50% off at major monuments",
            ]
            for tip in tips:
                st.markdown(f"✅ {tip}")
                
        else:
            st.info("Generate an itinerary to see budget breakdown.")

    # ── DESTINATION INFO PAGE
    elif st.session_state.page == "Destination Info":
        section_header("Destination Guide", "📍", "Explore key highlights and tips")
        
        dest_name = st.session_state.selected_dest
        data = DESTINATIONS[dest_name]
        clr = data["color"]
        
        # Hero
        st.markdown(f"""
        <div style="background: #111827; padding: 25px; border-radius: 20px; border: 1px solid #334155; border-left: 10px solid {clr};">
            <div style="display: flex; gap: 20px; align-items: center;">
                <div style="font-size: 50px;">{data['emoji']}</div>
                <div>
                    <h1 style="color: {clr}; margin: 0;">{dest_name}</h1>
                    <p style="color: #64748b; margin: 0;">{data['tagline']}</p>
                </div>
            </div>
            <p style="margin-top: 20px; color: #f1f5f9;">{data['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"#### 🎯 Must-Visit (at {dest_name})")
            for p in data["places"][:5]:
                st.markdown(f"› {p}")
                
            st.markdown(f"#### 🍛 Food Spots")
            for f in data["food_spots"][:4]:
                st.markdown(f"› {f}")
                
        with col2:
            st.markdown("#### 🎒 Student Tips")
            for t in data["student_tips"]:
                st.markdown(f"✅ {t}")
                
            b = data["avg_budget_per_day"]
            st.markdown(f"""
            <div style="background: #1a2235; padding: 15px; border-radius: 10px; border: 1px solid #f59e0b; margin-top: 20px;">
                <div style="font-weight: bold; color: {GOLD}; margin-bottom: 5px;">Average Daily Budget:</div>
                <div style="font-size: 13px;">
                    Budget: <b>₹{b['budget']}</b> • Mid: <b>₹{b['mid']}</b> • Premium: <b>₹{b['premium']}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.link_button("🗺️ Open in Google Maps", data["maps_url"], use_container_width=True)

        if st.button(f"Plan a trip to {dest_name} →", use_container_width=True, type="primary"):
            set_page("Plan Trip")
            st.rerun()

if __name__ == "__main__":
    main()
