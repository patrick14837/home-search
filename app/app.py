import os
import time
import requests
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Home Search Kenya",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- Configuration --------------------
API_BASE = st.secrets.get(
    "PAYMENT_API_BASE",
    os.getenv("PAYMENT_API_BASE", "http://localhost:8000"),
).rstrip("/")
REGISTRATION_FEE_KES = int(st.secrets.get("REGISTRATION_FEE_KES", 1300))
API_TIMEOUT = 20

# Illustrative demo data only. Replace with reviewed listings from a database.
SAMPLE_PROPERTIES = [
    {
        "town": "Siaya", "type": "Bedsitter", "rent": 4500, "deposit": 4500,
        "title": "Sample bedsitter — Siaya",
        "description": "Illustrative listing. This is not a verified or bookable property.",
        "area": "Siaya town (approximate)", "bedrooms": "Bedsitter",
        "image": "https://images.unsplash.com/photo-1598928506311-c55ded91a20c?auto=format&fit=crop&w=1200&q=85",
    },
    {
        "town": "Kisumu", "type": "One-bedroom", "rent": 9000, "deposit": 9000,
        "title": "Sample one-bedroom — Kisumu",
        "description": "Illustrative listing. This is not a verified or bookable property.",
        "area": "Kisumu (approximate)", "bedrooms": "1 bedroom",
        "image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=85",
    },
    {
        "town": "Busia", "type": "Bedsitter", "rent": 4000, "deposit": 4000,
        "title": "Sample bedsitter — Busia",
        "description": "Illustrative listing. This is not a verified or bookable property.",
        "area": "Busia town (approximate)", "bedrooms": "Bedsitter",
        "image": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1200&q=85",
    },
]

# Approximate town-centre coordinates for a demonstration map, not property addresses.
TOWN_COORDS = {
    "Siaya": (-0.0617, 34.2881),
    "Kisumu": (-0.0917, 34.7680),
    "Busia": (0.4608, 34.1115),
}

# -------------------- Styling --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
:root { --forest:#0d3b2e; --green:#0b5945; --gold:#f2c96d; --ink:#173c35; }
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #f7f8f5; }
.block-container { max-width: 1440px; padding-top: 1rem; padding-bottom: 3rem; }
[data-testid="stSidebar"] { background: #f0f4ef; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #244a3e; }
.hero {
  min-height: 360px; padding: 2.5rem 2.8rem; border-radius: 24px;
  display:flex; flex-direction:column; justify-content:center;
  color:#fff; overflow:hidden; position:relative;
  background: linear-gradient(90deg, rgba(7,37,29,.88) 0%, rgba(7,37,29,.58) 48%, rgba(7,37,29,.08) 100%),
  url('https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=2000&q=90') center 48%/cover;
  box-shadow: 0 14px 35px rgba(13,59,46,.14);
}
.brand { color:#fff; font-size:1.05rem; font-weight:800; letter-spacing:.2px; margin-bottom:1.4rem; }
.brand span { color:var(--gold); }
.hero h1 { color:#fff; font-size:clamp(2.2rem,4.5vw,4rem); line-height:1.05; max-width:650px; margin:0 0 1rem 0; font-weight:800; }
.hero p { color:#f3f6f3; font-size:1.12rem; max-width:620px; }
.house-bob { display:inline-block; transform-origin:center bottom; animation:houseBob 1.35s ease-in-out infinite; }
@keyframes houseBob { 0%,100% { transform:translateY(0) rotate(0); } 50% { transform:translateY(-5px) rotate(-3deg); } }
.section-title { color:var(--ink); font-size:1.8rem; font-weight:800; margin:.6rem 0 .1rem 0; }
.subtle { color:#69756f; }
.property-card { background:#fff; border:1px solid #e5e9e4; border-radius:18px; overflow:hidden; box-shadow:0 5px 18px rgba(20,50,38,.06); margin-bottom:1rem; }
.property-card img { width:100%; height:180px; object-fit:cover; display:block; }
.property-body { padding:1rem 1.1rem 1.2rem 1.1rem; }
.price { font-size:1.35rem; color:#0c4a3b; font-weight:800; }
.tag { display:inline-block; background:#fff3d4; color:#73510a; border-radius:99px; padding:.22rem .65rem; font-size:.75rem; font-weight:700; }
div.stButton > button[kind="primary"] { background:#0b5945; border:0; border-radius:10px; color:white; font-weight:700; }
div.stButton > button[kind="primary"]:hover { background:#083e31; color:white; }
div[data-testid="stForm"] { background:white; border:1px solid #e5e9e4; padding:1.2rem; border-radius:16px; }
[data-testid="stMetric"] { background:white; border:1px solid #e5e9e4; border-radius:14px; padding:1rem; }
@media (max-width: 700px) { .hero { padding:1.5rem; min-height:300px; } .hero h1 { font-size:2.2rem; } }
</style>
""", unsafe_allow_html=True)


def api_get(path, params=None):
    return requests.get(f"{API_BASE}{path}", params=params, timeout=API_TIMEOUT)


def api_post(path, payload):
    return requests.post(f"{API_BASE}{path}", json=payload, timeout=API_TIMEOUT)


def normalize_phone(phone):
    return phone.strip().replace(" ", "").replace("-", "")


# -------------------- Header --------------------
st.markdown("""
<div class="hero">
  <div class="brand"><span class="house-bob">🏠</span> Home Search <span>Kenya</span></div>
  <h1>Find a place to call home.</h1>
  <p>Explore rental options across Siaya, Kisumu, Busia and nearby towns.</p>
</div>
""", unsafe_allow_html=True)
st.caption("Early-access project. Listings shown below are examples only and are not verified properties.")

page = st.sidebar.radio(
    "Explore Home Search Kenya",
    ["Find a Home", "Landlord / Caretaker Registration", "About & Safety"],
)
st.sidebar.markdown("---")
st.sidebar.markdown("**Home Search Kenya**")
st.sidebar.caption("Helping tenants discover homes and connect with property owners.")


# -------------------- Find a Home --------------------
if page == "Find a Home":
    st.markdown('<div class="section-title">Homes to explore</div>', unsafe_allow_html=True)
    st.markdown('<p class="subtle">Filter by location, property type and monthly budget.</p>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.15, 1.15, 1.3])
    with c1:
        town = st.selectbox("Town or area", ["All towns", "Siaya", "Kisumu", "Busia"])
    with c2:
        ptype = st.selectbox("Property type", ["All types", "Bedsitter", "One-bedroom", "Two-bedroom", "House"])
    with c3:
        max_rent = st.number_input("Maximum monthly rent (KSh)", min_value=0, value=15000, step=500)

    data = [
        p for p in SAMPLE_PROPERTIES
        if (town == "All towns" or p["town"] == town)
        and (ptype == "All types" or p["type"] == ptype)
        and p["rent"] <= max_rent
    ]

    left, right = st.columns([2.2, 1])
    with left:
        if not data:
            st.info("No sample listings match these filters. Try increasing your budget or changing the filters.")
        else:
            cards = st.columns(min(3, len(data)))
            for i, p in enumerate(data):
                with cards[i % len(cards)]:
                    st.markdown(
                        f"""
                        <div class="property-card">
                          <img src="{p['image']}" alt="Illustrative property photo">
                          <div class="property-body">
                            <span class="tag">SAMPLE LISTING</span>
                            <h3 style="color:#173c35;margin:.7rem 0 .25rem 0;font-size:1.15rem">{p['title']}</h3>
                            <div class="subtle">{p['town']} · {p['bedrooms']}</div>
                            <div class="price" style="margin-top:.65rem">KSh {p['rent']:,}<span style="font-size:.8rem;font-weight:500"> / month</span></div>
                            <div class="subtle" style="margin-top:.4rem">Deposit example: KSh {p['deposit']:,}</div>
                            <p style="color:#69756f;font-size:.9rem;margin-top:.6rem">{p['description']}</p>
                          </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    with st.expander("Listing details"):
                        st.write(f"**Area:** {p['area']}")
                        st.write(f"**Estimated move-in total:** KSh {p['rent'] + p['deposit']:,}")
                        st.caption("Sample only: this property is not verified, available for viewing, or bookable.")

    with right:
        st.markdown("#### 📍 Explore by location")
        st.write("Allow location access to view your approximate position on the map.")
        try:
            from streamlit_geolocation import streamlit_geolocation
            location_result = streamlit_geolocation()
        except ImportError:
            location_result = None
            st.warning("Location support isn't installed yet. Install the packages in requirements.txt and redeploy.")
        except Exception:
            location_result = None

        if isinstance(location_result, dict) and location_result.get("latitude") is not None and location_result.get("longitude") is not None:
            lat = float(location_result["latitude"])
            lon = float(location_result["longitude"])
            st.success("Location received from your browser.")
            st.caption("Your browser may ask for permission. Coordinates are shown only in this session.")
            map_rows = [{"latitude": lat, "longitude": lon, "label": "Your approximate location"}]
            for town_name, (town_lat, town_lon) in TOWN_COORDS.items():
                map_rows.append({"latitude": town_lat, "longitude": town_lon, "label": f"{town_name} town centre (approx.)"})
            st.map(pd.DataFrame(map_rows), latitude="latitude", longitude="longitude", size=100)
            st.link_button("Open your location in Google Maps", f"https://www.google.com/maps?q={lat},{lon}")
        else:
            st.info("Location is optional. You can still search homes by town.")
            map_rows = [
                {"latitude": coords[0], "longitude": coords[1]}
                for coords in TOWN_COORDS.values()
            ]
            st.map(pd.DataFrame(map_rows), latitude="latitude", longitude="longitude")
            st.caption("Pins indicate approximate town centres, not exact property locations.")

    st.info("The current version uses sample listings. Before launch, connect a database and add property photos and listings that have been reviewed.")


# -------------------- Landlord registration and payments --------------------
elif page == "Landlord / Caretaker Registration":
    st.markdown('<div class="section-title">List your property</div>', unsafe_allow_html=True)
    st.write(f"Registration fee: **KSh {REGISTRATION_FEE_KES:,}**")
    st.caption(
        "This fee is currently configured as an approximate KSh equivalent of US$10. "
        "Confirm the exact fee and publish clear service/refund terms before launch. "
        "This form does not itself charge a payment; the payment API must be configured."
    )

    with st.form("start_payment"):
        full_name = st.text_input("Full name")
        phone = st.text_input("M-Pesa phone number", placeholder="e.g. 0712345678 or 254712345678")
        email = st.text_input("Email (optional)")
        role = st.selectbox("I am a", ["Landlord", "Caretaker / agent"])
        accepted = st.checkbox("I understand the registration fee and have read the fee/refund terms.")
        submitted = st.form_submit_button("Request M-Pesa payment", type="primary")

    if submitted:
        normalized_phone = normalize_phone(phone)
        if not full_name.strip():
            st.error("Enter your full name.")
        elif not normalized_phone:
            st.error("Enter the M-Pesa phone number for the payment request.")
        elif not accepted:
            st.error("Please confirm the fee/refund terms.")
        else:
            try:
                resp = api_post("/payments/stk-push", {
                    "full_name": full_name.strip(),
                    "phone": normalized_phone,
                    "email": email.strip(),
                    "role": role,
                    "amount": REGISTRATION_FEE_KES,
                })
                if resp.ok:
                    result = resp.json()
                    payment_id = result.get("payment_id")
                    if not payment_id:
                        st.error("The payment service did not return a payment reference. Please contact support.")
                    else:
                        st.session_state["pending_payment"] = {
                            "payment_id": payment_id,
                            "full_name": full_name.strip(),
                            "email": email.strip(),
                            "role": role,
                        }
                        st.success("Payment request sent. Check your phone and enter your PIN only in the official M-Pesa prompt.")
                        st.info(f"Reference: {payment_id}. Keep this reference for support.")
                else:
                    try:
                        detail = resp.json().get("detail", resp.text)
                    except Exception:
                        detail = resp.text
                    st.error(f"Could not start payment: {detail}")
            except requests.RequestException:
                st.error("The payment service is not reachable. No payment has been confirmed by this website.")
                st.caption("For local testing, start payment_api.py in a second terminal. Live payments require approved Daraja production credentials and a public HTTPS callback.")

    pending = st.session_state.get("pending_payment")
    if pending:
        st.divider()
        st.markdown("#### Check payment status")
        st.write(f"Payment reference: `{pending['payment_id']}`")
        col_status, col_auto = st.columns(2)
        with col_status:
            if st.button("Refresh payment status"):
                try:
                    r = api_get(f"/payments/{pending['payment_id']}")
                    if r.ok:
                        status = r.json().get("status", "pending")
                        if status == "paid":
                            st.session_state["payment_verified"] = pending
                            st.success("Payment verified by the payment service.")
                        elif status in ("failed", "cancelled", "expired"):
                            st.error(f"Payment status: {status}. You can start a new payment request.")
                        else:
                            st.warning("Payment is still pending. Wait a little and refresh.")
                    else:
                        st.error("Could not check payment status.")
                except requests.RequestException:
                    st.error("Payment service unavailable.")
        with col_auto:
            if st.button("Auto-check for 20 seconds"):
                status_box = st.empty()
                for _ in range(10):
                    try:
                        r = api_get(f"/payments/{pending['payment_id']}")
                        if r.ok:
                            status = r.json().get("status", "pending")
                            status_box.info(f"Payment status: {status}")
                            if status == "paid":
                                st.session_state["payment_verified"] = pending
                                status_box.success("Payment verified. Registration is unlocked.")
                                break
                            if status in ("failed", "cancelled", "expired"):
                                break
                    except requests.RequestException:
                        status_box.error("Payment service unavailable.")
                        break
                    time.sleep(2)
                st.rerun()

    verified = st.session_state.get("payment_verified")
    if verified:
        st.divider()
        st.success("Payment confirmed by the payment service. Complete the initial property submission below.")
        with st.form("property_submission"):
            property_title = st.text_input("Property title")
            town2 = st.selectbox("Property town", ["Siaya", "Kisumu", "Busia", "Other"])
            property_type = st.selectbox("Property type", ["Bedsitter", "One-bedroom", "Two-bedroom", "House", "Shop / commercial"])
            rent = st.number_input("Monthly rent (KSh)", min_value=0, step=500)
            deposit = st.number_input("Deposit (KSh)", min_value=0, step=500)
            contact = st.text_input("Public contact phone number")
            area = st.text_input("Estate / area (avoid entering a private home address)")
            description = st.text_area("Property description")
            submit_property = st.form_submit_button("Submit property for review", type="primary")
        if submit_property:
            st.info("Payment is confirmed, but persistent property storage is not enabled in this starter version. The submission below is only a preview.")
            st.json({
                "registrant": verified["full_name"],
                "role": verified["role"],
                "property_title": property_title,
                "town": town2,
                "property_type": property_type,
                "rent_kes": rent,
                "deposit_kes": deposit,
                "contact": contact,
                "area": area,
                "description": description,
                "review_status": "pending",
            })


# -------------------- About and safety --------------------
elif page == "About & Safety":
    st.markdown('<div class="section-title">About Home Search Kenya</div>', unsafe_allow_html=True)
    st.write(
        "Home Search Kenya aims to help tenants discover rental properties and connect "
        "with landlords and caretakers in Siaya, Kisumu, Busia and nearby areas."
    )
    st.markdown("#### Our priorities before public launch")
    st.markdown("""
    - Replace sample listings with properties whose owners or agents have been checked.
    - Publish clear registration, service and refund terms.
    - Set up a secure database and protected photo storage.
    - Use a secure verification process for identity checks; do not collect identity documents in this prototype.
    - Configure HTTPS, secrets, access controls, backups and an administrator review workflow.
    - Test successful, cancelled, failed, duplicate and delayed M-Pesa callbacks.
    - Ask permission before accessing browser location and explain how location data is used.
    """)
    st.warning(
        "This is an early-stage prototype, not production-ready. Do not collect real fees "
        "until approved Safaricom production credentials, callback verification, persistent "
        "records, security controls and business terms are in place."
    )

st.markdown("---")
st.caption("© Home Search Kenya · Early access · Please verify all property details before making payments or commitments.")
