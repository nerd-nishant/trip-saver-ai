"""
ui_components.py — Professional UI widgets for Trip Saver
Modern, aesthetic dark design with saffron + gold + midnight palette.
"""

import tkinter as tk
import customtkinter as ctk
import webbrowser
from destinations import DESTINATIONS

# ── Premium Colour Palette ───────────────────────────────────────
BG_DARK    = "#0a0e1a"    # deep midnight navy
BG_CARD    = "#111827"    # dark card
BG_INPUT   = "#1a2235"    # input fields
BG_GLASS   = "#151f2e"    # glassmorphism panel
ACCENT     = "#f97316"    # saffron-orange (India flag)
ACCENT2    = "#6366f1"    # indigo-purple
GOLD       = "#fbbf24"    # gold / turmeric
TEXT_PRI   = "#f1f5f9"    # near-white
TEXT_SEC   = "#64748b"    # muted slate
SUCCESS    = "#10b981"    # emerald green
WARNING    = "#f59e0b"    # amber
DANGER     = "#ef4444"    # red
BORDER     = "#1e293b"    # subtle border
BORDER_LIT = "#334155"    # lit border on hover
TEAL       = "#14b8a6"    # teal accent
PINK       = "#ec4899"    # pink accent

FONT_HEADING  = ("Segoe UI", 18, "bold")
FONT_SUBHEAD  = ("Segoe UI", 13, "bold")
FONT_BODY     = ("Segoe UI", 11)
FONT_SMALL    = ("Segoe UI", 10)
FONT_MONO     = ("Consolas", 12)
FONT_HERO     = ("Segoe UI", 30, "bold")


class ScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kw):
        kw.setdefault("fg_color", BG_DARK)
        kw.setdefault("scrollbar_button_color", ACCENT)
        kw.setdefault("scrollbar_button_hover_color", "#ea580c")
        super().__init__(master, **kw)


class Divider(ctk.CTkFrame):
    def __init__(self, master, color=BORDER_LIT, **kw):
        kw.setdefault("fg_color", color)
        kw.setdefault("height", 1)
        super().__init__(master, **kw)


class SectionHeader(ctk.CTkFrame):
    def __init__(self, master, title: str, emoji: str = "", subtitle: str = "", **kw):
        kw.setdefault("fg_color", BG_GLASS)
        kw.setdefault("corner_radius", 0)
        super().__init__(master, **kw)

        inner = ctk.CTkFrame(self, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=12)

        left = ctk.CTkFrame(inner, fg_color="transparent")
        left.pack(side="left")

        # Accent bar
        ctk.CTkFrame(left, fg_color=ACCENT, width=4, corner_radius=2).pack(
            side="left", fill="y", padx=(0, 10))

        text_col = ctk.CTkFrame(left, fg_color="transparent")
        text_col.pack(side="left")
        ctk.CTkLabel(
            text_col,
            text=f"{emoji}  {title}" if emoji else title,
            font=ctk.CTkFont(*FONT_HEADING),
            text_color=TEXT_PRI,
        ).pack(anchor="w")
        if subtitle:
            ctk.CTkLabel(
                text_col, text=subtitle,
                font=ctk.CTkFont(*FONT_SMALL),
                text_color=TEXT_SEC,
            ).pack(anchor="w")


class GlowButton(ctk.CTkButton):
    """Accent button with hover glow effect."""
    def __init__(self, master, **kw):
        kw.setdefault("fg_color", ACCENT)
        kw.setdefault("hover_color", "#ea580c")
        kw.setdefault("text_color", "#ffffff")
        kw.setdefault("font", ctk.CTkFont("Segoe UI", 13, "bold"))
        kw.setdefault("corner_radius", 10)
        kw.setdefault("height", 44)
        super().__init__(master, **kw)


class DestinationCard(ctk.CTkFrame):
    """Premium clickable destination card."""
    def __init__(self, master, dest_name: str, on_click, **kw):
        data = DESTINATIONS[dest_name]
        kw.setdefault("fg_color", BG_CARD)
        kw.setdefault("corner_radius", 14)
        kw.setdefault("border_width", 1)
        kw.setdefault("border_color", BORDER)
        super().__init__(master, **kw)

        color = data["color"]

        def _enter(e):
            self.configure(border_color=color)
            emoji_lbl.configure(text_color=color)

        def _leave(e):
            self.configure(border_color=BORDER)
            emoji_lbl.configure(text_color=TEXT_PRI)

        def _click(e):
            on_click(dest_name)

        self.bind("<Button-1>", _click)
        self.bind("<Enter>", _enter)
        self.bind("<Leave>", _leave)

        # Top: emoji + badge
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=14, pady=(14, 2))

        emoji_lbl = ctk.CTkLabel(
            top, text=data["emoji"],
            font=ctk.CTkFont("Segoe UI", 32),
            text_color=TEXT_PRI)
        emoji_lbl.pack(side="left")

        # Budget pill
        b = data["avg_budget_per_day"]["budget"]
        pill = ctk.CTkFrame(top, fg_color=BG_INPUT, corner_radius=20)
        pill.pack(side="right", padx=4)
        ctk.CTkLabel(pill, text=f"₹{b}/day",
                     font=ctk.CTkFont("Segoe UI", 10, "bold"),
                     text_color=SUCCESS).pack(padx=8, pady=3)

        # Name
        ctk.CTkLabel(
            self, text=dest_name,
            font=ctk.CTkFont("Segoe UI", 14, "bold"),
            text_color=TEXT_PRI, anchor="w",
        ).pack(padx=14, anchor="w", pady=(4, 0))

        # Tagline
        ctk.CTkLabel(
            self, text=data["tagline"],
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=TEXT_SEC, anchor="w",
            wraplength=210,
        ).pack(padx=14, anchor="w", pady=(2, 6))

        # Bottom info bar
        bar = ctk.CTkFrame(self, fg_color=BG_INPUT, corner_radius=8)
        bar.pack(fill="x", padx=10, pady=(0, 12))
        ctk.CTkLabel(bar, text=f"📍 {data['state']}",
                     font=ctk.CTkFont("Segoe UI", 10),
                     text_color=TEXT_SEC).pack(side="left", padx=8, pady=5)
        ctk.CTkLabel(bar, text=f"🗓 {data['best_time']}",
                     font=ctk.CTkFont("Segoe UI", 10),
                     text_color=color).pack(side="right", padx=8, pady=5)

        # Bind all children
        def _bind_all(w):
            w.bind("<Button-1>", _click)
            w.bind("<Enter>", _enter)
            w.bind("<Leave>", _leave)
            for c in w.winfo_children():
                _bind_all(c)
        _bind_all(self)


class InfoPanel(ctk.CTkFrame):
    """Rich destination info sidebar."""
    def __init__(self, master, dest_name: str, **kw):
        kw.setdefault("fg_color", BG_CARD)
        kw.setdefault("corner_radius", 14)
        kw.setdefault("border_width", 1)
        kw.setdefault("border_color", BORDER)
        super().__init__(master, **kw)
        data = DESTINATIONS[dest_name]
        color = data["color"]

        # Hero row
        hero = ctk.CTkFrame(self, fg_color=BG_INPUT, corner_radius=10)
        hero.pack(fill="x", padx=12, pady=(12, 8))
        ctk.CTkLabel(hero, text=data["emoji"],
                     font=ctk.CTkFont("Segoe UI", 36)).pack(side="left", padx=12, pady=10)
        txt = ctk.CTkFrame(hero, fg_color="transparent")
        txt.pack(side="left", pady=10)
        ctk.CTkLabel(txt, text=dest_name,
                     font=ctk.CTkFont("Segoe UI", 16, "bold"),
                     text_color=color).pack(anchor="w")
        ctk.CTkLabel(txt, text=data["tagline"],
                     font=ctk.CTkFont("Segoe UI", 10),
                     text_color=TEXT_SEC).pack(anchor="w")

        ctk.CTkLabel(
            self, text=data["description"],
            font=ctk.CTkFont(*FONT_SMALL),
            text_color=TEXT_SEC, wraplength=300, justify="left",
        ).pack(padx=12, pady=(0, 8))

        self._section("📍 Must-Visit", data["places"][:5], color)
        self._section("🍛 Food Spots", data["food_spots"][:4], GOLD)

        b = data["avg_budget_per_day"]
        ctk.CTkLabel(
            self,
            text=f"Budget: ₹{b['budget']}/d  •  Mid: ₹{b['mid']}/d  •  Premium: ₹{b['premium']}/d",
            font=ctk.CTkFont("Segoe UI", 10, "bold"),
            text_color=WARNING,
        ).pack(padx=12, pady=(4, 8))

        GlowButton(
            self, text="🗺️  Open in Google Maps",
            command=lambda: webbrowser.open(data["maps_url"]),
            fg_color=ACCENT2, hover_color="#4f46e5",
            height=36, corner_radius=8,
        ).pack(padx=12, pady=(0, 12), fill="x")

    def _section(self, title, items, color):
        ctk.CTkLabel(self, text=title,
                     font=ctk.CTkFont("Segoe UI", 11, "bold"),
                     text_color=color).pack(padx=12, anchor="w", pady=(4, 2))
        for item in items:
            ctk.CTkLabel(self, text=f"  ›  {item}",
                         font=ctk.CTkFont(*FONT_SMALL),
                         text_color=TEXT_SEC, anchor="w").pack(padx=12, anchor="w")
        Divider(self).pack(fill="x", padx=12, pady=6)


class BudgetBar(ctk.CTkFrame):
    def __init__(self, master, label, amount, total, color, **kw):
        kw.setdefault("fg_color", "transparent")
        super().__init__(master, **kw)
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text=label, font=ctk.CTkFont(*FONT_SMALL),
                     text_color=TEXT_PRI, anchor="w").grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(self, text=f"₹{amount:,}",
                     font=ctk.CTkFont("Segoe UI", 11, "bold"),
                     text_color=color).grid(row=0, column=1, sticky="e")

        pct = min(int((amount / total) * 100), 100) if total else 2
        outer = ctk.CTkFrame(self, fg_color=BORDER, height=6, corner_radius=3)
        outer.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(2, 8))
        outer.grid_propagate(False)
        inner = ctk.CTkFrame(outer, fg_color=color, height=6, corner_radius=3)
        inner.place(relwidth=max(pct / 100, 0.02), relheight=1.0)
