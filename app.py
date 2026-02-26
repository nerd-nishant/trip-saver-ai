"""
app.py — Trip Saver: AI Travel Planner for Students
Rename: "Trip Saver" | API key hardcoded | Streaming AI output | Professional UI
"""

import threading
import tkinter as tk
import customtkinter as ctk

from destinations import DESTINATIONS
from budget_calculator import estimate_budget
from ai_planner import generate_itinerary, DEFAULT_API_KEY
from ui_components import (
    BG_DARK, BG_CARD, BG_INPUT, BG_GLASS,
    ACCENT, ACCENT2, GOLD, TEXT_PRI, TEXT_SEC,
    SUCCESS, WARNING, BORDER, BORDER_LIT, TEAL, PINK,
    ScrollableFrame, SectionHeader, DestinationCard,
    InfoPanel, BudgetBar, GlowButton, Divider,
)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

APP_NAME  = "Trip Saver"
APP_ICON  = "🧳"
API_KEY   = DEFAULT_API_KEY


# ── helpers ───────────────────────────────────────────────────
def make_textbox(parent, height=400):
    return ctk.CTkTextbox(
        parent, height=height,
        fg_color=BG_INPUT, text_color=TEXT_PRI,
        font=ctk.CTkFont("Consolas", 12),
        border_color=BORDER_LIT, border_width=1,
        wrap="word", corner_radius=10,
    )


def field_label(parent, text):
    ctk.CTkLabel(
        parent, text=text,
        font=ctk.CTkFont("Segoe UI", 12, "bold"),
        text_color=TEXT_PRI,
    ).pack(anchor="w", pady=(10, 3))


# ════════════════════════════════════════════════════════════════
#  HOME TAB
# ════════════════════════════════════════════════════════════════
class HomeTab(ctk.CTkFrame):
    def __init__(self, master, on_dest_select, **kw):
        kw.setdefault("fg_color", BG_DARK)
        super().__init__(master, **kw)
        self.on_dest_select = on_dest_select
        self._build()

    def _build(self):
        # ── Hero banner ──────────────────────────────────────
        hero = ctk.CTkFrame(self, fg_color=BG_GLASS, corner_radius=0)
        hero.pack(fill="x")

        # decorative top stripe
        ctk.CTkFrame(hero, fg_color=ACCENT, height=3, corner_radius=0
                     ).pack(fill="x")

        ctk.CTkLabel(
            hero,
            text=f"{APP_ICON}  {APP_NAME}",
            font=ctk.CTkFont("Segoe UI", 32, "bold"),
            text_color=TEXT_PRI,
        ).pack(pady=(20, 2))
        ctk.CTkLabel(
            hero,
            text="Budget-friendly itineraries powered by Groq API",
            font=ctk.CTkFont("Segoe UI", 13),
            text_color=TEXT_SEC,
        ).pack()

        # Stats pills
        pills = ctk.CTkFrame(hero, fg_color="transparent")
        pills.pack(pady=16)
        for icon, val, lbl, clr in [
            ("📍", "6",      "Destinations", ACCENT),
            ("🤖", "AI",     "Powered",      ACCENT2),
            ("💰", "₹",      "Budget Tracking", SUCCESS),
            ("🎒", "Students", "Focused",    GOLD),
        ]:
            p = ctk.CTkFrame(pills, fg_color=BG_INPUT, corner_radius=24,
                             border_width=1, border_color=BORDER_LIT)
            p.pack(side="left", padx=6)
            inner = ctk.CTkFrame(p, fg_color="transparent")
            inner.pack(padx=16, pady=8)
            ctk.CTkLabel(inner, text=f"{icon} {val}",
                         font=ctk.CTkFont("Segoe UI", 13, "bold"),
                         text_color=clr).pack()
            ctk.CTkLabel(inner, text=lbl,
                         font=ctk.CTkFont("Segoe UI", 9),
                         text_color=TEXT_SEC).pack()

        ctk.CTkFrame(hero, fg_color=BORDER_LIT, height=1, corner_radius=0
                     ).pack(fill="x", pady=(8, 0))

        # ── Destinations grid ────────────────────────────────
        outer = ScrollableFrame(self)
        outer.pack(fill="both", expand=True, padx=16, pady=16)

        ctk.CTkLabel(
            outer, text="Choose Your Destination  ✈️",
            font=ctk.CTkFont("Segoe UI", 15, "bold"),
            text_color=TEXT_PRI,
        ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(4, 14))

        dest_list = list(DESTINATIONS.keys())
        for idx, name in enumerate(dest_list):
            r, c = divmod(idx, 3)
            card = DestinationCard(outer, name, on_click=self.on_dest_select)
            card.grid(row=r + 1, column=c, padx=8, pady=8, sticky="nsew")
            outer.grid_columnconfigure(c, weight=1)


# ════════════════════════════════════════════════════════════════
#  PLANNER TAB
# ════════════════════════════════════════════════════════════════
class PlannerTab(ctk.CTkFrame):
    def __init__(self, master, on_generate, **kw):
        kw.setdefault("fg_color", BG_DARK)
        super().__init__(master, **kw)
        self.on_generate = on_generate
        self._build()

    def _build(self):
        SectionHeader(self, "Plan Your Trip", "🗺️",
                      subtitle="Fill in the details and let AI craft your itinerary"
                      ).pack(fill="x")

        scroll = ScrollableFrame(self)
        scroll.pack(fill="both", expand=True, padx=24, pady=12)
        scroll.grid_columnconfigure(0, weight=1)
        scroll.grid_columnconfigure(1, weight=1)

        def opt(row, col, label, values, default, color=ACCENT):
            ctk.CTkLabel(scroll, text=label,
                         font=ctk.CTkFont("Segoe UI", 12, "bold"),
                         text_color=TEXT_PRI,
                         ).grid(row=row*2, column=col, sticky="w", pady=(10, 2))
            w = ctk.CTkOptionMenu(
                scroll, values=values,
                fg_color=BG_INPUT, dropdown_fg_color=BG_CARD,
                button_color=color, button_hover_color="#ea580c" if color == ACCENT else "#4f46e5",
                text_color=TEXT_PRI, corner_radius=8, height=40)
            w.set(default)
            w.grid(row=row*2+1, column=col, sticky="ew", pady=(0, 4))
            return w

        self.departure = opt(0, 0, "🏠  Departure City",
            ["Delhi", "Mumbai", "Kolkata", "Bangalore",
             "Hyderabad", "Chennai", "Pune", "Chandigarh", "Siliguri"], "Delhi")

        self.destination = opt(0, 1, "📍  Destination",
            list(DESTINATIONS.keys()), "Rishikesh", ACCENT2)

        # Duration
        ctk.CTkLabel(scroll, text="📅  Duration (days)",
                     font=ctk.CTkFont("Segoe UI", 12, "bold"),
                     text_color=TEXT_PRI).grid(row=2, column=0, sticky="w", pady=(10, 2))
        dur_row = ctk.CTkFrame(scroll, fg_color="transparent")
        dur_row.grid(row=3, column=0, sticky="ew", pady=(0, 4))
        self.duration = ctk.CTkSlider(dur_row, from_=1, to=15, number_of_steps=14,
            progress_color=ACCENT, button_color=ACCENT,
            button_hover_color="#ea580c", width=200)
        self.duration.set(4)
        self.duration.pack(side="left", padx=(0, 10))
        self.dur_lbl = ctk.CTkLabel(dur_row, text="4 days",
            font=ctk.CTkFont("Segoe UI", 13, "bold"), text_color=ACCENT)
        self.dur_lbl.pack(side="left")
        self.duration.configure(command=lambda v: self.dur_lbl.configure(text=f"{int(v)} days"))

        # Group
        ctk.CTkLabel(scroll, text="👥  Group Size",
                     font=ctk.CTkFont("Segoe UI", 12, "bold"),
                     text_color=TEXT_PRI).grid(row=2, column=1, sticky="w", pady=(10, 2))
        grp_row = ctk.CTkFrame(scroll, fg_color="transparent")
        grp_row.grid(row=3, column=1, sticky="ew", pady=(0, 4))
        self.group_size = ctk.CTkSlider(grp_row, from_=1, to=20, number_of_steps=19,
            progress_color=ACCENT2, button_color=ACCENT2,
            button_hover_color="#4f46e5", width=200)
        self.group_size.set(3)
        self.group_size.pack(side="left", padx=(0, 10))
        self.grp_lbl = ctk.CTkLabel(grp_row, text="3 students",
            font=ctk.CTkFont("Segoe UI", 13, "bold"), text_color=ACCENT2)
        self.grp_lbl.pack(side="left")
        self.group_size.configure(command=lambda v: self.grp_lbl.configure(text=f"{int(v)} students"))

        # Budget
        ctk.CTkLabel(scroll, text="💰  Budget Per Person (₹)",
                     font=ctk.CTkFont("Segoe UI", 12, "bold"),
                     text_color=TEXT_PRI).grid(row=4, column=0, sticky="w", pady=(10, 2))
        self.budget_entry = ctk.CTkEntry(
            scroll, fg_color=BG_INPUT, border_color=BORDER_LIT,
            text_color=TEXT_PRI, height=40, corner_radius=8)
        self.budget_entry.insert(0, "5000")
        self.budget_entry.grid(row=5, column=0, sticky="ew", pady=(0, 4))

        self.budget_tier = opt(2, 1, "🏷️  Budget Tier",
            ["budget", "mid", "premium"], "budget", SUCCESS)

        self.travel_style = opt(3, 0, "🎯  Travel Style", [
            "Adventure & Trekking", "Spiritual & Cultural",
            "Relaxation & Sightseeing", "Heritage & History",
            "Food & Shopping", "Backpacker"],
            "Adventure & Trekking", TEAL)

        # Prefs
        ctk.CTkLabel(scroll, text="✍️  Special Preferences (optional)",
                     font=ctk.CTkFont("Segoe UI", 12, "bold"),
                     text_color=TEXT_PRI).grid(row=7, column=0, columnspan=2, sticky="w", pady=(10, 2))
        self.prefs = ctk.CTkTextbox(
            scroll, height=65, fg_color=BG_INPUT,
            border_color=BORDER_LIT, border_width=1,
            text_color=TEXT_SEC, corner_radius=8)
        self.prefs.insert("0.0", "e.g.  vegetarian only, love photography, need wheelchair access…")
        self.prefs.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(0, 6))

        scroll.grid_columnconfigure(0, weight=1)
        scroll.grid_columnconfigure(1, weight=1)

        # Generate button
        self.gen_btn = GlowButton(
            self, text=f"  {APP_ICON}  Generate AI Itinerary  →",
            font=ctk.CTkFont("Segoe UI", 15, "bold"),
            height=52, corner_radius=12, command=self._on_click)
        self.gen_btn.pack(fill="x", padx=24, pady=14)

    def _on_click(self):
        prefs_text = self.prefs.get("0.0", "end").strip()
        if "e.g." in prefs_text:
            prefs_text = ""
        self.on_generate(
            destination=self.destination.get(),
            duration=int(self.duration.get()),
            budget=int(self.budget_entry.get().strip() or "5000"),
            group_size=int(self.group_size.get()),
            travel_style=self.travel_style.get(),
            departure=self.departure.get(),
            preferences=prefs_text,
            budget_tier=self.budget_tier.get(),
        )

    def set_destination(self, name):
        self.destination.set(name)


# ════════════════════════════════════════════════════════════════
#  ITINERARY TAB
# ════════════════════════════════════════════════════════════════
class ItineraryTab(ctk.CTkFrame):
    def __init__(self, master, **kw):
        kw.setdefault("fg_color", BG_DARK)
        super().__init__(master, **kw)
        self._build()

    def _build(self):
        SectionHeader(self, "AI Itinerary", "📋",
                      subtitle="Generated by Groq API · streams live"
                      ).pack(fill="x")

        # Status bar
        self.status_bar = ctk.CTkFrame(self, fg_color=BG_GLASS, corner_radius=0, height=36)
        self.status_bar.pack(fill="x")
        self.status_bar.pack_propagate(False)
        self.status_lbl = ctk.CTkLabel(
            self.status_bar,
            text="  👈  Fill the Plan Trip form and click Generate",
            font=ctk.CTkFont("Segoe UI", 11), text_color=TEXT_SEC, anchor="w")
        self.status_lbl.pack(side="left", padx=12)

        # progress bar (hidden by default)
        self.progress = ctk.CTkProgressBar(
            self.status_bar, mode="indeterminate",
            progress_color=ACCENT, fg_color=BG_INPUT, height=4)

        self.textbox = make_textbox(self)
        self.textbox.pack(fill="both", expand=True, padx=16, pady=12)

        # Bottom toolbar
        tb = ctk.CTkFrame(self, fg_color=BG_GLASS, corner_radius=0, height=46)
        tb.pack(fill="x")
        tb.pack_propagate(False)
        ctk.CTkButton(
            tb, text="📋  Copy to Clipboard",
            command=self._copy,
            fg_color=BG_INPUT, hover_color=BORDER_LIT,
            text_color=TEXT_PRI, font=ctk.CTkFont("Segoe UI", 11),
            corner_radius=8, height=30, width=180,
        ).pack(side="right", padx=12, pady=8)

    def show_loading(self):
        self.status_lbl.configure(
            text="  ⏳  Connecting to Groq API and streaming response …",
            text_color=GOLD)
        self.progress.pack(side="right", padx=12, pady=0, fill="y")
        self.progress.start()
        self._set_text("🤖  Generating your personalised itinerary …\n\nThis typically takes 5–15 seconds.")

    def stream_chunk(self, chunk: str):
        """Append a streaming chunk to the textbox (called from main thread)."""
        self.textbox.configure(state="normal")
        # Clear placeholder on first chunk
        current = self.textbox.get("0.0", "end").strip()
        if current.startswith("🤖"):
            self.textbox.delete("0.0", "end")
        self.textbox.insert("end", chunk)
        self.textbox.see("end")
        self.textbox.configure(state="disabled")

    def show_done(self, had_error=False):
        self.progress.stop()
        self.progress.pack_forget()
        if had_error:
            self.status_lbl.configure(
                text="  ❌  Error generating itinerary. See details below.",
                text_color=PINK)
        else:
            self.status_lbl.configure(
                text="  ✅  Itinerary ready! Scroll to explore your trip.",
                text_color=SUCCESS)

    def _set_text(self, text: str):
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", text)
        self.textbox.configure(state="disabled")

    def _copy(self):
        content = self.textbox.get("0.0", "end")
        self.clipboard_clear()
        self.clipboard_append(content)
        self.status_lbl.configure(text="  ✅  Copied to clipboard!", text_color=SUCCESS)
        self.after(2000, lambda: self.status_lbl.configure(
            text="  ✅  Itinerary ready!", text_color=SUCCESS))


# ════════════════════════════════════════════════════════════════
#  BUDGET TAB
# ════════════════════════════════════════════════════════════════
class BudgetTab(ctk.CTkFrame):
    def __init__(self, master, **kw):
        kw.setdefault("fg_color", BG_DARK)
        super().__init__(master, **kw)
        self._inner = None
        self._build()

    def _build(self):
        SectionHeader(self, "Budget Breakdown", "💰",
                      subtitle="Instant estimate — no API needed"
                      ).pack(fill="x")
        self.placeholder = ctk.CTkLabel(
            self, text="Generate an itinerary to see budget breakdown.",
            font=ctk.CTkFont("Segoe UI", 13), text_color=TEXT_SEC)
        self.placeholder.pack(expand=True)

    def update_budget(self, bdata: dict):
        self.placeholder.pack_forget()
        if self._inner:
            self._inner.destroy()

        self._inner = ScrollableFrame(self)
        self._inner.pack(fill="both", expand=True, padx=16, pady=12)

        # Big summary card
        summary = ctk.CTkFrame(self._inner, fg_color=BG_CARD, corner_radius=14,
                               border_width=1, border_color=BORDER_LIT)
        summary.pack(fill="x", pady=(0, 12))

        ctk.CTkFrame(summary, fg_color=ACCENT, height=3, corner_radius=0
                     ).pack(fill="x")
        row = ctk.CTkFrame(summary, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=16)

        for label, val, color in [
            ("Per Person", f"₹{bdata['per_person_total']:,}", SUCCESS),
            ("Group Total", f"₹{bdata['group_total']:,}\n({bdata['group_size']} students)", ACCENT),
            ("Duration", f"{bdata['duration']} days", ACCENT2),
            ("Tier", bdata['tier'].upper(), GOLD),
        ]:
            col = ctk.CTkFrame(row, fg_color=BG_INPUT, corner_radius=10)
            col.pack(side="left", expand=True, fill="x", padx=6)
            ctk.CTkLabel(col, text=val,
                         font=ctk.CTkFont("Segoe UI", 17, "bold"),
                         text_color=color).pack(pady=(10, 2))
            ctk.CTkLabel(col, text=label,
                         font=ctk.CTkFont("Segoe UI", 10),
                         text_color=TEXT_SEC).pack(pady=(0, 10))

        # Breakdown bars
        bars = ctk.CTkFrame(self._inner, fg_color=BG_CARD, corner_radius=14,
                            border_width=1, border_color=BORDER)
        bars.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(bars, text="Where Your Money Goes (per person)",
                     font=ctk.CTkFont("Segoe UI", 12, "bold"),
                     text_color=TEXT_PRI).pack(anchor="w", padx=16, pady=(12, 8))

        total = bdata["per_person_total"]
        for lbl, amt, clr in [
            ("✈️  Intercity Transport", bdata["intercity_transport"], ACCENT),
            ("🚌  Local Transport",     bdata["local_transport"],     ACCENT2),
            ("🏨  Accommodation",       bdata["accommodation"],       SUCCESS),
            ("🍛  Food & Drinks",       bdata["food"],                GOLD),
            ("🎯  Activities",          bdata["activities"],          PINK),
            ("🛍️  Shopping & Misc",     bdata["misc"],                TEAL),
        ]:
            BudgetBar(bars, lbl, amt, total, clr).pack(fill="x", padx=16, pady=2)
        ctk.CTkFrame(bars, fg_color="transparent", height=8).pack()

        # Tips
        tips_card = ctk.CTkFrame(self._inner, fg_color=BG_CARD, corner_radius=14,
                                 border_width=1, border_color=BORDER)
        tips_card.pack(fill="x")
        ctk.CTkLabel(tips_card, text="💡  Student Money-Saving Tips",
                     font=ctk.CTkFont("Segoe UI", 12, "bold"),
                     text_color=WARNING).pack(anchor="w", padx=16, pady=(12, 4))
        for tip in [
            "Book train on IRCTC 60 days ahead — cheapest fares available early",
            "Stay at Zostel or Moustache hostels — great vibes, cheapest beds",
            "Eat at dhabas & street stalls — same taste, 3× cheaper",
            "Travel midweek — weekend prices are always inflated",
            "Student ID cards can unlock 25–50% off at major monuments",
        ]:
            ctk.CTkLabel(tips_card, text=f"  ✅  {tip}",
                         font=ctk.CTkFont("Segoe UI", 10),
                         text_color=TEXT_SEC, anchor="w",
                         wraplength=520).pack(anchor="w", padx=16, pady=1)
        ctk.CTkFrame(tips_card, fg_color="transparent", height=10).pack()


# ════════════════════════════════════════════════════════════════
#  DESTINATION INFO TAB
# ════════════════════════════════════════════════════════════════
class DestInfoTab(ctk.CTkFrame):
    def __init__(self, master, **kw):
        kw.setdefault("fg_color", BG_DARK)
        super().__init__(master, **kw)
        self._current = None
        SectionHeader(self, "Destination Guide", "📍",
                      subtitle="Tap a destination card on Home to load details"
                      ).pack(fill="x")
        self.placeholder = ctk.CTkLabel(
            self, text="Select a destination card from the Home screen.",
            font=ctk.CTkFont("Segoe UI", 13), text_color=TEXT_SEC)
        self.placeholder.pack(expand=True)
        self._panel = None

    def show_destination(self, dest_name: str):
        if dest_name == self._current:
            return
        self._current = dest_name
        self.placeholder.pack_forget()
        if self._panel:
            self._panel.destroy()

        scroll = ScrollableFrame(self)
        scroll.pack(fill="both", expand=True, padx=16, pady=12)
        self._panel = scroll

        data = DESTINATIONS[dest_name]
        InfoPanel(scroll, dest_name).pack(fill="x", pady=(0, 12))

        # Activities
        act = ctk.CTkFrame(scroll, fg_color=BG_CARD, corner_radius=14,
                           border_width=1, border_color=BORDER)
        act.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(act, text="🎯  Activities & Costs",
                     font=ctk.CTkFont("Segoe UI", 12, "bold"),
                     text_color=ACCENT2).pack(anchor="w", padx=14, pady=(10, 4))
        for item in data.get("activities", []):
            ctk.CTkLabel(act, text=f"  ›  {item}",
                         font=ctk.CTkFont("Segoe UI", 10),
                         text_color=TEXT_SEC, anchor="w",
                         wraplength=480).pack(anchor="w", padx=14)
        ctk.CTkFrame(act, fg_color="transparent", height=8).pack()

        # Student tips
        tips = ctk.CTkFrame(scroll, fg_color=BG_CARD, corner_radius=14,
                            border_width=1, border_color=BORDER)
        tips.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(tips, text="🎒  Student Tips",
                     font=ctk.CTkFont("Segoe UI", 12, "bold"),
                     text_color=SUCCESS).pack(anchor="w", padx=14, pady=(10, 4))
        for tip in data.get("student_tips", []):
            ctk.CTkLabel(tips, text=f"  ✅  {tip}",
                         font=ctk.CTkFont("Segoe UI", 10),
                         text_color=TEXT_PRI, anchor="w",
                         wraplength=480).pack(anchor="w", padx=14, pady=1)
        ctk.CTkFrame(tips, fg_color="transparent", height=8).pack()


# ════════════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ════════════════════════════════════════════════════════════════
class TravelPlannerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_ICON} {APP_NAME} — Trip Saver")
        self.geometry("1150x740")
        self.minsize(900, 600)
        self.configure(fg_color=BG_DARK)
        self._build()

    def _build(self):
        # ── Sidebar ──────────────────────────────────────────
        sb = ctk.CTkFrame(self, width=210, fg_color=BG_GLASS, corner_radius=0)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)
        ctk.CTkFrame(sb, fg_color=ACCENT, width=3, corner_radius=0
                     ).place(x=0, y=0, relheight=1)

        # Logo
        logo = ctk.CTkFrame(sb, fg_color="transparent")
        logo.pack(pady=(30, 4), padx=16)
        ctk.CTkLabel(logo, text=APP_ICON,
                     font=ctk.CTkFont("Segoe UI", 42)).pack()
        ctk.CTkLabel(logo, text=APP_NAME,
                     font=ctk.CTkFont("Segoe UI", 18, "bold"),
                     text_color=ACCENT).pack()
        ctk.CTkLabel(logo, text="for Students",
                     font=ctk.CTkFont("Segoe UI", 10),
                     text_color=TEXT_SEC).pack()
        Divider(sb).pack(fill="x", padx=14, pady=16)

        self._nav_btns: dict[str, ctk.CTkButton] = {}
        nav = [
            ("🏠", "Home",        self.show_home),
            ("🗺️", "Plan Trip",   self.show_planner),
            ("📋", "Itinerary",   self.show_itinerary),
            ("💰", "Budget",      self.show_budget),
            ("📍", "Destination", self.show_dest),
        ]
        for icon, label, cmd in nav:
            btn = ctk.CTkButton(
                sb, text=f"  {icon}  {label}",
                command=cmd,
                fg_color="transparent", hover_color=BG_INPUT,
                text_color=TEXT_SEC, anchor="w",
                font=ctk.CTkFont("Segoe UI", 13),
                corner_radius=8, height=42)
            btn.pack(fill="x", padx=10, pady=2)
            self._nav_btns[label] = btn

        # Version
        Divider(sb).pack(fill="x", padx=14, pady=16, side="bottom")
        ctk.CTkLabel(sb, text="Powered by Groq API",
                     font=ctk.CTkFont("Segoe UI", 9),
                     text_color=TEXT_SEC).pack(side="bottom", pady=(0, 6))
        ctk.CTkLabel(sb, text="v2.0  •  Trip Saver",
                     font=ctk.CTkFont("Segoe UI", 9),
                     text_color=TEXT_SEC).pack(side="bottom", pady=0)

        # ── Content ──────────────────────────────────────────
        self.content = ctk.CTkFrame(self, fg_color=BG_DARK, corner_radius=0)
        self.content.pack(side="left", fill="both", expand=True)

        self.tab_home  = HomeTab(self.content,     on_dest_select=self._on_card)
        self.tab_plan  = PlannerTab(self.content,  on_generate=self._generate)
        self.tab_itin  = ItineraryTab(self.content)
        self.tab_bdgt  = BudgetTab(self.content)
        self.tab_dest  = DestInfoTab(self.content)

        self.show_home()

    # ── Nav ──────────────────────────────────────────────────
    def _switch(self, tab, name):
        for t in [self.tab_home, self.tab_plan, self.tab_itin,
                  self.tab_bdgt, self.tab_dest]:
            t.pack_forget()
        tab.pack(fill="both", expand=True)
        for n, btn in self._nav_btns.items():
            if n == name:
                btn.configure(fg_color=BG_INPUT, text_color=ACCENT)
            else:
                btn.configure(fg_color="transparent", text_color=TEXT_SEC)

    def show_home(self):      self._switch(self.tab_home, "Home")
    def show_planner(self):   self._switch(self.tab_plan, "Plan Trip")
    def show_itinerary(self): self._switch(self.tab_itin, "Itinerary")
    def show_budget(self):    self._switch(self.tab_bdgt, "Budget")
    def show_dest(self):      self._switch(self.tab_dest, "Destination")

    def _on_card(self, dest_name):
        self.tab_dest.show_destination(dest_name)
        self.tab_plan.set_destination(dest_name)
        self.show_dest()

    # ── Generate ────────────────────────────────────────────
    def _generate(self, destination, duration, budget, group_size,
                  travel_style, departure, preferences, budget_tier):

        # Instant budget estimate
        bdata = estimate_budget(destination, duration, budget_tier,
                                group_size, departure)
        self.tab_bdgt.update_budget(bdata)
        self.tab_dest.show_destination(destination)

        # Show loading
        self.tab_itin.show_loading()
        self.show_itinerary()

        def _worker():
            had_error = False
            chunks_received = [False]

            def on_chunk(chunk):
                chunks_received[0] = True
                self.after(0, lambda c=chunk: self.tab_itin.stream_chunk(c))

            result = generate_itinerary(
                api_key=API_KEY,
                destination=destination,
                duration=duration,
                budget_per_person=budget,
                group_size=group_size,
                travel_style=travel_style,
                departure_city=departure,
                preferences=preferences,
                stream_callback=on_chunk,
            )
            if result.startswith("❌"):
                had_error = True
                self.after(0, lambda: self.tab_itin.stream_chunk(
                    f"\n\n{result}"))
            self.after(0, lambda: self.tab_itin.show_done(had_error))

        threading.Thread(target=_worker, daemon=True).start()


# ════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = TravelPlannerApp()
    app.mainloop()
