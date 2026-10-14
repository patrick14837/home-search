import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.parse import quote
import re

st.set_page_config(
    page_title="Home Search Kenya",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Demo data
# IMPORTANT: These are examples, not verified rental listings.
# Replace them with verified properties before launching publicly.
# -----------------------------
DEMO_HOUSES = [
    {"id": 1, "town": "Siaya", "type": "Single Room", "rent": 3500, "deposit": 3500,
     "lat": -0.0626, "lon": 34.2878, "phone": "0712345678",
     "photo": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=1200&q=80",
     "landlord": "Demo landlord", "verified": False, "available": True},
    {"id": 2, "town": "Bondo", "type": "Bedsitter", "rent": 5500, "deposit": 5500,
     "lat": -0.0893, "lon": 34.2762, "phone": "0722112233",
     "photo": "https://images.unsplash.com/photo-1502672023488-70e25813eb80?auto=format&fit=crop&w=1200&q=80",
     "landlord": "Demo landlord", "verified": False, "available": True},
    {"id": 3, "town": "Kisumu", "type": "1BR", "rent": 12000, "deposit": 12000,
     "lat": -0.0917, "lon": 34.7680, "phone": "0700123456",
     "photo": "https://images.unsplash.com/photo-1493809842364-3750e0684b6e?auto=format&fit=crop&w=1200&q=80",
     "landlord": "Demo landlord", "verified": False, "available": True},
    {"id": 4, "town": "Ugunja", "type": "2BR", "rent": 8000, "deposit": 8000,
     "lat": 0.0860, "lon": 34.3100, "phone": "0711223344",
     "photo": "https://images.unsplash.com/photo-1560448204-603b3fc33ddc?auto=format&fit=crop&w=1200&q=80",
     "landlord": "Demo landlord", "verified": False, "available": True},
    {"id": 5, "town": "Siaya", "type": "Bedsitter", "rent": 6000, "deposit": 6000,
     "lat": -0.0590, "lon": 34.2900, "phone": "0722334455",
     "photo": "https://images.unsplash.com/photo-1502005229762-cf1b2da7c5d6?auto=format&fit=crop&w=1200&q=80",
     "landlord": "Demo landlord", "verified": False, "available": True},
]

if "houses" not in st.session_state:
    st.session_state.houses = pd.DataFrame(DEMO_HOUSES)
if "demo_listing_unlocked" not in st.session_state:
    st.session_state.demo_listing_unlocked = False
if "saved_house_ids" not in st.session_state:
    st.session_state.saved_house_ids = set()

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp { background: #f6f8fb; }
    h1, h2, h3 { font-family: 'Manrope', sans-serif; color: #14243a; }
    .hero {
        padding: 1.5rem 1.7rem; border-radius: 22px;
        background: linear-gradient(120deg, #102a43 0%, #176b5b 100%);
        color: white; margin-bottom: 1.2rem;
    }
    .hero h1 { color: white; margin: 0; font-size: clamp(1.8rem, 4vw, 2.8rem); }
    .hero p { color: #e4f4ef; margin: .45rem 0 0 0; font-size: 1.02rem; }
    .eyebrow { text-transform: uppercase; letter-spacing: .12em; font-size: .75rem; font-weight: 700; color: #bde9d9; }
    .listing-card {
        background: #ffffff; border: 1px solid #e6ebf1; border-radius: 18px;
        padding: 0 0 1rem 0; margin-bottom: 1rem; overflow: hidden;
        box-shadow: 0 5px 20px rgba(16,42,67,.055);
    }
    .listing-card img { width: 100%; height: 205px; object-fit: cover; display: block; }
    .listing-body { padding: 1rem 1rem .2rem 1rem; }
    .listing-title { font-family: 'Manrope', sans-serif; font-weight: 800; color: #14243a; font-size: 1.12rem; }
    .listing-meta { color: #66758a; font-size: .9rem; margin-top: .25rem; }
    .price { font-size: 1.35rem; font-weight: 800; color: #087f5b; margin-top: .7rem; }
    .cost { color: #536276; font-size: .88rem; margin-top: .2rem; }
    .pill { display: inline-block; border-radius: 100px; padding: .25rem .6rem; background: #fff4d6; color: #7b5700; font-size: .75rem; font-weight: 700; }
    .small-note { color: #64748b; font-size: .85rem; }
    [data-testid="stMetric"] { background: white; padding: 1rem; border: 1px solid #e6ebf1; border-radius: 14px; }
    div.stButton > button, div.stLinkButton > a { border-radius: 10px; font-weight: 700; }
    @media (max-width: 700px) {
      .hero { padding: 1.2rem; }
      .listing-card img { height: 180px; }
    }
</style>
""", unsafe_allow_html=True)

df = st.session_state.houses.copy()
for col, default in {
    "verified": False, "available": True, "deposit": 0, "landlord": "Not supplied",
    "phone": "", "photo": "", "lat": None, "lon": None
}.items():
    if col not in df.columns:
        df[col] = default

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.markdown("## 🏠 Home Search")
st.sidebar.caption("KENYA · RENTAL DISCOVERY")
st.sidebar.markdown("---")
towns = sorted(df["town"].dropna().unique().tolist())
types = sorted(df["type"].dropna().unique().tolist())
selected_towns = st.sidebar.multiselect("Town or area", towns, default=towns)
selected_types = st.sidebar.multiselect("Property type", types, default=types)
max_rent = int(max(20000, df["rent"].max() if not df.empty else 20000))
rent_limit = st.sidebar.slider("Maximum monthly rent (KSh)", 2000, max_rent, min(15000, max_rent), step=500)
show_available = st.sidebar.checkbox("Available properties only", value=True)
st.sidebar.markdown("---")
st.sidebar.caption("Demo listings are illustrative and have not been verified. Confirm a property in person before paying.")

filtered = df[
    df["town"].isin(selected_towns)
    & df["type"].isin(selected_types)
    & (pd.to_numeric(df["rent"], errors="coerce") <= rent_limit)
]
if show_available and "available" in filtered.columns:
    filtered = filtered[filtered["available"].fillna(False)]

# -----------------------------
# Header
# -----------------------------
st.markdown("""
<div class="hero">
  <div class="eyebrow">Find a place to call home</div>
  <h1>Home Search Kenya 🏡</h1>
  <p>Explore rental options around Siaya, Kisumu and neighbouring towns.</p>
</div>
""", unsafe_allow_html=True)
st.warning("Prototype mode: the properties and contact details shown may be demo data. No payment is processed by this app.")

tab_find, tab_dashboard, tab_landlord = st.tabs(
    ["🔎 Find a home", "📊 Rental insights", "🏘️ List a property"]
)

# -----------------------------
# Find a home
# -----------------------------
with tab_find:
    metric_cols = st.columns(3)
    metric_cols[0].metric("Matching homes", len(filtered))
    metric_cols[1].metric("Lowest rent", f"KSh {int(filtered['rent'].min()):,}" if not filtered.empty else "—")
    metric_cols[2].metric("Towns covered", filtered["town"].nunique() if not filtered.empty else 0)

    st.subheader("Explore on the map")
    map_df = filtered.dropna(subset=["lat", "lon"]).copy()
    if not map_df.empty:
        map_df["lat"] = pd.to_numeric(map_df["lat"], errors="coerce")
        map_df["lon"] = pd.to_numeric(map_df["lon"], errors="coerce")
        map_df = map_df.dropna(subset=["lat", "lon"])
        if not map_df.empty:
            st.map(map_df, latitude="lat", longitude="lon", size=35)
    else:
        st.info("No map coordinates are available for the current filters.")

    st.subheader("Homes matching your search")
    if filtered.empty:
        st.info("No homes match these filters. Try increasing your rent limit or selecting more towns.")
    else:
        cols = st.columns(3)
        for position, (_, row) in enumerate(filtered.iterrows()):
            with cols[position % 3]:
                photo = str(row.get("photo", "") or "").strip()
                if photo:
                    st.image(photo, use_container_width=True)
                else:
                    st.image("https://placehold.co/800x500?text=Photo+coming+soon", use_container_width=True)

                st.markdown(f"### {row['type']} · {row['town']}")
                st.markdown(f"<div class='price'>KSh {int(row['rent']):,}<span style='font-size:.8rem;font-weight:500;color:#64748b'> / month</span></div>", unsafe_allow_html=True)
                deposit = int(row.get("deposit", 0) or 0)
                st.markdown(f"<div class='cost'>Deposit: KSh {deposit:,}<br><b>Estimated move-in total: KSh {int(row['rent']) + deposit:,}</b></div>", unsafe_allow_html=True)
                if bool(row.get("verified", False)):
                    st.success("Verified listing")
                else:
                    st.markdown("<span class='pill'>Demo / not verified</span>", unsafe_allow_html=True)

                phone = re.sub(r"\D", "", str(row.get("phone", "")))
                if phone.startswith("0") and len(phone) == 10:
                    phone = "254" + phone[1:]
                elif phone.startswith("+"):
                    phone = phone[1:]
                if phone and len(phone) >= 10:
                    message = quote(f"Hello, I'm enquiring about the {row['type']} in {row['town']} listed at KSh {int(row['rent']):,} per month. Is it available, and can I arrange a viewing?")
                    st.link_button("WhatsApp about this home", f"https://wa.me/{phone}?text={message}", use_container_width=True)
                else:
                    st.button("Contact not available", key=f"contact_{row['id']}", disabled=True, use_container_width=True)

                saved = int(row["id"]) in st.session_state.saved_house_ids
                if st.button("♥ Saved" if saved else "♡ Save home", key=f"save_{row['id']}", use_container_width=True):
                    if saved:
                        st.session_state.saved_house_ids.discard(int(row["id"]))
                    else:
                        st.session_state.saved_house_ids.add(int(row["id"]))
                    st.rerun()
                st.caption(f"Listing ID: {row['id']} · Contact details must be verified independently.")

# -----------------------------
# Rental dashboard
# -----------------------------
with tab_dashboard:
    st.subheader("Rental market snapshot")
    st.caption("Insights are calculated from the current dataset, including demo listings.")
    if df.empty:
        st.info("Add listings to see market insights.")
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("Listings in dataset", len(df))
        c2.metric("Average monthly rent", f"KSh {df['rent'].mean():,.0f}")
        c3.metric("Median monthly rent", f"KSh {df['rent'].median():,.0f}")

        town_avg = df.groupby("town", as_index=False)["rent"].mean().sort_values("rent")
        fig1 = px.bar(
            town_avg, x="town", y="rent", color="rent",
            title="Average monthly rent by town",
            labels={"town": "Town", "rent": "Average rent (KSh)"},
            color_continuous_scale=["#bde9d9", "#087f5b"],
        )
        fig1.update_layout(showlegend=False, plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig1, use_container_width=True)

        left, right = st.columns(2)
        type_counts = df["type"].value_counts().rename_axis("type").reset_index(name="count")
        fig2 = px.pie(type_counts, names="type", values="count", title="Property types in dataset", hole=0.45)
        fig2.update_layout(paper_bgcolor="white")
        left.plotly_chart(fig2, use_container_width=True)

        fig3 = px.histogram(
            df, x="rent", nbins=10, title="Monthly rent distribution",
            labels={"rent": "Monthly rent (KSh)"},
            color_discrete_sequence=["#087f5b"],
        )
        fig3.update_layout(plot_bgcolor="white", paper_bgcolor="white")
        right.plotly_chart(fig3, use_container_width=True)

        st.markdown("#### Listings by town")
        st.dataframe(
            df.groupby("town", as_index=False).agg(
                Listings=("id", "count"),
                **{"Average rent (KSh)": ("rent", "mean"), "Lowest rent (KSh)": ("rent", "min")}
            ).round(0),
            use_container_width=True,
            hide_index=True,
        )

# -----------------------------
# Landlord portal (demo only)
# -----------------------------
with tab_landlord:
    st.subheader("List your rental property")
    st.info("This is a prototype form. It does not collect a real listing fee, verify ownership, or permanently save uploaded photos/listings.")
    st.markdown("**No payment is required in this demo.** Do not send money based on this screen.")
    if not st.session_state.demo_listing_unlocked:
        if st.button("Open demo listing form", type="primary"):
            st.session_state.demo_listing_unlocked = True
            st.rerun()
    else:
        with st.form("landlord_form", clear_on_submit=False):
            col_a, col_b = st.columns(2)
            with col_a:
                town = st.selectbox("Town", ["Siaya", "Bondo", "Ugunja", "Kisumu", "Usenge", "Busia", "Other"])
                h_type = st.selectbox("Property type", ["Single Room", "Bedsitter", "1BR", "2BR", "3BR", "Other"])
                rent = st.number_input("Monthly rent (KSh)", min_value=1000, max_value=200000, value=5000, step=500)
                deposit = st.number_input("Deposit (KSh)", min_value=0, max_value=200000, value=5000, step=500)
            with col_b:
                landlord_name = st.text_input("Your name or business name")
                phone = st.text_input("Contact phone number", placeholder="07XXXXXXXX")
                lat = st.number_input("GPS latitude (optional)", value=-0.062600, format="%.6f")
                lon = st.number_input("GPS longitude (optional)", value=34.287800, format="%.6f")
            uploaded_photos = st.file_uploader(
                "Upload property photos (demo; not permanently stored)",
                type=["jpg", "jpeg", "png", "webp"],
                accept_multiple_files=True,
            )
            submitted = st.form_submit_button("Preview and add demo listing", type="primary")

            if submitted:
                digits = re.sub(r"\D", "", phone)
                if not landlord_name.strip():
                    st.error("Enter a name or business name.")
                elif not (len(digits) == 10 and digits.startswith("0")):
                    st.error("Enter a Kenyan phone number in the format 07XXXXXXXX or 01XXXXXXXX.")
                elif rent <= 0:
                    st.error("Monthly rent must be greater than zero.")
                else:
                    new_id = int(pd.to_numeric(st.session_state.houses["id"], errors="coerce").max()) + 1 if not st.session_state.houses.empty else 1
                    photo_url = ""
                    if uploaded_photos:
                        # Session-only preview; uploaded file is not persisted to durable storage.
                        st.session_state[f"uploaded_photo_{new_id}"] = uploaded_photos[0].getvalue()
                        photo_url = ""
                    new_row = {
                        "id": new_id, "town": town, "type": h_type, "rent": int(rent),
                        "deposit": int(deposit), "lat": float(lat), "lon": float(lon),
                        "phone": phone.strip(), "photo": photo_url,
                        "landlord": landlord_name.strip(), "verified": False, "available": True,
                    }
                    st.session_state.houses = pd.concat(
                        [st.session_state.houses, pd.DataFrame([new_row])],
                        ignore_index=True,
                    )
                    st.success("Demo listing added to this session. It is not verified and may disappear when the session resets.")
                    if uploaded_photos:
                        st.image(uploaded_photos[0], caption="Photo preview (session only)", use_container_width=True)
                    st.caption("Before public launch, connect persistent storage, secure image storage, caretaker authentication and a real verification process.")
                    st.rerun()

st.markdown("---")
st.caption("Home Search Kenya · Prototype build · Confirm property details in person and never pay a deposit before verifying the property and recipient.")
