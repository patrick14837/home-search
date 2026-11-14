import html
import random
import re

import streamlit as st

try:
    from supabase import create_client
except ImportError:
    create_client = None

st.set_page_config(page_title="Home Search Kenya", layout="wide", page_icon="🏠")

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------
SUPPORT_PHONE = "0140311646"
LISTING_FEE_KSH = 1300  # roughly US$10; change to your real fee
PAGES = ("home", "landlords", "about", "signin")
PAGE_SIZE = 12

ALL_TOWNS = "All towns & cities"
ALL_AREAS = "All areas"
ANY_TYPE = "Any home"

# Starter location data. "factor" scales demo rents; "areas" feed the second
# dropdown. Edit these lists to match the places you really cover.
REGIONS = {
    "Nairobi": {
        "factor": 2.0,
        "areas": ["Kilimani", "Westlands", "Lavington", "Karen", "Langata", "South B",
                  "Kasarani", "Roysambu", "Embakasi", "Donholm", "Umoja"],
    },
    "Mombasa": {
        "factor": 1.7,
        "areas": ["Nyali", "Bamburi", "Tudor", "Likoni", "Kisauni", "Changamwe", "Old Town"],
    },
    "Kisumu": {
        "factor": 1.2,
        "areas": ["Milimani", "Mamboleo", "Kondele", "Nyalenda", "Dunga", "Kibos"],
    },
    "Nakuru": {
        "factor": 1.2,
        "areas": ["Milimani", "Section 58", "Lanet", "Naka", "Pipeline", "London"],
    },
    "Eldoret": {
        "factor": 1.15,
        "areas": ["Elgon View", "Pioneer", "Kapsoya", "Langas", "Huruma", "Kimumu"],
    },
    "Thika": {
        "factor": 1.1,
        "areas": ["Section 9", "Makongeni", "Ngoingwa"],
    },
    "Kiambu": {
        "factor": 1.35,
        "areas": ["Ruaka", "Ruiru", "Juja", "Kikuyu", "Kiambu Town"],
    },
    "Machakos & Kajiado": {
        "factor": 1.3,
        "areas": ["Syokimau", "Mlolongo", "Athi River", "Kitengela", "Ongata Rongai",
                  "Machakos Town"],
    },
    "Kakamega": {
        "factor": 1.0,
        "areas": ["Milimani", "Lurambi", "Amalemba", "Shieywe"],
    },
    "Kisii": {
        "factor": 0.95,
        "areas": ["Daraja Mbili", "Nyanchwa", "Jogoo"],
    },
    "Maseno": {
        "factor": 0.85,
        "areas": ["Maseno Town", "Mabungo", "Near Maseno University"],
    },
    "Siaya": {
        "factor": 0.9,
        "areas": ["Siaya Town Centre", "Siaya Outskirts"],
    },
    "Busia": {
        "factor": 0.9,
        "areas": ["Busia Town", "Busia Border Area"],
    },
    "Bondo": {
        "factor": 0.8,
        "areas": ["Bondo Town", "Usenge"],
    },
    "Ugunja": {
        "factor": 0.7,
        "areas": ["Ugunja Town", "Ugunja Outskirts"],
    },
    "Ukwala": {
        "factor": 0.65,
        "areas": ["Ukwala Town", "Ukwala Outskirts"],
    },
}
TOWNS = list(REGIONS)
PREMIUM_AREAS = {"Kilimani", "Westlands", "Lavington", "Karen", "Nyali", "Milimani"}

TYPE_BASE = {
    "Single room": 2500,
    "Bedsitter": 4500,
    "1 Bedroom": 7000,
    "2 Bedroom": 12000,
    "3 Bedroom": 18000,
}
PROPERTY_TYPES = list(TYPE_BASE)

BUDGET_STEPS = [0, 3000, 4000, 5000, 7500, 10000, 15000, 20000, 30000, 50000, 80000, 150000]
SORTS = ["Lowest rent first", "Highest rent first", "Town A-Z"]
IMAGES = [
    "https://images.unsplash.com/photo-1605146769289-440113cc3d00?w=800",
    "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800",
    "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800",
]


@st.cache_data
def get_listings():
    """Clearly labelled demonstration listings. Not real, not verified rentals."""
    rng = random.Random(2026)  # fixed seed: same demo data on every run
    items = []
    for town, info in REGIONS.items():
        for area in info["areas"]:
            for ptype in rng.sample(PROPERTY_TYPES, k=3):
                rent = TYPE_BASE[ptype] * info["factor"]
                if area in PREMIUM_AREAS:
                    rent *= 1.35
                rent *= rng.uniform(0.9, 1.15)
                items.append({
                    "town": town,
                    "area": area,
                    "type": ptype,
                    "rent": int(round(rent / 500) * 500),
                    "name": f"{ptype} - {area}, {town}",
                    "image": IMAGES[len(items) % len(IMAGES)],
                })
    return items


def fmt_budget(value):
    if value == BUDGET_STEPS[-1]:
        return f"{value // 1000}k+"
    return f"KSh {value:,}"


# --------------------------------------------------------------------------
# Session state and routing
# --------------------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "verified" not in st.session_state:
    st.session_state.verified = False
if "stk" not in st.session_state:
    st.session_state.stk = False
if "shown" not in st.session_state:
    st.session_state.shown = PAGE_SIZE

# Only accept known pages from the URL; anything else falls back to home.
requested_page = st.query_params.get("page")
if requested_page in PAGES:
    st.session_state.page = requested_page


def go(p):
    st.session_state.page = p
    st.query_params["page"] = p
    st.rerun()


def is_signed_in():
    return bool(st.session_state.get("auth_user_id"))


def get_supabase_client():
    """Return a per-visitor Supabase client (never shared between visitors).

    The Supabase client keeps the signed-in session inside itself, so a client
    cached globally with st.cache_resource would leak one user's session to
    everyone else. Keep it in st.session_state instead.
    """
    if create_client is None:
        return None, "The Supabase package is not installed. Add supabase to requirements.txt."
    client = st.session_state.get("_supabase")
    if client is not None:
        return client, None
    try:
        client = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_ANON_KEY"])
    except Exception:
        return None, (
            "Authentication is not configured yet. Add SUPABASE_URL and "
            "SUPABASE_ANON_KEY to Streamlit secrets."
        )
    st.session_state["_supabase"] = client
    return client, None


def sign_out():
    client = st.session_state.get("_supabase")
    if client is not None:
        try:
            client.auth.sign_out()
        except Exception:
            pass
    for key in ("auth_user_email", "auth_user_id", "signed_in_account_type", "_supabase"):
        st.session_state.pop(key, None)
    go("home")


def reset_filters():
    st.session_state.f_town = ALL_TOWNS
    st.session_state.f_area = ALL_AREAS
    st.session_state.f_text = ""
    st.session_state.f_type = ANY_TYPE
    st.session_state.f_budget = (BUDGET_STEPS[0], BUDGET_STEPS[-1])
    st.session_state.f_sort = SORTS[0]


def show_more():
    st.session_state.shown += PAGE_SIZE


# --------------------------------------------------------------------------
# Styles
# --------------------------------------------------------------------------
st.markdown("""
<style>
[data-testid="stHeader"] {display:none !important;}
footer {display:none !important;}
.block-container {
    padding-top: 0 !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
    max-width: 100% !important;
}
.stApp {background:#FFFFFF;}

/* ---------- BUTTONS: always readable, light or dark browser theme ---------- */
.stApp button[kind="primary"],
.stApp [data-testid="stBaseButton-primary"],
.stApp [data-testid="stBaseButton-primaryFormSubmit"] {
    background:#0F3D2E !important;
    color:#FFFFFF !important;
    border:2px solid #0F3D2E !important;
    border-radius:10px !important;
    font-weight:700 !important;
    min-height:44px;
}
.stApp button[kind="secondary"],
.stApp [data-testid="stBaseButton-secondary"],
.stApp [data-testid="stBaseButton-secondaryFormSubmit"] {
    background:#FFFFFF !important;
    color:#0F3D2E !important;
    border:2px solid #0F3D2E !important;
    border-radius:10px !important;
    font-weight:700 !important;
    min-height:44px;
}
.stApp button p, .stApp button span {color:inherit !important; font-weight:700 !important;}
.stApp button[kind="primary"]:hover,
.stApp [data-testid="stBaseButton-primary"]:hover {background:#1B5E47 !important; border-color:#1B5E47 !important;}
.stApp button[kind="secondary"]:hover,
.stApp [data-testid="stBaseButton-secondary"]:hover {background:#E3F0E9 !important;}
.stApp button:focus-visible {outline:3px solid #F7E38E !important; outline-offset:2px !important; box-shadow:0 0 0 5px #0F3D2E !important;}
.stApp button:disabled {opacity:0.55 !important;}

/* ---------- GREEN TOP NAVIGATION BAR ---------- */
.st-key-top_nav {
    background:#0F3D2E !important;
    padding:14px 20px !important;
    border-bottom:1px solid #0A2D22 !important;
    box-shadow:0 2px 8px rgba(0,0,0,0.12);
}
.st-key-top_nav [data-testid="stHorizontalBlock"],
.st-key-top_nav [data-testid="stColumn"] {background:transparent !important;}
.st-key-top_nav [data-testid="stMarkdownContainer"] {color:white !important;}
/* inactive tab: white pill, dark green text */
.st-key-top_nav button[kind="secondary"],
.st-key-top_nav [data-testid="stBaseButton-secondary"] {
    background:#FFFFFF !important;
    color:#0F3D2E !important;
    border:2px solid #FFFFFF !important;
    border-radius:999px !important;
}
/* active tab: yellow pill, dark green text */
.st-key-top_nav button[kind="primary"],
.st-key-top_nav [data-testid="stBaseButton-primary"] {
    background:#F7E38E !important;
    color:#0F3D2E !important;
    border:2px solid #F7E38E !important;
    border-radius:999px !important;
}
.st-key-top_nav button:focus-visible {outline:3px solid #FFFFFF !important; box-shadow:none !important;}

/* ---------- HERO ---------- */
.hero {
    height:380px;
    background:linear-gradient(to right, rgba(0,0,0,0.68), rgba(0,0,0,0.25)),
    url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1600&q=80');
    background-size:cover;
    background-position:center;
    padding:50px 32px 90px 32px;
    display:flex;
    flex-direction:column;
    justify-content:center;
}
.hero h1 {color:white; font-size:52px; font-weight:800; line-height:1.05; margin:0;}

/* ---------- SEARCH PANEL ---------- */
.st-key-search_box {
    background:#FFFFFF;
    border-radius:20px;
    padding:22px 22px 14px 22px;
    margin:-70px 32px 20px 32px;
    width:calc(100% - 64px) !important;
    box-sizing:border-box;
    box-shadow:0 12px 40px rgba(0,0,0,0.16);
    border:1px solid #D5E3DB;
    position:relative;
    z-index:10;
}
.st-key-search_box label p {color:#0F3D2E !important; font-weight:700 !important; font-size:14px !important;}
.st-key-search_box [data-baseweb="select"] > div,
.st-key-search_box [data-baseweb="input"] {
    border:1.5px solid #8FAE9F !important;
    border-radius:10px !important;
}
.st-key-search_box [data-baseweb="select"] div,
.st-key-search_box [data-baseweb="input"],
.st-key-search_box [data-baseweb="input"] > div,
.st-key-search_box input {
    background:#FFFFFF !important;
    color:#10241C !important;
    -webkit-text-fill-color:#10241C !important;
}
.st-key-search_box input::placeholder {color:#6B7A75 !important; -webkit-text-fill-color:#6B7A75 !important; opacity:1;}
.st-key-search_box [data-baseweb="select"] svg {fill:#0F3D2E !important;}
/* dropdown lists open in a popover outside the panel */
[data-baseweb="popover"] [role="listbox"],
[data-baseweb="popover"] [role="option"],
[data-baseweb="popover"] li {background:#FFFFFF !important; color:#10241C !important;}
[data-baseweb="popover"] [role="option"]:hover {background:#E3F0E9 !important;}

/* ---------- CARDS ---------- */
.st-key-landlord_card {
    background:#FFFFFF;
    border-radius:16px;
    padding:24px;
    box-shadow:0 8px 30px rgba(0,0,0,0.08);
    border:1px solid #EFE9E0;
    margin:24px 32px;
}
.form-card {
    background:white;
    border-radius:16px;
    padding:24px;
    box-shadow:0 8px 30px rgba(0,0,0,0.08);
    border:1px solid #EFE9E0;
    margin:24px 32px;
}
.safety-card {
    background:white;
    border-radius:12px;
    padding:20px;
    border-left:4px solid #0F3D2E;
    box-shadow:0 4px 16px rgba(0,0,0,0.06);
    margin-bottom:16px;
}
.trust-badge {
    background:#F7E38E;
    color:#0F3D2E;
    padding:6px 12px;
    border-radius:20px;
    font-size:12px;
    font-weight:800;
    display:inline-block;
    margin:4px 4px 4px 0;
}
.st-key-results_grid {padding:0 32px;}
.home-title {color:#10241C !important; font-size:17px; font-weight:800; margin:10px 0 2px 0; line-height:1.3;}
.home-rent {color:#0F3D2E !important; font-size:16px; font-weight:700; margin:0 0 6px 0;}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------------------------------
# Navigation bar
# --------------------------------------------------------------------------
with st.container(key="top_nav"):
    col_logo, c1, c2, c3, c4 = st.columns([2.8, 1.1, 1, 1.3, 0.9], vertical_alignment="center")
    with col_logo:
        st.markdown(
            '<div style="color:white; font-weight:900; font-size:20px;">'
            'Home Search <span style="color:#F7E38E;">Kenya</span></div>',
            unsafe_allow_html=True
        )
    with c1:
        if st.button("Find a Home", type="primary" if st.session_state.page == "home" else "secondary",
                     use_container_width=True, key="bh"):
            go("home")
    with c2:
        if st.button("Landlords", type="primary" if st.session_state.page == "landlords" else "secondary",
                     use_container_width=True, key="bl"):
            go("landlords")
    with c3:
        if st.button("About & Safety", type="primary" if st.session_state.page == "about" else "secondary",
                     use_container_width=True, key="ba"):
            go("about")
    with c4:
        if is_signed_in():
            if st.button("Sign out", type="secondary", use_container_width=True, key="bso"):
                sign_out()
        else:
            if st.button("Sign in", type="primary" if st.session_state.page == "signin" else "secondary",
                         use_container_width=True, key="bs"):
                go("signin")


# --------------------------------------------------------------------------
# HOME
# --------------------------------------------------------------------------
if st.session_state.page == "home":
    st.markdown(
        '<div class="hero"><h1>Find a place to<br>call home.</h1>'
        '<p style="color:#E8EDEB; font-size:15px; max-width:460px; margin-top:14px;">'
        f'Search rentals in Nairobi, Mombasa, Kisumu, Nakuru, Eldoret and {len(REGIONS) - 5} more towns. '
        f'Customer Service: {SUPPORT_PHONE}</p></div>',
        unsafe_allow_html=True
    )

    with st.container(key="search_box"):
        r1a, r1b, r1c = st.columns([1.4, 1.4, 2.2], vertical_alignment="bottom")
        with r1a:
            town = st.selectbox("Town or city", [ALL_TOWNS] + TOWNS, key="f_town")
        with r1b:
            area_options = [ALL_AREAS] + (REGIONS[town]["areas"] if town in REGIONS else [])
            if st.session_state.get("f_area") not in area_options:
                st.session_state["f_area"] = ALL_AREAS
            area = st.selectbox(
                "Area or estate", area_options, key="f_area",
                disabled=town == ALL_TOWNS,
                help="Pick a town or city first to narrow down to an estate."
            )
        with r1c:
            text = st.text_input(
                "Landmark, estate or street",
                placeholder="e.g. Milimani, near the university, Mabungo",
                key="f_text"
            )

        r2a, r2b, r2c, r2d, r2e = st.columns([1.2, 2.3, 1.3, 1.1, 1.0], vertical_alignment="bottom")
        with r2a:
            ptype = st.selectbox("Property type", [ANY_TYPE] + PROPERTY_TYPES, key="f_type")
        with r2b:
            budget = st.select_slider(
                "Monthly rent (KSh)", options=BUDGET_STEPS,
                value=(BUDGET_STEPS[0], BUDGET_STEPS[-1]),
                format_func=fmt_budget, key="f_budget"
            )
        with r2c:
            sort_by = st.selectbox("Sort by", SORTS, key="f_sort")
        with r2d:
            search_clicked = st.button("Search homes", type="primary", use_container_width=True, key="search_btn")
        with r2e:
            st.button("Clear", type="secondary", use_container_width=True, key="clear_btn", on_click=reset_filters)

    # ---- filtering ----
    if not isinstance(budget, (tuple, list)):
        budget = (BUDGET_STEPS[0], budget)
    low, high = budget
    tokens = text.lower().split()
    filtered = []
    for house in get_listings():
        if town != ALL_TOWNS and house["town"] != town:
            continue
        if area != ALL_AREAS and house["area"] != area:
            continue
        if ptype != ANY_TYPE and house["type"] != ptype:
            continue
        if house["rent"] < low:
            continue
        if high != BUDGET_STEPS[-1] and house["rent"] > high:
            continue
        haystack = f'{house["name"]} {house["area"]} {house["town"]}'.lower()
        if tokens and not all(token in haystack for token in tokens):
            continue
        filtered.append(house)

    if sort_by == "Lowest rent first":
        filtered.sort(key=lambda h: h["rent"])
    elif sort_by == "Highest rent first":
        filtered.sort(key=lambda h: -h["rent"])
    else:
        filtered.sort(key=lambda h: (h["town"], h["area"], h["rent"]))

    # Start from the first page of results whenever the filters change.
    signature = (town, area, text, ptype, budget, sort_by)
    if st.session_state.get("_sig") != signature:
        st.session_state["_sig"] = signature
        st.session_state.shown = PAGE_SIZE

    if search_clicked:
        st.toast(f"{len(filtered)} demonstration home(s) match your search.")

    place = town if town == ALL_TOWNS else (town if area == ALL_AREAS else f"{area}, {town}")
    st.markdown(
        f'<div style="padding:8px 32px 0 32px;">'
        f'<h2 style="color:#0F3D2E; margin-bottom:4px;">Homes you might love</h2>'
        f'<p style="color:#51635D; font-size:14px; margin-top:0;">'
        f'{len(filtered)} demonstration listing(s) in {html.escape(place)}, '
        f'KSh {low:,} to {html.escape(fmt_budget(high))}. '
        f'Listings are examples, not confirmed available rentals.</p></div>',
        unsafe_allow_html=True
    )

    if filtered:
        visible = filtered[:st.session_state.shown]
        grid = st.container(key="results_grid")
        cols = grid.columns(3)
        for index, house in enumerate(visible):
            with cols[index % 3]:
                st.image(house["image"], use_container_width=True)
                st.markdown(
                    f"<div class='home-title'>{html.escape(house['name'])}</div>"
                    f"<div class='home-rent'>KSh {house['rent']:,} / month</div>"
                    f"<span class='trust-badge'>Demo listing</span>"
                    f"<span class='trust-badge'>{html.escape(house['area'])}</span>",
                    unsafe_allow_html=True
                )
        remaining = len(filtered) - len(visible)
        if remaining > 0:
            _, mid, _ = st.columns([1, 1, 1])
            with mid:
                st.button(f"Show more homes ({remaining} left)", type="primary",
                          use_container_width=True, key="more_btn", on_click=show_more)
    else:
        st.info(
            "No demonstration listings match those filters. Try All areas, a wider rent "
            "range, or a different property type."
        )
        st.button("Clear all filters", type="primary", key="clear_empty", on_click=reset_filters)


# --------------------------------------------------------------------------
# LANDLORDS
# --------------------------------------------------------------------------
elif st.session_state.page == "landlords":
    st.markdown(
        '<div style="padding:24px 32px 0 32px;">'
        '<h1 style="color:#0F3D2E; font-weight:900;">List your house - Get tenants fast</h1>'
        f'<p style="color:#51635D;">{len(REGIONS)} towns covered. Demo verification code 123456 - '
        f'Support: {SUPPORT_PHONE}</p></div>',
        unsafe_allow_html=True
    )
    with st.container(key="landlord_card"):
        if not is_signed_in():
            st.info("Sign in to save your listing. You can still try the demo steps below.")
        full_name = st.text_input("Full Name *")
        phone = st.text_input("Phone / WhatsApp *", placeholder="07XXXXXXXX")
        lc1, lc2 = st.columns(2)
        with lc1:
            town_ll = st.selectbox("Town or city *", TOWNS, key="ll_town")
        with lc2:
            if st.session_state.get("ll_area") not in REGIONS[town_ll]["areas"]:
                st.session_state["ll_area"] = REGIONS[town_ll]["areas"][0]
            area_ll = st.selectbox("Area or estate *", REGIONS[town_ll]["areas"], key="ll_area")
        type_ll = st.selectbox("Property type *", PROPERTY_TYPES, key="ll_type")
        rent = st.number_input("Monthly Rent (KSh) *", min_value=0, value=6500, step=500)
        desc = st.text_area("House Description *")
        st.caption("Demo only: this form does not collect a real payment or publish a live listing.")

        if st.button(f"Demo M-Pesa STK Push - KSh {LISTING_FEE_KSH:,}", type="primary", key="stk_btn"):
            st.session_state.stk = True
            st.info("Demo flow only. No real STK push has been sent.")
        if st.session_state.stk:
            code = st.text_input("Enter demo verification code", key="code")
            if st.button("Verify Code", type="secondary", key="ver"):
                if code == "123456":
                    st.session_state.verified = True
                    st.success("Demo verification complete.")
                else:
                    st.error("Incorrect demo code. Use 123456.")
        if st.session_state.verified:
            if st.button("Submit demo listing", type="primary", use_container_width=True, key="submit_demo"):
                phone_ok = re.fullmatch(r"(?:\+254|254|0)[17]\d{8}", phone.replace(" ", ""))
                if not full_name.strip() or not desc.strip():
                    st.error("Enter your full name and a house description.")
                elif not phone_ok:
                    st.error("Enter a valid Kenyan phone number, e.g. 0712345678.")
                elif rent <= 0:
                    st.error("Enter the monthly rent.")
                else:
                    st.success(
                        f"Demo listing entered for {full_name.strip()}: {type_ll} in {area_ll}, "
                        f"{town_ll} at KSh {int(rent):,}. It has not been published to a live database."
                    )
        else:
            st.warning("Complete the demo verification steps to test this flow.")


# --------------------------------------------------------------------------
# ABOUT
# --------------------------------------------------------------------------
elif st.session_state.page == "about":
    towns_text = ", ".join(TOWNS[:-1]) + " and " + TOWNS[-1]
    st.markdown(
        '<div style="padding:24px 32px 0 32px;">'
        '<h1 style="color:#0F3D2E; font-weight:900; font-size:38px;">About Home Search Kenya</h1>'
        '<p style="color:#51635D;">Rental search demonstration for Kenya. '
        f'Customer Service: <b>{SUPPORT_PHONE}</b></p></div>',
        unsafe_allow_html=True
    )
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"""
        <div class="form-card" style="margin:16px 0 16px 32px;">
          <h3 style="color:#0F3D2E; margin-top:0;">Who We Are</h3>
          <p style="color:#3F504A; line-height:1.8;">
          Home Search Kenya is a rental-platform prototype for exploring properties in
          {html.escape(towns_text)}.
          <br><br>
          <b>Important:</b> The properties currently shown are sample listings for demonstration.
          They have not been confirmed as available, and this prototype does not verify landlord IDs.
          </p>
          <h3 style="color:#0F3D2E;">How It Works</h3>
          <p style="color:#3F504A; line-height:1.8;">
          <b>Tenants:</b> Filter the sample listings by town, area, property type and rent.
          Always physically view a property and independently confirm the landlord before paying.
          <br><br>
          <b>Landlords:</b> The current form is a demo and does not publish a real listing or process payment.
          </p>
        </div>
        <div style="padding:0 0 0 32px;">
          <h2 style="color:#0F3D2E;">Safety Center</h2>
          <div class="safety-card">
            <h4 style="margin:0 0 8px 0; color:#0F3D2E;">For Tenants - Safety Tips</h4>
            <ol style="color:#3F504A; line-height:1.9; margin:0;">
              <li>Never pay before viewing the property.</li>
              <li>Meet at the property and check water, electricity and locks.</li>
              <li>Ask for identification and evidence that the person can rent the property.</li>
              <li>Get a written agreement and receipt for any payment.</li>
              <li>Be cautious of unusually low prices or pressure to pay immediately.</li>
            </ol>
          </div>
          <div class="safety-card" style="border-left-color:#C0392B;">
            <h4 style="margin:0 0 8px 0; color:#C0392B;">Red Flags</h4>
            <ul style="color:#3F504A; line-height:1.8; margin:0;">
              <li>Requests a deposit before a viewing.</li>
              <li>Refuses to meet in person.</li>
              <li>Pressures you to pay immediately.</li>
              <li>Cannot provide evidence of identity or authority to rent the property.</li>
            </ul>
          </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="form-card" style="margin:16px 32px 16px 0;">
          <h3 style="color:#0F3D2E; margin-top:0;">Customer Service</h3>
          <p style="color:#3F504A; line-height:2;">
          <b>Phone / WhatsApp:</b><br>{SUPPORT_PHONE}<br><br>
          <b>Support hours:</b><br>To be confirmed<br><br>
          <b>Email:</b><br>To be confirmed<br><br>
          <b>Office address:</b><br>To be confirmed
          </p>
          <hr>
          <h4 style="color:#0F3D2E;">Trust and Safety</h4>
          <p style="color:#3F504A; font-size:13px; line-height:1.7;">
          Listings on this prototype are examples only.<br>
          Landlord identity verification is not yet connected.<br>
          Real M-Pesa payments are not enabled.<br>
          Always view a house before paying.
          </p>
        </div>
        """, unsafe_allow_html=True)


# --------------------------------------------------------------------------
# SIGN IN
# --------------------------------------------------------------------------
elif st.session_state.page == "signin":
    st.markdown("""
    <style>
    .login-page {
        padding: 38px 18px 48px 18px;
        background: linear-gradient(135deg, #F5F8F5 0%, #FFFFFF 55%, #EAF2ED 100%);
        border-radius: 0 0 24px 24px;
    }
    .login-heading {text-align:center; color:#0F3D2E; font-size:34px; font-weight:850; margin:0 0 8px 0;}
    .login-subheading {text-align:center; color:#51635D; font-size:15px; margin:0 0 24px 0;}
    .login-brand {text-align:center; font-size:13px; font-weight:800; letter-spacing:2px; color:#0F3D2E; margin-bottom:12px;}
    div[data-testid="stForm"] {
        background:#FFFFFF;
        border:1px solid #E1EAE4;
        border-radius:20px;
        padding:26px;
        box-shadow:0 16px 44px rgba(15, 61, 46, 0.10);
    }
    </style>
    <div class="login-page">
      <div class="login-brand">HOME SEARCH KENYA</div>
      <h1 class="login-heading">Your home journey starts here</h1>
      <p class="login-subheading">Sign in or create an account to continue.</p>
    </div>
    """, unsafe_allow_html=True)

    left_space, login_col, right_space = st.columns([1, 1.15, 1])
    with login_col:
        if is_signed_in():
            st.success(
                f"You are signed in as {st.session_state.get('auth_user_email', 'your account')} "
                f"({st.session_state.get('signed_in_account_type', 'tenant')})."
            )
            st.info("Your account is authenticated. A user dashboard can be added next.")
        else:
            st.markdown(
                '<h3 style="text-align:center; color:#0F3D2E; margin:0 0 6px 0;">Your account</h3>'
                '<p style="text-align:center; color:#51635D; font-size:13px; margin:0 0 18px 0;">'
                'For tenants and landlords</p>',
                unsafe_allow_html=True
            )
            auth_mode = st.radio(
                "Choose an option",
                ["Sign in", "Create account", "Forgot password"],
                horizontal=True,
                key="auth_mode"
            )
            supabase, auth_setup_error = get_supabase_client()

            if auth_mode == "Sign in":
                with st.form("signin_form", clear_on_submit=False):
                    email = st.text_input("Email address", placeholder="you@example.com")
                    password = st.text_input("Password", type="password")
                    submitted = st.form_submit_button("Sign in", type="primary", use_container_width=True)

                if submitted:
                    if not email.strip() or not password:
                        st.error("Enter both your email address and password.")
                    elif supabase is None:
                        st.error(auth_setup_error)
                    else:
                        try:
                            result = supabase.auth.sign_in_with_password({
                                "email": email.strip(),
                                "password": password
                            })
                            user = result.user
                            if user:
                                st.session_state["auth_user_email"] = user.email
                                st.session_state["auth_user_id"] = user.id
                                # Display only. user_metadata can be edited by the user, so use a
                                # profiles table with Row Level Security for real access control.
                                st.session_state["signed_in_account_type"] = (
                                    (user.user_metadata or {}).get("account_type", "tenant")
                                )
                                st.rerun()
                            else:
                                st.error("Sign-in was not completed. Check your details and try again.")
                        except Exception:
                            st.error("Sign-in failed. Check your email and password, and verify your email if required.")

            elif auth_mode == "Create account":
                account_type = st.radio("I am a", ["Tenant", "Landlord"], horizontal=True, key="auth_account_type")
                with st.form("signup_form", clear_on_submit=False):
                    email = st.text_input("Email address", placeholder="you@example.com")
                    password = st.text_input(
                        "Create password",
                        type="password",
                        help="Use at least 8 characters and avoid reusing a password from another site."
                    )
                    confirm_password = st.text_input("Confirm password", type="password")
                    accepted = st.checkbox(
                        "I understand this is a rental platform and I will provide accurate information."
                    )
                    submitted = st.form_submit_button("Create account", type="primary", use_container_width=True)

                if submitted:
                    if not email.strip() or not password or not confirm_password:
                        st.error("Complete all fields.")
                    elif "@" not in email or "." not in email.rsplit("@", 1)[-1]:
                        st.error("Enter a valid email address.")
                    elif len(password) < 8:
                        st.error("Choose a password with at least 8 characters.")
                    elif password != confirm_password:
                        st.error("The passwords do not match.")
                    elif not accepted:
                        st.error("Please confirm the statement before creating an account.")
                    elif supabase is None:
                        st.error(auth_setup_error)
                    else:
                        try:
                            result = supabase.auth.sign_up({
                                "email": email.strip(),
                                "password": password,
                                "options": {"data": {"account_type": account_type.lower()}}
                            })
                            if result.user:
                                st.success(
                                    "Registration request submitted. If email confirmation is enabled "
                                    "in Supabase, check your inbox to verify your email before signing in."
                                )
                            else:
                                st.error("The account could not be created. Please try again.")
                        except Exception:
                            st.error(
                                "Account creation failed. The email may already be registered, "
                                "or the authentication service may need configuration."
                            )

            else:
                with st.form("reset_password_form", clear_on_submit=True):
                    reset_email = st.text_input("Account email address", placeholder="you@example.com")
                    reset_submitted = st.form_submit_button(
                        "Send password reset email", type="primary", use_container_width=True
                    )
                if reset_submitted:
                    if not reset_email.strip() or "@" not in reset_email:
                        st.error("Enter the email address associated with your account.")
                    elif supabase is None:
                        st.error(auth_setup_error)
                    else:
                        try:
                            options = {}
                            try:
                                site_url = st.secrets["SITE_URL"]
                            except Exception:
                                site_url = None
                            if site_url:
                                options["redirect_to"] = site_url
                            supabase.auth.reset_password_for_email(reset_email.strip(), options)
                            st.success(
                                "If an account exists for that address, a password-reset email will be sent. "
                                "Check your inbox and spam folder."
                            )
                        except Exception:
                            st.error("The reset request could not be sent. Please try again later.")

            st.markdown(
                '<p style="text-align:center; color:#51635D; font-size:12px; margin-top:18px;">'
                'Never share your password or email verification codes.</p>',
                unsafe_allow_html=True
            )


st.markdown(
    '<div style="text-align:center; padding:20px; color:#6B7A75; font-size:12px; '
    'background:white; margin-top:20px; border-top:1px solid #EDE9E0;">'
    '2026 Home Search Kenya - Sample listings for demonstration - '
    'Always view a house before paying</div>',
    unsafe_allow_html=True
)
