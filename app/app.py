import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.parse import quote
import re
import io

st.set_page_config(
    page_title="Home Search Kenya",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# DEMO ONLY: replace these sample records with verified listings before public launch.
DEMO_HOUSES = [
    {"id": 1, "town": "Siaya", "type": "Single Room", "rent": 3500, "deposit": 3500,
     "lat": -0.0626, "lon": 34.2878, "phone": "0712345678",
     "photo": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=1200&q=80",
     "landlord": "Demo landlord", "verified": False, "available": True, "description": "Sample listing only."},
    {"id": 2, "town": "Bondo", "type": "Bedsitter", "rent": 5500, "deposit": 5500,
     "lat": -0.0893, "lon": 34.2762, "phone": "0722112233",
     "photo": "https://images.unsplash.com/photo-1502672023488-70e25813eb80?auto=format&fit=crop&w=1200&q=80",
     "landlord": "Demo landlord", "verified": False, "available": True, "description": "Sample listing only."},
    {"id": 3, "town": "Kisumu", "type": "1BR", "rent": 12000, "deposit": 12000,
     "lat": -0.0917, "lon": 34.7680, "phone": "0700123456",
     "photo": "https://images.unsplash.com/photo-1493809842364-3750e0684b6e?auto=format&fit=crop&w=1200&q=80",
     "landlord": "Demo landlord", "verified": False, "available": True, "description": "Sample listing only."},
    {"id": 4, "town": "Ugunja", "type": "2BR", "rent": 8000, "deposit": 8000,
     "lat": 0.0860, "lon": 34.3100, "phone": "0711223344",
     "photo": "https://images.unsplash.com/photo-1560448204-603b3fc33ddc?auto=format&fit=crop&w=1200&q=80",
     "landlord": "Demo landlord", "verified": False, "available": True, "description": "Sample listing only."},
    {"id": 5, "town": "Siaya", "type": "Bedsitter", "rent": 6000, "deposit": 6000,
     "lat": -0.0590, "lon": 34.2900, "phone": "0722334455",
     "photo": "https://images.unsplash.com/photo-1502005229762-cf1b2da7c5d6?auto=format&fit=crop&w=1200&q=80",
     "landlord": "Demo landlord", "verified": False, "available": True, "description": "Sample listing only."},
]

if "houses" not in st.session_state:
    st.session_state.houses = pd.DataFrame(DEMO_HOUSES)
if "saved_house_ids" not in st.session_state:
    st.session_state.saved_house_ids = set()
if "submitted_credentials" not in st.session_state:
    st.session_state.submitted_credentials = []
if "uploaded_property_photos" not in st.session_state:
    st.session_state.uploaded_property_photos = {}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
html, body, [class*="css"] {font-family:'DM Sans',sans-serif;}
.stApp {background:#f6f8fb;}
h1,h2,h3 {font-family:'Manrope',sans-serif;color:#14243a;}
.hero {padding:1.5rem 1.7rem;border-radius:22px;background:linear-gradient(120deg,#102a43,#176b5b);color:white;margin-bottom:1.2rem;}
.hero h1 {color:white;margin:0;font-size:clamp(1.8rem,4vw,2.8rem);}
.hero p {color:#e4f4ef;margin:.45rem 0 0;font-size:1.02rem;}
.eyebrow {text-transform:uppercase;letter-spacing:.12em;font-size:.75rem;font-weight:700;color:#bde9d9;}
.price {font-size:1.35rem;font-weight:800;color:#087f5b;margin-top:.7rem;}
.pill {display:inline-block;border-radius:100px;padding:.25rem .6rem;background:#fff4d6;color:#7b5700;font-size:.75rem;font-weight:700;}
[data-testid="stMetric"] {background:white;padding:1rem;border:1px solid #e6ebf1;border-radius:14px;}
div.stButton>button,div.stLinkButton>a {border-radius:10px;font-weight:700;}
</style>
""", unsafe_allow_html=True)

df = st.session_state.houses.copy()
defaults = {"verified": False, "available": True, "deposit": 0, "landlord": "Not supplied",
            "phone": "", "photo": "", "lat": None, "lon": None, "description": ""}
for col, default in defaults.items():
    if col not in df.columns:
        df[col] = default

st.markdown("""
<div class="hero">
  <div class="eyebrow">Find a place to call home</div>
  <h1>Home Search Kenya 🏡</h1>
  <p>Search rentals, compare prices, explore satellite imagery and connect with property managers.</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("## 🏠 Home Search Kenya")
st.sidebar.caption("SIAYA · KISUMU · BUSIA")
page = st.sidebar.radio(
    "Go to",
    ["🔎 Tenant property search", "🧑🏽‍💼 Landlord & caretaker portal", "🛰️ Satellite property map", "📊 Rental insights"],
)
st.sidebar.markdown("---")
st.sidebar.caption("Prototype only. Demo listings and contacts are not verified. Never pay before verifying the property and recipient.")

def show_satellite_map(data):
    """Render Esri World Imagery tiles with Folium; install folium + streamlit-folium."""
    if data.empty or data.dropna(subset=["lat", "lon"]).empty:
        st.info("No mapped properties match the current selection.")
        return
    try:
        import folium
        from streamlit_folium import st_folium
        coords = data.dropna(subset=["lat", "lon"]).copy()
        coords["lat"] = pd.to_numeric(coords["lat"], errors="coerce")
        coords["lon"] = pd.to_numeric(coords["lon"], errors="coerce")
        coords = coords.dropna(subset=["lat", "lon"])
        if coords.empty:
            st.info("No valid GPS coordinates are available.")
            return
        center = [coords["lat"].mean(), coords["lon"].mean()]
        m = folium.Map(location=center, zoom_start=10, tiles=None, control_scale=True)
        folium.TileLayer(
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            attr="Tiles © Esri — Source: Esri, Maxar, Earthstar Geographics, and the GIS User Community",
            name="Satellite imagery",
            overlay=False,
            control=True,
        ).add_to(m)
        folium.TileLayer("OpenStreetMap", name="Street map", control=True).add_to(m)
        for _, r in coords.iterrows():
            popup = (
                f"<b>{r['type']} · {r['town']}</b><br>"
                f"Rent: KSh {int(r['rent']):,}/month<br>"
                f"Deposit: KSh {int(r['deposit']):,}<br>"
                f"Listing ID: {r['id']}<br>"
                "Demo/unverified listing"
            )
            folium.Marker(
                [float(r["lat"]), float(r["lon"])],
                tooltip=f"{r['type']} · {r['town']} · KSh {int(r['rent']):,}",
                popup=folium.Popup(popup, max_width=280),
                icon=folium.Icon(color="green", icon="home", prefix="fa"),
            ).add_to(m)
        folium.LayerControl().add_to(m)
        st_folium(m, use_container_width=True, height=520, returned_objects=[])
        st.caption("Satellite tiles show imagery, not a live video feed. Property pins use the GPS coordinates saved with each listing.")
    except ImportError:
        st.warning("Satellite maps need two extra packages. In your terminal run: pip install folium streamlit-folium")
    except Exception as exc:
        st.error(f"The map could not load. Check your internet connection and map dependencies. Details: {exc}")

def valid_kenyan_phone(raw):
    digits = re.sub(r"\D", "", raw or "")
    return (len(digits) == 10 and digits.startswith(("07", "01"))) or (len(digits) == 12 and digits.startswith("254"))

def whatsapp_link(raw_phone, message):
    digits = re.sub(r"\D", "", raw_phone or "")
    if digits.startswith("0") and len(digits) == 10:
        digits = "254" + digits[1:]
    elif digits.startswith("+"):
        digits = digits[1:]
    if digits.startswith("254") and len(digits) == 12:
        return f"https://wa.me/{digits}?text={quote(message)}"
    return None

# ---------------- Tenant search page ----------------
if page == "🔎 Tenant property search":
    st.subheader("Find a home that fits your budget")
    towns = sorted(df["town"].dropna().unique().tolist())
    types = sorted(df["type"].dropna().unique().tolist())
    f1, f2, f3 = st.columns([1, 1, 1])
    with f1:
        selected_towns = st.multiselect("Choose town(s)", towns, default=towns)
    with f2:
        selected_types = st.multiselect("Property type", types, default=types)
    with f3:
        max_price = max(20000, int(pd.to_numeric(df["rent"], errors="coerce").max() or 20000))
        rent_limit = st.slider("Maximum monthly rent (KSh)", 1000, max_price, min(15000, max_price), step=500)
    only_verified = st.checkbox("Verified listings only", value=False)
    results = df[df["town"].isin(selected_towns) & df["type"].isin(selected_types) & (df["rent"] <= rent_limit)]
    results = results[results["available"].fillna(False)]
    if only_verified:
        results = results[results["verified"].fillna(False)]

    a, b, c = st.columns(3)
    a.metric("Homes found", len(results))
    b.metric("Lowest rent", f"KSh {int(results['rent'].min()):,}" if not results.empty else "—")
    c.metric("Towns represented", results["town"].nunique() if not results.empty else 0)

    with st.expander("🛰️ Show matching homes on satellite map", expanded=False):
        show_satellite_map(results)

    st.markdown("### Available properties")
    if results.empty:
        st.info("No properties match these filters. Try another town or a higher rent limit.")
    else:
        cols = st.columns(3)
        for pos, (_, row) in enumerate(results.iterrows()):
            with cols[pos % 3]:
                if row.get("photo"):
                    st.image(row["photo"], use_container_width=True)
                else:
                    st.info("No property photo supplied.")
                st.markdown(f"### {row['type']} · {row['town']}")
                st.markdown(f"<div class='price'>KSh {int(row['rent']):,}<span style='font-size:.8rem;font-weight:500;color:#64748b'> / month</span></div>", unsafe_allow_html=True)
                deposit = int(row.get("deposit", 0) or 0)
                st.write(f"Deposit: **KSh {deposit:,}**")
                st.write(f"Estimated move-in total: **KSh {int(row['rent']) + deposit:,}**")
                if row.get("description"):
                    st.caption(row["description"])
                if bool(row.get("verified", False)):
                    st.success("Verified listing")
                else:
                    st.markdown("<span class='pill'>Demo / not verified</span>", unsafe_allow_html=True)
                if pd.notna(row.get("lat")) and pd.notna(row.get("lon")):
                    st.caption(f"GPS: {float(row['lat']):.5f}, {float(row['lon']):.5f}")
                msg = f"Hello, I'm enquiring about the {row['type']} in {row['town']} listed at KSh {int(row['rent']):,}/month. Can I arrange a viewing?"
                wa = whatsapp_link(str(row.get("phone", "")), msg)
                if wa:
                    st.link_button("WhatsApp caretaker", wa, use_container_width=True)
                else:
                    st.button("Contact not available", key=f"no_contact_{row['id']}", disabled=True, use_container_width=True)
                is_saved = int(row["id"]) in st.session_state.saved_house_ids
                if st.button("♥ Saved" if is_saved else "♡ Save home", key=f"save_{row['id']}", use_container_width=True):
                    if is_saved:
                        st.session_state.saved_house_ids.discard(int(row["id"]))
                    else:
                        st.session_state.saved_house_ids.add(int(row["id"]))
                    st.rerun()
                st.caption(f"Listing ID: {row['id']}")

# ---------------- Landlord/caretaker portal ----------------
elif page == "🧑🏽‍💼 Landlord & caretaker portal":
    st.subheader("Landlord & caretaker portal")
    st.write("Submit your contact details, verification information and property details for review.")
    st.warning(
        "Security note: this prototype does not securely store credentials or uploaded files. "
        "Do not upload national ID/passport scans, passwords, PINs or other highly sensitive documents here. "
        "For a public launch, identity documents need authenticated access, encrypted storage, limited staff access, "
        "a retention policy and consent."
    )
    with st.form("property_submission", clear_on_submit=False):
        st.markdown("#### 1. Your contact and verification details")
        name = st.text_input("Full name or registered business name")
        role = st.selectbox("I am a", ["Landlord / property owner", "Caretaker / property manager", "Authorized agent"])
        phone = st.text_input("Kenyan phone number", placeholder="07XXXXXXXX")
        email = st.text_input("Email address (optional)")
        credential_type = st.selectbox(
            "Verification method to provide to the review team",
            ["Owner/manager details for manual review", "Business registration details", "Written authorization from owner", "Other"],
        )
        credential_reference = st.text_input(
            "Credential/reference number (optional; do not enter passwords or PINs)",
            help="For this demo, enter only a non-sensitive reference. Do not upload identity documents.",
        )

        st.markdown("#### 2. Property details")
        c1, c2 = st.columns(2)
        with c1:
            town = st.selectbox("Town", ["Siaya", "Bondo", "Ugunja", "Kisumu", "Busia", "Usenge", "Other"])
            house_type = st.selectbox("Property type", ["Single Room", "Bedsitter", "1BR", "2BR", "3BR", "Other"])
            rent = st.number_input("Monthly rent (KSh)", min_value=1000, max_value=200000, value=5000, step=500)
            deposit = st.number_input("Deposit (KSh)", min_value=0, max_value=200000, value=5000, step=500)
        with c2:
            address_hint = st.text_input("Estate, street or nearby landmark")
            lat = st.number_input("GPS latitude", value=-0.062600, format="%.6f", help="Use the property's coordinates, not your current location unless they match.")
            lon = st.number_input("GPS longitude", value=34.287800, format="%.6f")
            description = st.text_area("Property description and amenities", placeholder="Water, electricity, security, parking, distance to town...")
        property_photos = st.file_uploader(
            "Upload property photos (JPG, PNG or WEBP)",
            type=["jpg", "jpeg", "png", "webp"],
            accept_multiple_files=True,
            help="Demo only: uploads remain in temporary app memory and are not safely persisted.",
        )
        credential_photo = st.file_uploader(
            "Optional: non-sensitive supporting image only",
            type=["jpg", "jpeg", "png", "webp"],
            accept_multiple_files=False,
            help="Do not upload national ID/passport scans in this prototype.",
        )
        consent = st.checkbox("I confirm I am authorized to submit this listing and consent to the details being reviewed.")
        submitted = st.form_submit_button("Submit listing for demo review", type="primary")

    if submitted:
        errors = []
        if not name.strip():
            errors.append("Enter your name or business name.")
        if not valid_kenyan_phone(phone):
            errors.append("Enter a valid Kenyan phone number (07XXXXXXXX, 01XXXXXXXX or 254...).")
        if not consent:
            errors.append("Confirm your authorization and consent.")
        if not (-5 <= float(lat) <= 5 and 33 <= float(lon) <= 42):
            errors.append("The coordinates don't look like a location in Kenya. Check latitude and longitude.")
        if errors:
            for error in errors:
                st.error(error)
        else:
            new_id = int(pd.to_numeric(st.session_state.houses["id"], errors="coerce").max()) + 1 if not st.session_state.houses.empty else 1
            photo_url = ""
            if property_photos:
                st.session_state.uploaded_property_photos[new_id] = [f.name for f in property_photos]
                photo_url = ""
            listing = {
                "id": new_id, "town": town, "type": house_type, "rent": int(rent), "deposit": int(deposit),
                "lat": float(lat), "lon": float(lon), "phone": phone.strip(), "photo": photo_url,
                "landlord": name.strip(), "verified": False, "available": True, "description": description.strip(),
            }
            st.session_state.houses = pd.concat([st.session_state.houses, pd.DataFrame([listing])], ignore_index=True)
            st.session_state.submitted_credentials.append({
                "listing_id": new_id, "name": name.strip(), "role": role, "phone": phone.strip(),
                "email": email.strip(), "credential_type": credential_type,
                "credential_reference": credential_reference.strip(), "address_hint": address_hint.strip(),
                "photos": [f.name for f in property_photos] if property_photos else [],
                "supporting_image": credential_photo.name if credential_photo else None,
                "review_status": "Pending manual review",
            })
            st.success(f"Demo submission created with listing ID {new_id}. It is not verified and is not permanently saved.")
            st.info("Before public launch, connect a database and private file storage, add sign-in and admin review, and only then mark a listing verified.")
            st.write("Property GPS preview:")
            st.code(f"Latitude: {lat:.6f}\nLongitude: {lon:.6f}")
            st.link_button("Open coordinates in Google Maps", f"https://www.google.com/maps?q={lat:.6f},{lon:.6f}")
            if property_photos:
                st.image(property_photos[0], caption="First uploaded property photo (temporary preview)", use_container_width=True)

    st.markdown("#### Submission status (this session only)")
    if st.session_state.submitted_credentials:
        status_df = pd.DataFrame([
            {"Listing ID": x["listing_id"], "Submitted by": x["name"], "Role": x["role"], "Status": x["review_status"]}
            for x in st.session_state.submitted_credentials
        ])
        st.dataframe(status_df, use_container_width=True, hide_index=True)
    else:
        st.caption("No submissions in this session yet.")

# ---------------- Satellite map page ----------------
elif page == "🛰️ Satellite property map":
    st.subheader("Property locations")
    st.write("Switch between satellite imagery and street-map layers. Select a marker to view a listing's summary.")
    st.info("Satellite imagery is not live video. Imagery update frequency varies by location and provider.")
    towns = ["All towns"] + sorted(df["town"].dropna().unique().tolist())
    chosen_town = st.selectbox("Filter map by town", towns)
    map_data = df if chosen_town == "All towns" else df[df["town"] == chosen_town]
    show_satellite_map(map_data)
    st.caption("GPS pins are only as accurate as the coordinates submitted. A caretaker must confirm the pin points to the actual property.")

# ---------------- Dashboard page ----------------
elif page == "📊 Rental insights":
    st.subheader("Rental market snapshot")
    st.caption("Statistics are calculated from the current dataset, including demo listings.")
    if df.empty:
        st.info("No listings available yet.")
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("Listings in dataset", len(df))
        c2.metric("Average monthly rent", f"KSh {df['rent'].mean():,.0f}")
        c3.metric("Median monthly rent", f"KSh {df['rent'].median():,.0f}")
        town_avg = df.groupby("town", as_index=False)["rent"].mean().sort_values("rent")
        fig1 = px.bar(town_avg, x="town", y="rent", color="rent", title="Average monthly rent by town",
                      labels={"town": "Town", "rent": "Average rent (KSh)"},
                      color_continuous_scale=["#bde9d9", "#087f5b"])
        fig1.update_layout(showlegend=False, plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig1, use_container_width=True)
        left, right = st.columns(2)
        type_counts = df["type"].value_counts().rename_axis("type").reset_index(name="count")
        fig2 = px.pie(type_counts, names="type", values="count", title="Property types", hole=0.45)
        left.plotly_chart(fig2, use_container_width=True)
        fig3 = px.histogram(df, x="rent", nbins=10, title="Monthly rent distribution",
                            labels={"rent": "Monthly rent (KSh)"}, color_discrete_sequence=["#087f5b"])
        right.plotly_chart(fig3, use_container_width=True)
        st.markdown("#### Listings by town")
        town_table = df.groupby("town", as_index=False).agg(
            Listings=("id", "count"), Average_Rent=("rent", "mean"), Lowest_Rent=("rent", "min")
        ).round(0).rename(columns={"Average_Rent": "Average rent (KSh)", "Lowest_Rent": "Lowest rent (KSh)"})
        st.dataframe(town_table, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("Home Search Kenya · Prototype. Demo records are unverified. Verify property ownership, caretaker authority and payment recipient before paying.")
