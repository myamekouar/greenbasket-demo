# ─────────────────────────────────────────────────────────────────────────────
# GreenBasket · Shopper Intelligence Demo
# Catalina Hackathon — Omnichannel Activation & Gamification Platform
# Run: streamlit run demo_app.py
# ─────────────────────────────────────────────────────────────────────────────

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GreenBasket · Catalina",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Colour palette ────────────────────────────────────────────────────────────
C_BLUE  = "#004A97"
C_RED   = "#CC0000"
C_GREEN = "#2E7D32"
C_AMBER = "#F57F17"
C_LTBL  = "#E8F1FB"

# ── Lookup tables ─────────────────────────────────────────────────────────────
TIER_COL = {"Bronze": "#B87333", "Silver": "#757575",
            "Gold": "#F9A825", "Platinum": "#455A64"}
SEG_ICON = {"Premium Loyal": "💎", "Regular Engaged": "⭐", "Occasional": "🌱"}
CH_ICON  = {
    "App Push Notification": "📱", "Email Campaign": "📧",
    "In-Store Coupon": "🏪",       "E-commerce Banner": "🛒",
    "Weekend Email": "📧",          "In-Store Flyer": "📄",
    "Email + App Push": "📱📧",     "App Challenge": "🏆",
}
BADGE_COL = {"A": "#038141", "B": "#85BB2F", "C": "#FFCC00",
             "D": "#EE8100", "E": "#E63312"}
BADGE_ICON = {
    "Green Champion": "🌿", "Planet Saver": "🌍", "Loyal Explorer": "⭐",
    "Family Hero": "👨‍👩‍👧", "First Steps": "🌱", "Sporty Shopper": "🏃",
    "E-shopper": "📱", "Bulk Buyer": "📦", "Foodie Explorer": "🍴",
}

PERSONA_META = {
    "Health Pioneer": {
        "icon": "🥦",
        "desc": "Actively gravitating toward healthier products. Strong preference for fresh, organic, and minimally-processed foods across multiple weekly visits.",
        "motivation": "Personal wellbeing and family health outcomes.",
        "opportunity": "Double-points missions on fresh & organic categories drive strong engagement and basket upgrading.",
    },
    "Eco Explorer": {
        "icon": "🌍",
        "desc": "Sustainability-driven shopper with a rising share of eco-certified and plant-based products. High e-commerce usage.",
        "motivation": "Minimising environmental footprint and ethical consumption.",
        "opportunity": "Eco Challenge campaigns and carbon-neutral swap missions resonate strongly with this profile.",
    },
    "Family Organiser": {
        "icon": "👨‍👩‍👧",
        "desc": "High-spend shopper focused on value and convenience for a busy household. Large baskets, weekend-concentrated visits.",
        "motivation": "Feeding the family efficiently without sacrificing quality.",
        "opportunity": "Family bundle promos and bulk-buy rewards deliver strong basket size uplift.",
    },
    "Smart Saver": {
        "icon": "💰",
        "desc": "Price-sensitive shopper who responds strongly to promotional mechanics. In-store only, low frequency.",
        "motivation": "Maximising value on a tight budget.",
        "opportunity": "Simple in-store price promotions and bundle offers are the most effective activation lever.",
    },
    "Routine Loyalist": {
        "icon": "🔁",
        "desc": "Habitual shopper with predictable but infrequent visits. Low offer engagement but shows upgrade potential.",
        "motivation": "Continuity, familiarity, and convenience.",
        "opportunity": "Loyalty bonus emails and reactivation campaigns can unlock latent frequency uplift.",
    },
    "Weekend Foodie": {
        "icon": "🍷",
        "desc": "Concentrated shopper — high basket value concentrated on weekends. Premium fresh and gourmet categories.",
        "motivation": "Quality, experience, and food discovery.",
        "opportunity": "Exclusive weekend deals on premium categories drive premium basket trade-up.",
    },
    "Budget-Conscious": {
        "icon": "🧾",
        "desc": "Early-stage shopper in discovery phase. Low spend, curious about products, strong growth potential.",
        "motivation": "Exploring options without overspending.",
        "opportunity": "Gamified product discovery challenges drive trial and habit formation.",
    },
    "Eco-Progressive": {
        "icon": "♻️",
        "desc": "Mid-journey sustainability shopper progressively upgrading to greener choices. High digital engagement.",
        "motivation": "Making progressively better environmental choices.",
        "opportunity": "Seasonal challenges and eco-progress tracking accelerate the transition to greener baskets.",
    },
}

CATEGORY_PROFILES = {
    "Health Pioneer":   [("Fresh Produce", 32), ("Dairy & Eggs", 18), ("Beverages", 14), ("Bakery", 12), ("Snacks", 8),  ("Other", 16)],
    "Eco Explorer":     [("Plant-Based",   28), ("Fresh Produce", 22), ("Beverages", 18), ("Dairy & Eggs", 15), ("Other", 17)],
    "Family Organiser": [("Frozen & Ready",30), ("Dairy & Eggs", 20), ("Bakery", 15),    ("Snacks", 12), ("Other", 23)],
    "Smart Saver":      [("Frozen & Ready",28), ("Snacks", 20),       ("Beverages", 15), ("Bakery", 15), ("Other", 22)],
    "Routine Loyalist": [("Deli & Cheese", 25), ("Wine & Spirits", 20),("Bakery", 18),   ("Dairy & Eggs", 17), ("Other", 20)],
    "Weekend Foodie":   [("Fresh Meat & Fish",30),("Wine & Spirits",20),("Fresh Produce",18),("Dairy & Eggs",12),("Other",20)],
    "Budget-Conscious": [("Frozen & Ready",25), ("Bakery", 22),       ("Beverages", 18), ("Snacks", 15), ("Other", 20)],
    "Eco-Progressive":  [("Plant-Based",   25), ("Fresh Produce", 25), ("Beverages", 15), ("Dairy & Eggs", 12), ("Other", 23)],
}

PRODUCT_RECS = {
    "Health Pioneer": [
        {"name": "Organic Spinach", "brand": "Bio Village",   "icon": "🥬", "pts": 50, "tag": "Organic"},
        {"name": "Greek Yoghurt",   "brand": "Nature's Best", "icon": "🥛", "pts": 40, "tag": "High Protein"},
        {"name": "Avocados x2",     "brand": "Fresh Select",  "icon": "🥑", "pts": 45, "tag": "Superfood"},
        {"name": "Blueberries",     "brand": "Berry Farm",    "icon": "🫐", "pts": 35, "tag": "Antioxidant"},
    ],
    "Eco Explorer": [
        {"name": "Oat Milk 1L",       "brand": "Oatly",       "icon": "🌾", "pts": 60, "tag": "Plant-Based"},
        {"name": "Organic Tofu",      "brand": "Clearspring", "icon": "🫘", "pts": 55, "tag": "Vegan"},
        {"name": "Eco Washing Tabs",  "brand": "EcoHome",     "icon": "♻️", "pts": 80, "tag": "Zero Waste"},
        {"name": "Hemp Seeds",        "brand": "Naturgreen",  "icon": "🌿", "pts": 45, "tag": "Eco-Certified"},
    ],
    "Family Organiser": [
        {"name": "Family Lasagne",  "brand": "Barilla",    "icon": "🍝", "pts": 60, "tag": "Family Pack"},
        {"name": "Orange Juice 2L", "brand": "Tropicana",  "icon": "🍊", "pts": 40, "tag": "Value Pack"},
        {"name": "Cheese Selection","brand": "Président",  "icon": "🧀", "pts": 55, "tag": "Bundle"},
        {"name": "Frozen Veg Mix",  "brand": "Bonduelle",  "icon": "🥦", "pts": 35, "tag": "Family Size"},
    ],
    "Smart Saver": [
        {"name": "Own-Brand Pasta",  "brand": "Carrefour", "icon": "🍝", "pts": 30, "tag": "Best Value"},
        {"name": "Canned Tomatoes",  "brand": "Carrefour", "icon": "🥫", "pts": 25, "tag": "Buy 2 Get 1"},
        {"name": "Frozen Ready Meal","brand": "Carrefour", "icon": "🍱", "pts": 35, "tag": "Budget Pick"},
        {"name": "Own-Brand Cereal", "brand": "Carrefour", "icon": "🥣", "pts": 20, "tag": "Everyday Low"},
    ],
    "Routine Loyalist": [
        {"name": "Comté 200g",    "brand": "Président",     "icon": "🧀", "pts": 40, "tag": "Your Usual"},
        {"name": "Bordeaux Rouge","brand": "Baron de Leys", "icon": "🍷", "pts": 60, "tag": "Favourite"},
        {"name": "Fresh Baguette","brand": "Boulangerie",   "icon": "🥖", "pts": 20, "tag": "Daily Pick"},
        {"name": "Butter 250g",   "brand": "Président",     "icon": "🧈", "pts": 25, "tag": "Your Usual"},
    ],
    "Weekend Foodie": [
        {"name": "Salmon Fillet", "brand": "Fresh Ocean",  "icon": "🐟", "pts": 80, "tag": "Premium"},
        {"name": "Prosecco 75cl", "brand": "Canella",      "icon": "🥂", "pts": 70, "tag": "Weekend Special"},
        {"name": "Truffle Oil",   "brand": "Urbani",       "icon": "🫙", "pts": 90, "tag": "Gourmet"},
        {"name": "Wagyu Beef",    "brand": "Select Cuts",  "icon": "🥩", "pts": 100,"tag": "Chef's Pick"},
    ],
    "Budget-Conscious": [
        {"name": "Oat Porridge",    "brand": "Quaker",     "icon": "🥣", "pts": 20, "tag": "Try It"},
        {"name": "Mixed Salad",     "brand": "Fresh Farm", "icon": "🥗", "pts": 25, "tag": "Discover"},
        {"name": "Greek Yoghurt",   "brand": "Fage",       "icon": "🥛", "pts": 20, "tag": "New to You"},
        {"name": "Wholegrain Bread","brand": "Harry's",    "icon": "🍞", "pts": 15, "tag": "Healthy Pick"},
    ],
    "Eco-Progressive": [
        {"name": "Oat Milk 1L",      "brand": "Oatly",       "icon": "🌾", "pts": 55, "tag": "Swap & Save"},
        {"name": "Lentil Soup",      "brand": "Bjorg",        "icon": "🫘", "pts": 45, "tag": "Eco-Swap"},
        {"name": "Bamboo Toothbrush","brand": "WooBamboo",    "icon": "🌿", "pts": 70, "tag": "Green Choice"},
        {"name": "Plant Burger",     "brand": "Beyond Meat",  "icon": "🌱", "pts": 60, "tag": "CO₂ Saved"},
    ],
}

VALIDITY_MAP = {
    "Weekend": "Valid this weekend only",
    "Saturday": "Valid this Saturday only",
    "Saturday Afternoon": "Valid this Saturday only",
    "Sunday": "Valid this Sunday only",
    "Weekday Morning": "Valid Mon–Fri, until 12pm",
    "Monday Morning": "Valid this Monday morning",
    "Tuesday Morning": "Valid this Tuesday morning",
    "Wednesday": "Valid this Wednesday",
    "Wednesday Evening": "Valid Wed evening",
    "Thursday": "Valid this Thursday",
    "Friday": "Valid this Friday",
    "Friday Evening": "Valid Fri–Sat evening",
    "Morning": "Valid weekday mornings",
    "Weekend Morning": "Valid Sat–Sun, until 12pm",
}

# ── Helpers ───────────────────────────────────────────────────────────────────
def score_col(v):
    return C_GREEN if v >= 70 else (C_AMBER if v >= 50 else C_RED)

def html_card(label, value, color=C_BLUE, sub=None):
    sub_part = f'<div style="font-size:11px;color:#aaa;margin-top:4px">{sub}</div>' if sub else ""
    return (
        f'<div style="background:#fff;border-radius:10px;padding:18px 16px;'
        f'box-shadow:0 2px 10px rgba(0,0,0,.07);border-top:4px solid {color};'
        f'text-align:center;height:100%">'
        f'<div style="font-size:10px;color:#999;text-transform:uppercase;'
        f'letter-spacing:1px;margin-bottom:8px">{label}</div>'
        f'<div style="font-size:26px;font-weight:900;color:{color};line-height:1.1">{value}</div>'
        f'{sub_part}</div>'
    )

def section_title(text):
    st.markdown(
        f'<div style="font-size:11px;font-weight:700;text-transform:uppercase;'
        f'letter-spacing:2px;color:{C_BLUE};margin:28px 0 14px;'
        f'padding-bottom:8px;border-bottom:2px solid {C_LTBL}">'
        f'{text}</div>',
        unsafe_allow_html=True,
    )

# ── Charts ────────────────────────────────────────────────────────────────────
def radar_chart(row):
    tier_score = {"Bronze": 25, "Silver": 50, "Gold": 75, "Platinum": 95}.get(
        row["loyalty_tier"], 50
    )
    freq_score   = min(round(row["visits_per_month"] / 12 * 100), 100)
    engage_score = min(row["streak_weeks"] * 9 + 20, 100)
    categories   = ["Health", "Sustain-<br>ability", "Frequency",
                    "Engage-<br>ment", "E-com", "Loyalty"]
    values       = [
        row["health_score"], row["sustainability_score"],
        freq_score, engage_score, row["pct_ecommerce"], tier_score,
    ]
    values     += [values[0]]
    categories += [categories[0]]
    fig = go.Figure(go.Scatterpolar(
        r=values, theta=categories,
        fill="toself",
        fillcolor="rgba(0,74,151,0.18)",
        line=dict(color=C_BLUE, width=2.5),
        marker=dict(color=C_BLUE, size=6),
        hovertemplate="%{theta}: %{r}<extra></extra>",
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=False, range=[0, 100]),
            angularaxis=dict(
                tickfont=dict(size=11, color="#555", family="Segoe UI, Arial"),
                linecolor="#ddd", gridcolor="#ddd",
            ),
            gridshape="linear",
            bgcolor="#F8F9FA",
        ),
        showlegend=False,
        margin=dict(l=44, r=44, t=32, b=32),
        paper_bgcolor="white",
        height=270,
    )
    return fig

def channel_donut(row):
    ec  = row["pct_ecommerce"]
    cc  = min(ec * 0.3, 8)
    sto = round(100 - ec - cc, 1)
    fig = go.Figure(go.Pie(
        labels=["In-Store", "E-commerce", "Click & Collect"],
        values=[sto, ec, cc],
        hole=0.62,
        marker=dict(colors=[C_BLUE, C_RED, C_AMBER],
                    line=dict(color="white", width=2)),
        textinfo="label+percent",
        textfont=dict(size=11, family="Segoe UI, Arial"),
        hovertemplate="%{label}: %{value:.1f}%<extra></extra>",
    ))
    fig.update_layout(
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="white",
        height=220,
    )
    return fig

def category_bar(row):
    cats   = CATEGORY_PROFILES.get(row["persona"], [("Other", 100)])
    labels = [c[0] for c in cats]
    values = [c[1] for c in cats]
    colors = [C_BLUE if i == 0 else f"rgba(0,74,151,{0.65 - i*0.1})" for i in range(len(labels))]
    fig = go.Figure(go.Bar(
        x=values, y=labels,
        orientation="h",
        marker_color=colors,
        text=[f"{v}%" for v in values],
        textposition="outside",
        textfont=dict(size=11, color="#555"),
        hovertemplate="%{y}: %{x}%<extra></extra>",
    ))
    fig.update_layout(
        xaxis=dict(visible=False, range=[0, max(values) * 1.3]),
        yaxis=dict(autorange="reversed", tickfont=dict(size=11, color="#444")),
        margin=dict(l=10, r=40, t=10, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        height=220,
        bargap=0.35,
    )
    return fig

def impact_chart(row):
    metrics = ["Engagement\nUplift", "Healthier\nBasket", "Sustainability\nGain", "Retention"]
    values  = [
        int(row["engagement_uplift_pct"].replace("+","").replace("%","")),
        int(row["health_shift_pct"].replace("+","").replace("%","")),
        int(row["sustainability_improvement_pct"].replace("+","").replace("%","")),
        int(row["retention_pct"].replace("%","")),
    ]
    colors = [C_GREEN, C_GREEN, "#43A047", C_BLUE]
    fig = go.Figure(go.Bar(
        x=metrics, y=values,
        marker_color=colors,
        text=[f"{v}%" for v in values],
        textposition="outside",
        textfont=dict(size=13, family="Segoe UI"),
        width=0.5,
    ))
    fig.add_hline(y=0, line_color="#ccc", line_width=1)
    fig.update_layout(
        xaxis=dict(tickfont=dict(size=11, color="#444")),
        yaxis=dict(range=[0, max(values) * 1.3], showgrid=True,
                   gridcolor="#F0F0F0", ticksuffix="%",
                   tickfont=dict(size=11, color="#aaa")),
        margin=dict(l=20, r=20, t=10, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        height=240,
        bargap=0.4,
    )
    return fig

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: "Segoe UI", Arial, sans-serif;
}
.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1080px !important;
}
/* Sidebar */
section[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg, #002f6c 0%, #004A97 100%);
    padding-top: 0;
}
/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
/* Plotly chart rounded corners */
.js-plotly-plot { border-radius: 10px; overflow: hidden; }
/* Tab styling */
button[data-baseweb="tab"] {
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: .5px !important;
    padding: 10px 24px !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #004A97 !important;
    border-bottom: 3px solid #004A97 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load():
    return pd.read_csv("demo_shopper_profiles.csv")

df = load()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="background:rgba(0,0,0,.25);padding:18px 16px 14px;margin-bottom:4px">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
        <div style="background:#CC0000;padding:5px 10px;border-radius:6px;
                    font-size:13px;font-weight:900;color:#fff;letter-spacing:.4px">Catalina</div>
        <div style="font-size:16px;font-weight:800;color:#fff">GreenBasket</div>
      </div>
      <div style="font-size:11px;color:rgba(255,255,255,.55);letter-spacing:.5px">
        Shopper Intelligence Demo
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="padding:12px 16px 4px;font-size:10px;color:rgba(255,255,255,.5);
                text-transform:uppercase;letter-spacing:1.2px;font-weight:600">
      Select Profile
    </div>
    """, unsafe_allow_html=True)

    opts = {
        f"{r['name']}  ·  {r['persona']}": r["shopper_id"]
        for _, r in df.sort_values(["segment", "persona"]).iterrows()
    }
    chosen_label = st.selectbox(
        "shopper", list(opts.keys()), label_visibility="collapsed"
    )
    row = df[df["shopper_id"] == opts[chosen_label]].iloc[0]

    st.markdown(
        '<div style="padding:8px 16px 16px;font-size:10px;'
        'color:rgba(255,255,255,.3);text-align:center">Synthetic data · Demo</div>',
        unsafe_allow_html=True,
    )

# ── HEADER (shared across both tabs) ─────────────────────────────────────────
_tc   = TIER_COL.get(row["loyalty_tier"], "#777")
_pbg, _pcol = {
    "Health Pioneer":   ("#E8F5E9", "#2E7D32"),
    "Eco Explorer":     ("#E0F2F1", "#00695C"),
    "Family Organiser": ("#E3F2FD", "#1565C0"),
    "Smart Saver":      ("#FFF8E1", "#E65100"),
    "Routine Loyalist": ("#F3E5F5", "#6A1B9A"),
    "Weekend Foodie":   ("#FFF3E0", "#BF360C"),
    "Budget-Conscious": ("#FFF8E1", "#BF360C"),
    "Eco-Progressive":  ("#E8F5E9", "#2E7D32"),
}.get(row["persona"], ("#E8F1FB", "#004A97"))

st.markdown(f"""
<div style="background:linear-gradient(135deg,#004A97 0%,#0066CC 100%);
            border-radius:12px;padding:22px 26px;margin-bottom:20px;
            display:flex;align-items:center;justify-content:space-between;
            box-shadow:0 4px 18px rgba(0,74,151,.3)">
  <div>
    <div style="font-size:10px;color:#A8C8F0;text-transform:uppercase;
                letter-spacing:2px;margin-bottom:5px">
      Catalina · GreenBasket Intelligence Demo
    </div>
    <div style="font-size:26px;font-weight:800;color:#fff;margin-bottom:10px">
      {row['name']}
    </div>
    <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
      <span style="background:{_pbg};color:{_pcol};padding:5px 14px;
                   border-radius:20px;font-size:13px;font-weight:700">
        ✦ {row['persona']}
      </span>
      <span style="background:rgba(255,255,255,.15);color:#fff;padding:5px 14px;
                   border-radius:20px;font-size:12px">
        {SEG_ICON.get(row['segment'], '')} {row['segment']}
      </span>
      <span style="background:{_tc};color:#fff;padding:5px 14px;
                   border-radius:20px;font-size:12px;font-weight:700">
        ⭐ {row['loyalty_tier']}
      </span>
    </div>
  </div>
  <div style="text-align:right;color:#fff;flex-shrink:0;margin-left:24px">
    <div style="font-size:11px;color:#A8C8F0;margin-bottom:2px">Age Group</div>
    <div style="font-size:20px;font-weight:700">{row['age_group']}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab_biz, tab_shop = st.tabs(["  Business View  ", "  Shopper View  "])

# ═════════════════════════════════════════════════════════════════════════════
# TAB 1 · BUSINESS VIEW
# ═════════════════════════════════════════════════════════════════════════════
with tab_biz:

    # ── SECTION 1 · SHOPPER PROFILE ──────────────────────────────────────────
    section_title("Shopper Profile")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(html_card("Annual Spend", f"€{row['total_spend']:,.0f}", C_BLUE,
                              f"{row['num_transactions'] if 'num_transactions' in row else '—'} transactions"), unsafe_allow_html=True)
    with c2:
        st.markdown(html_card("Avg Basket Value", f"€{row['avg_basket_value']:.1f}", C_RED), unsafe_allow_html=True)
    with c3:
        st.markdown(html_card("Visits / Month", f"{row['visits_per_month']}", C_GREEN,
                              f"{row['pct_ecommerce']}% online"), unsafe_allow_html=True)
    with c4:
        st.markdown(html_card("Points Balance", f"{row['points_balance']:,}", C_AMBER,
                              f"{row['points_to_next_reward']:,} to next reward"), unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.1, 1])

    with c1:
        st.markdown(
            '<div style="background:#fff;border-radius:10px;padding:16px 16px 8px;'
            'box-shadow:0 2px 10px rgba(0,0,0,.07)">'
            '<div style="font-size:11px;font-weight:700;color:#666;text-transform:uppercase;'
            'letter-spacing:1px;margin-bottom:2px">Channel Mix</div></div>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(channel_donut(row), use_container_width=True, config={"displayModeBar": False})

    with c2:
        st.markdown(
            '<div style="background:#fff;border-radius:10px;padding:16px 16px 8px;'
            'box-shadow:0 2px 10px rgba(0,0,0,.07)">'
            '<div style="font-size:11px;font-weight:700;color:#666;text-transform:uppercase;'
            'letter-spacing:1px;margin-bottom:2px">Category Preferences (% spend)</div></div>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(category_bar(row), use_container_width=True, config={"displayModeBar": False})

    with c3:
        nc  = BADGE_COL.get(str(row["nutri_score"]), "#aaa")
        ec  = BADGE_COL.get(str(row["eco_score"]),   "#aaa")
        hc  = C_AMBER
        sc2 = C_GREEN
        hs  = row["health_score"]
        ss  = row["sustainability_score"]
        streak_col = C_AMBER if row["streak_weeks"] > 0 else "#aaa"
        st.markdown(f"""
        <div style="background:#fff;border-radius:10px;padding:16px;
                    box-shadow:0 2px 10px rgba(0,0,0,.07);height:100%">
          <div style="font-size:11px;font-weight:700;color:{C_GREEN};text-transform:uppercase;
                      letter-spacing:1px;margin-bottom:12px">Health &amp; Sustainability</div>
          <div style="display:flex;gap:10px;align-items:flex-start;margin-bottom:14px">
            <div style="background:{nc};color:#fff;width:52px;height:52px;border-radius:10px;
                        display:flex;flex-direction:column;align-items:center;
                        justify-content:center;font-size:20px;font-weight:900;flex-shrink:0">
              {row['nutri_score']}<span style="font-size:7px;font-weight:400">NUTRI</span>
            </div>
            <div style="background:{ec};color:#fff;width:52px;height:52px;border-radius:10px;
                        display:flex;flex-direction:column;align-items:center;
                        justify-content:center;font-size:20px;font-weight:900;flex-shrink:0">
              {row['eco_score']}<span style="font-size:7px;font-weight:400">ECO</span>
            </div>
            <div style="font-size:11px;color:#666;line-height:1.8">
              <div style="font-size:10px;color:#aaa;margin-bottom:2px">Avg basket quality scores</div>
              <div>Top category: <strong style="color:#333">{row['top_category']}</strong></div>
              <div>E-commerce: <strong style="color:#333">{row['pct_ecommerce']}%</strong></div>
            </div>
          </div>
          <div style="margin-bottom:10px">
            <div style="display:flex;justify-content:space-between;
                        font-size:11px;color:#555;margin-bottom:4px">
              <span>Health Score</span>
              <span style="font-weight:700;color:{hc}">{hs}/100</span>
            </div>
            <div style="background:#F0F0F0;border-radius:6px;height:8px">
              <div style="width:{hs}%;height:8px;border-radius:6px;background:{hc}"></div>
            </div>
          </div>
          <div style="margin-bottom:14px">
            <div style="display:flex;justify-content:space-between;
                        font-size:11px;color:#555;margin-bottom:4px">
              <span>Sustainability Score</span>
              <span style="font-weight:700;color:{sc2}">{ss}/100</span>
            </div>
            <div style="background:#F0F0F0;border-radius:6px;height:8px">
              <div style="width:{ss}%;height:8px;border-radius:6px;background:{sc2}"></div>
            </div>
          </div>
          <div style="background:#FFF8E1;border-radius:8px;padding:8px 12px;font-size:12px;
                      font-weight:600;color:{streak_col};text-align:center">
            🔥 {row['streak_weeks']}-week healthy basket streak
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── SECTION 2 · PERSONA ──────────────────────────────────────────────────
    section_title("Shopper Persona")

    meta   = PERSONA_META.get(row["persona"], {})
    p_icon = meta.get("icon", "👤")
    p_bg, p_col = {
        "Health Pioneer":   ("#E8F5E9", C_GREEN),
        "Eco Explorer":     ("#E0F2F1", "#00695C"),
        "Family Organiser": ("#E3F2FD", "#1565C0"),
        "Smart Saver":      ("#FFF8E1", "#E65100"),
        "Routine Loyalist": ("#F3E5F5", "#6A1B9A"),
        "Weekend Foodie":   ("#FFF3E0", "#BF360C"),
        "Budget-Conscious": ("#FFF8E1", "#BF360C"),
        "Eco-Progressive":  ("#E8F5E9", C_GREEN),
    }.get(row["persona"], (C_LTBL, C_BLUE))

    col_p, col_r = st.columns([1.35, 1])

    with col_p:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{C_LTBL} 0%,#F0F7FF 100%);
                    border:1.5px solid #B3D1F0;border-radius:12px;padding:20px 24px;height:100%">
          <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px">
            <div style="background:{p_bg};color:{p_col};width:52px;height:52px;border-radius:12px;
                        font-size:26px;display:flex;align-items:center;justify-content:center;
                        flex-shrink:0">{p_icon}</div>
            <div>
              <div style="font-size:18px;font-weight:800;color:{C_BLUE}">{row['persona']}</div>
              <div style="margin-top:4px">
                <span style="background:{C_BLUE};color:#fff;padding:3px 10px;border-radius:20px;
                             font-size:11px;font-weight:600">{row['segment']}</span>
                &nbsp;
                <span style="background:{p_bg};color:{p_col};padding:3px 10px;border-radius:20px;
                             font-size:11px;font-weight:600;border:1px solid {p_col}33">
                  {row['age_group']}
                </span>
              </div>
            </div>
          </div>
          <div style="font-size:13px;color:#444;line-height:1.65;margin-bottom:12px">
            {meta.get('desc', '—')}
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
            <div style="background:rgba(255,255,255,.7);border-radius:8px;padding:10px 12px">
              <div style="font-size:10px;color:#999;text-transform:uppercase;
                          letter-spacing:1px;margin-bottom:3px">Motivation</div>
              <div style="font-size:12px;color:#333;line-height:1.5">{meta.get('motivation','—')}</div>
            </div>
            <div style="background:rgba(255,255,255,.7);border-radius:8px;padding:10px 12px">
              <div style="font-size:10px;color:#999;text-transform:uppercase;
                          letter-spacing:1px;margin-bottom:3px">Activation Opportunity</div>
              <div style="font-size:12px;color:#333;line-height:1.5">{meta.get('opportunity','—')}</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_r:
        st.markdown(
            '<div style="background:#fff;border-radius:12px;padding:16px 16px 4px;'
            'box-shadow:0 2px 10px rgba(0,0,0,.07)">'
            f'<div style="font-size:11px;font-weight:700;color:{C_BLUE};text-transform:uppercase;'
            'letter-spacing:1.5px;margin-bottom:0">Behavioural Profile</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(radar_chart(row), use_container_width=True, config={"displayModeBar": False})
        st.markdown(
            '<div style="text-align:center;font-size:11px;color:#aaa;margin-top:-18px;'
            'padding-bottom:6px">Multi-dimensional shopper behaviour analysis</div>',
            unsafe_allow_html=True,
        )

    # ── SECTION 3 · GAMIFIED REWARDS ─────────────────────────────────────────
    section_title("Rewards Journey")

    total_pts = row["points_balance"] + row["points_to_next_reward"]
    prog_pct  = int(row["points_balance"] / total_pts * 100)
    badges    = [str(row.get(b, "")) for b in ["badge_health", "badge_eco", "badge_loyalty"]]
    badges    = [b for b in badges if b not in ("", "nan")]

    col_r2, col_m = st.columns([1, 1.2])

    with col_r2:
        badge_html = "".join(
            f'<span style="background:{C_LTBL};color:{C_BLUE};padding:4px 12px;'
            f'border-radius:20px;font-size:12px;font-weight:600;margin:2px 3px;'
            f'display:inline-block;border:1px solid #B3D1F0">🏅 {b}</span>'
            for b in badges
        ) or f'<span style="color:#aaa;font-size:12px">No badges yet — start your journey!</span>'

        st.markdown(f"""
        <div style="background:#fff;border-radius:12px;padding:20px;
                    box-shadow:0 2px 10px rgba(0,0,0,.07)">
          <div style="display:flex;justify-content:space-between;align-items:center;
                      margin-bottom:6px">
            <span style="font-size:13px;color:#555;font-weight:500">Progress to next reward</span>
            <span style="font-size:15px;font-weight:900;color:{C_BLUE}">{prog_pct}%</span>
          </div>
          <div style="background:#E8EAED;border-radius:8px;height:14px;overflow:hidden;margin-bottom:5px">
            <div style="width:{prog_pct}%;height:14px;border-radius:8px;
                        background:linear-gradient(90deg,{C_BLUE},{C_BLUE}cc)"></div>
          </div>
          <div style="display:flex;justify-content:space-between;
                      font-size:11px;color:#aaa;margin-bottom:18px">
            <span>{row['points_balance']:,} pts accumulated</span>
            <span>{row['points_to_next_reward']:,} pts needed</span>
          </div>
          <div style="font-size:11px;font-weight:700;color:#666;
                      text-transform:uppercase;letter-spacing:1px;margin-bottom:8px">
            Earned Badges
          </div>
          <div>{badge_html}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_m:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{C_LTBL} 0%,#F0F7FF 100%);
                    border:1.5px solid #B3D1F0;border-radius:12px;padding:20px">
          <div style="font-size:11px;font-weight:700;color:{C_BLUE};text-transform:uppercase;
                      letter-spacing:1px;margin-bottom:12px">🎯 Active Mission</div>
          <div style="font-size:15px;font-weight:700;color:#333;margin-bottom:12px;line-height:1.5">
            {row['recommended_offer_text']}
          </div>
          <div style="background:white;border-radius:8px;padding:12px;
                      border-left:4px solid {C_AMBER}">
            <div style="font-size:11px;color:#999;margin-bottom:2px">Offer type</div>
            <div style="font-size:14px;font-weight:700;color:#333">
              🎁 {row['recommended_offer_type']}
            </div>
          </div>
          <div style="margin-top:12px;display:flex;gap:8px">
            <div style="flex:1;background:white;border-radius:8px;padding:10px;text-align:center">
              <div style="font-size:11px;color:#999;margin-bottom:2px">Streak</div>
              <div style="font-size:18px;font-weight:800;color:{C_AMBER}">
                🔥 {row['streak_weeks']}w
              </div>
            </div>
            <div style="flex:1;background:white;border-radius:8px;padding:10px;text-align:center">
              <div style="font-size:11px;color:#999;margin-bottom:2px">Total Points</div>
              <div style="font-size:18px;font-weight:800;color:{C_BLUE}">
                {row['points_balance']:,}
              </div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── SECTION 4 · OMNICHANNEL ACTIVATION ───────────────────────────────────
    section_title("Omnichannel Activation")

    ch_icon = CH_ICON.get(row["recommended_channel"], "📣")
    col_act, col_why = st.columns([1, 1.4])

    with col_act:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#FFF5F5 0%,#FFF0F0 100%);
                    border:1.5px solid #FFCDD2;border-left:5px solid {C_RED};
                    border-radius:12px;padding:20px">
          <div style="font-size:11px;color:#999;text-transform:uppercase;
                      letter-spacing:1px;margin-bottom:14px">Recommended Activation</div>
          <div style="margin-bottom:12px">
            <div style="font-size:10px;color:#aaa;text-transform:uppercase;
                        letter-spacing:1px;margin-bottom:4px">Channel</div>
            <div style="font-size:18px;font-weight:800;color:{C_RED}">
              {ch_icon} {row['recommended_channel']}
            </div>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px">
            <div style="background:rgba(255,255,255,.7);border-radius:8px;padding:10px">
              <div style="font-size:10px;color:#aaa;text-transform:uppercase;
                          letter-spacing:1px;margin-bottom:3px">Timing</div>
              <div style="font-size:13px;font-weight:700;color:#333">
                ⏰ {row['recommended_timing']}
              </div>
            </div>
            <div style="background:rgba(255,255,255,.7);border-radius:8px;padding:10px">
              <div style="font-size:10px;color:#aaa;text-transform:uppercase;
                          letter-spacing:1px;margin-bottom:3px">Offer type</div>
              <div style="font-size:13px;font-weight:700;color:#333">
                🎁 {row['recommended_offer_type']}
              </div>
            </div>
          </div>
          <div style="background:rgba(255,255,255,.8);border-radius:8px;padding:10px 12px">
            <div style="font-size:12px;color:#444;line-height:1.55">
              <strong style="color:#333">Message:</strong><br/>
              {row['recommended_offer_text']}
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_why:
        st.markdown(f"""
        <div style="background:#fff;border-radius:12px;padding:20px;
                    box-shadow:0 2px 10px rgba(0,0,0,.07);height:100%">
          <div style="font-size:11px;font-weight:700;color:#666;text-transform:uppercase;
                      letter-spacing:1px;margin-bottom:14px">Why this activation?</div>
          <div style="font-size:13px;color:#444;line-height:1.7;margin-bottom:16px">
            {row['activation_reason']}
          </div>
          <div style="background:{C_LTBL};border-radius:8px;padding:12px 14px">
            <div style="font-size:10px;color:{C_BLUE};font-weight:700;text-transform:uppercase;
                        letter-spacing:1px;margin-bottom:6px">Data signals used</div>
            <div style="display:flex;flex-wrap:wrap;gap:6px">
              <span style="background:white;color:{C_BLUE};padding:3px 10px;border-radius:20px;
                           font-size:11px;border:1px solid #B3D1F0">📊 Purchase frequency</span>
              <span style="background:white;color:{C_BLUE};padding:3px 10px;border-radius:20px;
                           font-size:11px;border:1px solid #B3D1F0">🛒 Channel preference</span>
              <span style="background:white;color:{C_BLUE};padding:3px 10px;border-radius:20px;
                           font-size:11px;border:1px solid #B3D1F0">🌿 Health trajectory</span>
              <span style="background:white;color:{C_BLUE};padding:3px 10px;border-radius:20px;
                           font-size:11px;border:1px solid #B3D1F0">🎯 Offer response history</span>
              <span style="background:white;color:{C_BLUE};padding:3px 10px;border-radius:20px;
                           font-size:11px;border:1px solid #B3D1F0">🏷️ Product Nutri/Eco scores</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── SECTION 5 · SIMULATED IMPACT ─────────────────────────────────────────
    section_title("Simulated Business Impact")

    st.markdown(
        '<div style="font-size:11px;color:#aaa;margin-top:-10px;margin-bottom:14px">'
        'Simulated model output — for demonstration purposes</div>',
        unsafe_allow_html=True,
    )

    ci1, ci2, ci3, ci4 = st.columns(4)
    impact_cards = [
        (ci1, "Engagement Uplift",    row["engagement_uplift_pct"],          C_GREEN,  "#F1F8F2"),
        (ci2, "Healthier Basket",     row["health_shift_pct"],               "#43A047", "#F1F8F2"),
        (ci3, "Sustainability Gain",  row["sustainability_improvement_pct"], "#66BB6A", "#F1F8F2"),
        (ci4, "Retention Likelihood", row["retention_pct"],                  C_BLUE,   "#F0F4FA"),
    ]
    for col, label, val, col_color, bg in impact_cards:
        with col:
            st.markdown(
                f'<div style="background:{bg};border-radius:10px;padding:18px;'
                f'text-align:center;border-bottom:3px solid {col_color}">'
                f'<div style="font-size:28px;font-weight:900;color:{col_color}">{val}</div>'
                f'<div style="font-size:11px;color:#555;margin-top:5px">{label}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.plotly_chart(impact_chart(row), use_container_width=True, config={"displayModeBar": False})

    st.markdown("""
    <div style="text-align:center;font-size:11px;color:#ccc;
                padding:20px 0 4px;border-top:1px solid #eee;margin-top:8px">
      Catalina Shopper Intelligence · GreenBasket Demo ·
      Synthetic data for presentation purposes only
    </div>
    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# TAB 2 · SHOPPER VIEW
# ═════════════════════════════════════════════════════════════════════════════
with tab_shop:

    # ── Derived values ────────────────────────────────────────────────────────
    first_name = row["name"].split()[0]
    tier       = row["loyalty_tier"]
    tc_s       = TIER_COL.get(tier, "#777")
    pts        = row["points_balance"]
    total_pts_s = pts + row["points_to_next_reward"]
    prog_s     = int(pts / total_pts_s * 100)
    streak     = row["streak_weeks"]
    badges_s   = [str(row.get(b, "")) for b in ["badge_health", "badge_eco", "badge_loyalty"]]
    badges_s   = [b for b in badges_s if b not in ("", "nan")]
    products   = PRODUCT_RECS.get(row["persona"], PRODUCT_RECS["Health Pioneer"])
    validity   = VALIDITY_MAP.get(row["recommended_timing"], "Valid this week")
    ch_icon_s  = CH_ICON.get(row["recommended_channel"], "📣")

    meta_s  = PERSONA_META.get(row["persona"], {})
    p_icon_s = meta_s.get("icon", "👤")
    p_bg_s, p_col_s = {
        "Health Pioneer":   ("#E8F5E9", C_GREEN),
        "Eco Explorer":     ("#E0F2F1", "#00695C"),
        "Family Organiser": ("#E3F2FD", "#1565C0"),
        "Smart Saver":      ("#FFF8E1", "#E65100"),
        "Routine Loyalist": ("#F3E5F5", "#6A1B9A"),
        "Weekend Foodie":   ("#FFF3E0", "#BF360C"),
        "Budget-Conscious": ("#FFF8E1", "#BF360C"),
        "Eco-Progressive":  ("#E8F5E9", C_GREEN),
    }.get(row["persona"], (C_LTBL, C_BLUE))

    # ── Build HTML fragments ──────────────────────────────────────────────────
    prod_cards_html = ""
    for p in products:
        prod_cards_html += f"""
        <div style="background:#fff;border-radius:14px;padding:16px 12px 14px;
                    box-shadow:0 2px 10px rgba(0,0,0,.07);text-align:center;
                    border-bottom:3px solid {C_GREEN}">
          <div style="font-size:40px;margin-bottom:8px;line-height:1">{p['icon']}</div>
          <div style="font-size:12px;font-weight:700;color:#222;margin-bottom:2px">{p['name']}</div>
          <div style="font-size:10px;color:#aaa;margin-bottom:8px">{p['brand']}</div>
          <span style="background:{C_LTBL};color:{C_BLUE};font-size:10px;font-weight:600;
                       padding:3px 9px;border-radius:20px;display:inline-block">{p['tag']}</span>
          <div style="margin-top:9px;font-size:12px;font-weight:800;color:{C_AMBER}">
            +{p['pts']} pts
          </div>
        </div>"""

    badge_chips_html = ""
    for b in badges_s:
        icon = BADGE_ICON.get(b, "🏅")
        badge_chips_html += f"""
        <div style="display:flex;align-items:center;gap:10px;background:#fff;
                    border-radius:10px;padding:11px 14px;
                    box-shadow:0 2px 6px rgba(0,0,0,.06)">
          <span style="font-size:22px">{icon}</span>
          <div>
            <div style="font-size:13px;font-weight:700;color:#222">{b}</div>
            <div style="font-size:10px;color:#aaa">Earned badge</div>
          </div>
        </div>"""
    if not badge_chips_html:
        badge_chips_html = (
            '<div style="font-size:13px;color:#aaa;padding:8px 0">'
            'Complete missions to earn your first badge</div>'
        )

    # ── Centered mobile-style layout ──────────────────────────────────────────
    _, col_center, _ = st.columns([1, 1.5, 1])

    with col_center:

        # 1 · App greeting header
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{C_BLUE} 0%,#0066CC 100%);
                    border-radius:16px;padding:26px 24px 22px;margin-bottom:14px;
                    box-shadow:0 4px 18px rgba(0,74,151,.25)">
          <div style="font-size:10px;color:#A8C8F0;letter-spacing:2px;
                      text-transform:uppercase;margin-bottom:6px">GreenBasket Rewards</div>
          <div style="font-size:24px;font-weight:900;color:#fff;margin-bottom:12px">
            Hello, {first_name}! 👋
          </div>
          <div style="display:flex;gap:8px;flex-wrap:wrap">
            <div style="background:{tc_s};color:#fff;padding:5px 14px;border-radius:20px;
                        font-size:12px;font-weight:700">⭐ {tier} Member</div>
            <div style="background:rgba(255,255,255,.15);color:#fff;padding:5px 14px;
                        border-radius:20px;font-size:12px">
              {p_icon_s} {row['persona']}
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # 2 · Points + streak + progress
        st.markdown(f"""
        <div style="background:#fff;border-radius:16px;padding:22px 22px 18px;
                    margin-bottom:14px;box-shadow:0 2px 12px rgba(0,0,0,.07)">
          <div style="display:flex;justify-content:space-between;
                      align-items:flex-start;margin-bottom:16px">
            <div>
              <div style="font-size:10px;color:#aaa;text-transform:uppercase;
                          letter-spacing:1.2px;margin-bottom:4px">Your Points</div>
              <div style="font-size:40px;font-weight:900;color:{C_BLUE};line-height:1">
                {pts:,}
              </div>
              <div style="font-size:11px;color:#aaa;margin-top:5px">
                {row['points_to_next_reward']:,} pts to next reward
              </div>
            </div>
            <div style="text-align:right">
              <div style="font-size:10px;color:#aaa;text-transform:uppercase;
                          letter-spacing:1.2px;margin-bottom:4px">Streak</div>
              <div style="font-size:32px;font-weight:900;color:{C_AMBER}">🔥 {streak}w</div>
            </div>
          </div>
          <div style="background:#EAECEF;border-radius:8px;height:10px;
                      overflow:hidden;margin-bottom:6px">
            <div style="width:{prog_s}%;height:10px;border-radius:8px;
                        background:linear-gradient(90deg,{C_BLUE},{C_BLUE}bb)"></div>
          </div>
          <div style="display:flex;justify-content:space-between;font-size:11px;color:#aaa">
            <span>Progress to next reward</span>
            <span style="font-weight:700;color:{C_BLUE}">{prog_s}%</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # 3 · Active mission
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{C_LTBL} 0%,#DEEEFF 100%);
                    border:1.5px solid #B3D1F0;border-radius:16px;padding:20px 22px;
                    margin-bottom:14px">
          <div style="display:flex;justify-content:space-between;
                      align-items:center;margin-bottom:12px">
            <div style="font-size:11px;font-weight:700;color:{C_BLUE};
                        text-transform:uppercase;letter-spacing:1px">🎯 Your Active Mission</div>
            <span style="background:{C_GREEN};color:#fff;font-size:10px;font-weight:700;
                         padding:3px 11px;border-radius:20px">{row['recommended_offer_type']}</span>
          </div>
          <div style="font-size:15px;font-weight:700;color:#1a1a2e;
                      line-height:1.6;margin-bottom:16px">
            {row['recommended_offer_text']}
          </div>
          <div style="display:flex;gap:10px">
            <div style="flex:1;background:rgba(255,255,255,.85);border-radius:10px;
                        padding:11px 13px">
              <div style="font-size:10px;color:#aaa;text-transform:uppercase;
                          letter-spacing:1px;margin-bottom:4px">Channel</div>
              <div style="font-size:13px;font-weight:700;color:#333">
                {ch_icon_s} {row['recommended_channel']}
              </div>
            </div>
            <div style="flex:1;background:rgba(255,255,255,.85);border-radius:10px;
                        padding:11px 13px">
              <div style="font-size:10px;color:#aaa;text-transform:uppercase;
                          letter-spacing:1px;margin-bottom:4px">Valid</div>
              <div style="font-size:13px;font-weight:700;color:{C_RED}">
                ⏰ {validity}
              </div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # 4 · Recommended products
        st.markdown(
            f'<div style="font-size:11px;font-weight:700;color:{C_BLUE};'
            f'text-transform:uppercase;letter-spacing:1.5px;margin:4px 0 12px;'
            f'padding-bottom:7px;border-bottom:2px solid {C_LTBL}">'
            f'Recommended For You</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;'
            f'margin-bottom:20px">{prod_cards_html}</div>',
            unsafe_allow_html=True,
        )

        # 5 · Badges
        st.markdown(
            f'<div style="font-size:11px;font-weight:700;color:{C_BLUE};'
            f'text-transform:uppercase;letter-spacing:1.5px;margin:4px 0 12px;'
            f'padding-bottom:7px;border-bottom:2px solid {C_LTBL}">'
            f'Your Badges</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div style="display:flex;flex-direction:column;gap:9px;margin-bottom:22px">'
            f'{badge_chips_html}</div>',
            unsafe_allow_html=True,
        )

        # 6 · CTA
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{C_RED} 0%,#E53935 100%);
                    border-radius:14px;padding:20px;text-align:center;
                    box-shadow:0 4px 16px rgba(204,0,0,.28);margin-bottom:10px">
          <div style="font-size:17px;font-weight:900;color:#fff;letter-spacing:.4px">
            Activate Offer
          </div>
          <div style="font-size:11px;color:rgba(255,255,255,.75);margin-top:5px">
            Tap to unlock your personalised deal
          </div>
        </div>
        <div style="text-align:center;font-size:10px;color:#ccc;padding:10px 0 4px">
          GreenBasket · Powered by Catalina
        </div>
        """, unsafe_allow_html=True)
