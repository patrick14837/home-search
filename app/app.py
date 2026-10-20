import streamlit as st

st.set_page_config(
    page_title="Home Search Kenya",
    layout="wide",
    page_icon="🏠"
)

# ---------------- SESSION STATE & NAVIGATION ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "verified" not in st.session_state:
    st.session_state.verified = False
if "stk" not in st.session_state:
    st.session_state.stk = False

if "page" in st.query_params:
    st.session_state.page = st.query_params["page"]

def go(p):
    st.session_state.page = p
    st.query_params["page"] = p
    st.rerun()

# ---------------- STYLING ----------------
st.markdown("""
<style>
[data-testid="stHeader"] {display:none!important;}
footer {display:none!important;}
.block-container {
    padding-top:0!important;
    padding-left:0!important;
    padding-right:0!important;
    max-width:100%!important;
}
.stApp {background:#FFFFFF;}

/* Dedicated navigation container: reliable green background */
.st-key-top_nav {
    background:#0F3D2E !important;
    padding:14px 20px !important;
    border-bottom:1px solid #0A2D22 !important;
    box-shadow:0 2px 8px rgba(0,0,0,0.12);
}
.st-key-top_nav [data-testid="stHorizontalBlock"] {
    background:#0F3D2E !important;
}
.st-key-top_nav [data-testid="stColumn"] {
    background:transparent !important;
}
.st-key-top_nav [data-testid="stMarkdownContainer"] {
    color:white;
}
.st-key-top_nav [data-testid="stButton"] button {
    min-height:42px;
}

/* Keep the existing hero and page styling */
.hero {
    height:420px;
    background:linear-gradient(to right, rgba(0,0,0,0.65), rgba(0,0,0,0.2)),
    url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1600&q=80');
    background-size:cover;
    background-position:center;
    padding:50px 32px;
    display:flex;
    flex-direction:column;
    justify-content:center;
}
.hero h1 {
    color:white;
    font-size:54px;
    font-weight:800;
    line-height:1.05;
    margin:0;
}
.search-box {
    background:white;
    border-radius:20px;
    padding:22px 22px 12px 22px;
    margin:-40px 32px 20px 32px;
    box-shadow:0 12px 40px rgba(0,0,0,0.12);
    border:1px solid #EFE9E0;
    position:relative;
    z-index:10;
}
.search-box div[data-testid="stHorizontalBlock"] {
    background:white!important;
    padding:0!important;
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
    margin:4px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TOP NAVIGATION ----------------
with st.container(key="top_nav"):
    col_logo, c1, c2, c3, c4 = st.columns(
        [2.8, 1.1, 1, 1.3, 0.9],
        vertical_alignment="center"
    )

    with col_logo:
        st.markdown(
            '<div style="color:white;font-weight:900;font-size:20px;">'
            'Home Search <span style="color:#F7E38E;">Kenya</span></div>',
            unsafe_allow_html=True
        )
    with c1:
        if st.button(
            "Find a Home",
            type="primary" if st.session_state.page == "home" else "secondary",
            use_container_width=True,
            key="bh"
        ):
            go("home")
    with c2:
        if st.button(
            "Landlords",
            type="primary" if st.session_state.page == "landlords" else "secondary",
            use_container_width=True,
            key="bl"
        ):
            go("landlords")
    with c3:
        if st.button(
            "About & Safety",
            type="primary" if st.session_state.page == "about" else "secondary",
            use_container_width=True,
            key="ba"
        ):
            go("about")
    with c4:
        if st.button("Sign in", type="secondary", use_container_width=True, key="bs"):
            go("signin")

# ---------------- HOME PAGE ----------------
if st.session_state.page == "home":
    st.markdown(
        '<div class="hero"><h1>Find a place to<br>call home.</h1>'
        '<p style="color:#E8EDEB;font-size:15px;max-width:420px;margin-top:14px;">'
        'Explore verified rentals in Siaya, Kisumu, Busia, Maseno, Bondo, '
        'Ugunja, Ukwala. Customer Service: 0140311646</p></div>',
        unsafe_allow_html=True
    )

    # Search controls
    with st.container():
        st.markdown('<div class="search-box">', unsafe_allow_html=True)
        sc1, sc2, sc3, sc4 = st.columns([2, 2, 2, 1.2], vertical_alignment="bottom")
        with sc1:
            town = st.selectbox(
                "Town or estate",
                ["All Towns", "Kisumu", "Siaya", "Busia", "Bondo", "Ugunja", "Ukwala", "Maseno"],
                key="town_home"
            )
        with sc2:
            ptype = st.selectbox(
                "Property type",
                ["Any home", "Bedsitter", "1 Bedroom", "2 Bedroom", "3 Bedroom"],
                key="ptype_home"
            )
        with sc3:
            budget = st.selectbox(
                "Monthly budget",
                ["Any budget", "Below 5k", "5k-10k", "10k-15k", "15k+", "20k+"],
                key="bud_home"
            )
        with sc4:
            st.markdown(
                '<div style="margin-bottom:8px;font-size:14px;font-weight:600;">Search</div>',
                unsafe_allow_html=True
            )
            st.button("Search homes", type="primary", use_container_width=True, key="search_btn")
        st.markdown('</div>', unsafe_allow_html=True)

    # Demo listings. Replace/extend this list as real property data becomes available.
    listings = [
        {
            "town": "Maseno",
            "type": "Bedsitter",
            "rent": 5500,
            "name": "Bedsitter - Maseno - Mabungo",
            "image": "https://images.unsplash.com/photo-1605146769289-440113cc3d00?w=600"
        },
        {
            "town": "Siaya",
            "type": "1 Bedroom",
            "rent": 8000,
            "name": "1 Bedroom - Siaya Town",
            "image": "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=600"
        },
        {
            "town": "Kisumu",
            "type": "2 Bedroom",
            "rent": 14000,
            "name": "2 Bedroom - Kisumu - Milimani",
            "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=600"
        }
    ]

    filtered = listings

    if town != "All Towns":
        filtered = [house for house in filtered if house["town"] == town]

    if ptype != "Any home":
        filtered = [house for house in filtered if house["type"] == ptype]

    if budget == "Below 5k":
        filtered = [house for house in filtered if house["rent"] < 5000]
    elif budget == "5k-10k":
        filtered = [house for house in filtered if 5000 <= house["rent"] <= 10000]
    elif budget == "10k-15k":
        filtered = [house for house in filtered if 10000 < house["rent"] <= 15000]
    elif budget == "15k+":
        filtered = [house for house in filtered if house["rent"] >= 15000]
    elif budget == "20k+":
        filtered = [house for house in filtered if house["rent"] >= 20000]

    st.markdown(
        f'<div style="padding:24px 32px 0 32px;">'
        f'<h2 style="color:#0F3D2E;margin-bottom:4px;">Homes you might love</h2>'
        f'<p style="color:#6B7A75;font-size:13px;margin-top:0;">'
        f'Showing {len(filtered)} matching sample listing(s) · {town} · {ptype} · {budget}'
        f'</p></div>',
        unsafe_allow_html=True
    )

    if filtered:
        property_cols = st.columns(3)
        for i, house in enumerate(filtered):
            with property_cols[i % 3]:
                st.image(house["image"], use_container_width=True)
                st.markdown(
                    f"**{house['name']}**\n\n"
                    f"KSh {house['rent']:,} / month\n\n"
                    f"<span class='trust-badge'>Sample Listing</span> "
                    f"<span class='trust-badge'>{house['town']}</span>",
                    unsafe_allow_html=True
                )
    else:
        st.info(
            f"No sample houses match your filters in {town}. "
            "Try another town, property type, or budget."
        )

# ---------------- LANDLORDS PAGE ----------------
elif st.session_state.page == "landlords":
    st.markdown(
        '<div style="padding:24px 32px 0 32px;">'
        '<h1 style="color:#0F3D2E;font-weight:900;">List your house - Get tenants fast</h1>'
        '<p style="color:#6B7A75;">7 towns covered. $10 verification code 123456 - '
        'Support: 0140311646</p></div>',
        unsafe_allow_html=True
    )
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    full_name = st.text_input("Full Name *")
    phone = st.text_input("Phone / WhatsApp *", placeholder="0140311646")
    town_ll = st.selectbox(
        "Town *", ["Kisumu", "Siaya", "Busia", "Bondo", "Ugunja", "Ukwala", "Maseno"]
    )
    rent = st.number_input("Monthly Rent (KSh) *", value=6500, step=500)
    desc = st.text_area("House Description *")

    if st.button("Request M-Pesa STK Push - $10", type="primary", key="stk"):
        st.session_state.stk = True
        st.success("Demo only: no real M-Pesa STK push has been sent. Phone entered: {}".format(phone))

    if st.session_state.stk:
        code = st.text_input("Enter demo verification code", key="code")
        if st.button("Verify Code", key="ver"):
            if code == "123456":
                st.session_state.verified = True
                st.balloons()
                st.success("Demo verification successful.")
            else:
                st.error("Invalid demo code.")

    if st.session_state.verified:
        if st.button("Submit - Make LIVE", type="primary", use_container_width=True):
            st.warning(
                f"Demo listing submitted for {full_name} in {town_ll}. "
                "It has not been published to a live property database."
            )
    else:
        st.warning("Complete the demo verification first.")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- ABOUT & SAFETY PAGE ----------------
elif st.session_state.page == "about":
    st.markdown(
        '<div style="padding:24px 32px 0 32px;">'
        '<h1 style="color:#0F3D2E;font-weight:900;font-size:38px;">About Home Search Kenya</h1>'
        '<p style="color:#5A6B66;">Rental platform for Western Kenya. Customer Service: '
        '<b>0140311646</b></p></div>',
        unsafe_allow_html=True
    )
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        <div class="form-card" style="margin:16px 0 16px 32px;">
          <h3 style="color:#0F3D2E;margin-top:0;">Who We Are</h3>
          <p style="color:#4A5A55;line-height:1.8;">
          Home Search Kenya aims to help people find rentals in Western Kenya.
          We cover Kisumu, Siaya, Busia, Maseno, Bondo, Ugunja and Ukwala.
          <br><br>
          <b>Office details:</b> Add and verify your actual business address before publishing it.
          <br><br>
          <b>Verification:</b> Listings should be checked before being advertised as verified.
          </p>
          <h3 style="color:#0F3D2E;">How It Works</h3>
          <p style="color:#4A5A55;line-height:1.8;">
          <b>Tenants:</b> Search by town, property type and budget. Visit a property before paying.<br>
          <b>Landlords:</b> Submit accurate property details and complete a real verification process.
          </p>
        </div>
        <div style="padding:0 0 0 32px;">
          <h2 style="color:#0F3D2E;">Safety Center - 0140311646</h2>
          <div class="safety-card">
            <h4 style="margin:0 0 8px 0;color:#0F3D2E;">For Tenants - 5 Golden Rules</h4>
            <ol style="color:#4A5A55;line-height:1.9;margin:0;">
              <li><b>Never pay before viewing</b> the property.</li>
              <li>Check water, electricity, doors and locks.</li>
              <li>Ask for identification and proof the person can rent the property.</li>
              <li>Keep payment records and get a receipt.</li>
              <li>Report suspicious listings to the appropriate authorities.</li>
            </ol>
          </div>
          <div class="safety-card" style="border-left-color:#C0392B;">
            <h4 style="margin:0 0 8px 0;color:#C0392B;">Red Flags</h4>
            <ul style="color:#4A5A55;line-height:1.8;margin:0;">
              <li>Deposit demanded before viewing.</li>
              <li>Unusually low rent or pressure to pay immediately.</li>
              <li>Refusal to meet or show the property.</li>
              <li>No credible proof of identity or authority to rent.</li>
            </ul>
          </div>
          <div class="safety-card" style="border-left-color:#F7E38E;">
            <h4 style="margin:0 0 8px 0;">For Landlords</h4>
            <p style="color:#4A5A55;line-height:1.8;margin:0;">
            Provide accurate rent, availability, photos and proof that you are authorised to list the property.
            </p>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="form-card" style="margin:16px 32px 16px 0;">
          <h3 style="color:#0F3D2E;margin-top:0;">Customer Service</h3>
          <p style="color:#4A5A55;line-height:2;">
          <b>Phone / WhatsApp:</b><br>0140311646<br><br>
          <b>Email:</b><br>support@homesearch.co.ke<br><br>
          <b>Business address:</b><br>Add your confirmed business address here.
          </p>
          <hr>
          <h4 style="color:#0F3D2E;">Trust and Legal</h4>
          <p style="color:#4A5A55;font-size:13px;line-height:1.7;">
          Verify landlord identity and listing details before displaying a verified label.<br>
          Encourage tenants to view properties before paying.<br>
          Explain any fees and refund terms clearly before collecting money.
          </p>
        </div>
        """, unsafe_allow_html=True)

# ---------------- SIGN-IN PAGE ----------------
elif st.session_state.page == "signin":
    st.markdown(
        '<div style="padding:24px 32px;">'
        '<h2 style="color:#0F3D2E;">Sign in - Support: 0140311646</h2></div>',
        unsafe_allow_html=True
    )
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.text_input("Phone")
    st.text_input("Password", type="password")
    if st.button("Sign in", type="primary"):
        st.info("Sign-in is a demo only; authentication has not been connected.")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown(
    '<div style="text-align:center;padding:20px;color:#8A9A95;font-size:12px;'
    'background:white;margin-top:20px;border-top:1px solid #EDE9E0;">'
    '2026 Home Search Kenya - 0140311646 - Sample listings only - Never pay before viewing'
    '</div>',
    unsafe_allow_html=True
)
