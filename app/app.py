import streamlit as st

st.set_page_config(page_title="Home Search Kenya", layout="wide", page_icon="🏠")

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

/* GREEN TOP NAVIGATION BAR */
.st-key-top_nav {
    background: #0F3D2E !important;
    padding: 14px 20px !important;
    border-bottom: 1px solid #0A2D22 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.12);
}
.st-key-top_nav [data-testid="stHorizontalBlock"] {
    background: #0F3D2E !important;
}
.st-key-top_nav [data-testid="stColumn"] {
    background: transparent !important;
}
.st-key-top_nav [data-testid="stMarkdownContainer"] {
    color: white !important;
}

/* Black text on inactive navigation buttons */
.st-key-top_nav button[kind="secondary"],
.st-key-top_nav button[kind="secondary"] p,
.st-key-top_nav button[kind="secondary"] span {
    color: #000000 !important;
}

/* Keep the active navigation button coral with readable white text */
.st-key-top_nav button[kind="primary"],
.st-key-top_nav button[kind="primary"] p,
.st-key-top_nav button[kind="primary"] span {
    color: #FFFFFF !important;
}

/* Hero and page styles */
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
    background:white !important;
    padding:0 !important;
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
.property-card {
    background:#FFFFFF;
    border:1px solid #EFE9E0;
    border-radius:14px;
    padding:12px;
    margin-bottom:20px;
    box-shadow:0 5px 18px rgba(0,0,0,0.07);
}
</style>
""", unsafe_allow_html=True)


# Navigation bar: green background; inactive buttons have black text.
with st.container(key="top_nav"):
    col_logo, c1, c2, c3, c4 = st.columns(
        [2.8, 1.1, 1, 1.3, 0.9],
        vertical_alignment="center"
    )
    with col_logo:
        st.markdown(
            '<div style="color:white; font-weight:900; font-size:20px;">'
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
        if st.button(
            "Sign in",
            type="secondary",
            use_container_width=True,
            key="bs"
        ):
            go("signin")


if st.session_state.page == "home":
    st.markdown(
        '<div class="hero"><h1>Find a place to<br>call home.</h1>'
        '<p style="color:#E8EDEB; font-size:15px; max-width:420px; margin-top:14px;">'
        'Explore rentals in Siaya, Kisumu, Busia, Maseno, Bondo, Ugunja, Ukwala. '
        'Customer Service: 0140311646</p></div>',
        unsafe_allow_html=True
    )

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
                '<div style="margin-bottom:8px; font-size:14px; font-weight:600;">Search</div>',
                unsafe_allow_html=True
            )
            if st.button("Search homes", type="primary", use_container_width=True, key="search_btn"):
                st.toast(f"Showing homes for {town} - {ptype} - {budget}")
        st.markdown('</div>', unsafe_allow_html=True)

    # Clearly labelled demonstration listings. These are not verified real rentals.
    listings = [
        {"town": "Maseno", "type": "Bedsitter", "rent": 5500,
         "name": "Bedsitter - Maseno - Mabungo",
         "image": "https://images.unsplash.com/photo-1605146769289-440113cc3d00?w=800"},
        {"town": "Maseno", "type": "1 Bedroom", "rent": 7500,
         "name": "1 Bedroom - Maseno Town",
         "image": "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800"},
        {"town": "Siaya", "type": "1 Bedroom", "rent": 8000,
         "name": "1 Bedroom - Siaya Town",
         "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800"},
        {"town": "Siaya", "type": "Bedsitter", "rent": 4500,
         "name": "Bedsitter - Siaya",
         "image": "https://images.unsplash.com/photo-1605146769289-440113cc3d00?w=800"},
        {"town": "Kisumu", "type": "2 Bedroom", "rent": 14000,
         "name": "2 Bedroom - Kisumu - Milimani",
         "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800"},
        {"town": "Kisumu", "type": "Bedsitter", "rent": 6500,
         "name": "Bedsitter - Kisumu",
         "image": "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800"},
        {"town": "Busia", "type": "1 Bedroom", "rent": 7000,
         "name": "1 Bedroom - Busia Town",
         "image": "https://images.unsplash.com/photo-1605146769289-440113cc3d00?w=800"},
        {"town": "Busia", "type": "Bedsitter", "rent": 5000,
         "name": "Bedsitter - Busia",
         "image": "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800"},
        {"town": "Bondo", "type": "Bedsitter", "rent": 4500,
         "name": "Bedsitter - Bondo",
         "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800"},
        {"town": "Bondo", "type": "2 Bedroom", "rent": 11000,
         "name": "2 Bedroom - Bondo",
         "image": "https://images.unsplash.com/photo-1605146769289-440113cc3d00?w=800"},
        {"town": "Ugunja", "type": "Bedsitter", "rent": 4000,
         "name": "Bedsitter - Ugunja",
         "image": "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800"},
        {"town": "Ugunja", "type": "1 Bedroom", "rent": 6500,
         "name": "1 Bedroom - Ugunja",
         "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800"},
        {"town": "Ukwala", "type": "Bedsitter", "rent": 3500,
         "name": "Bedsitter - Ukwala",
         "image": "https://images.unsplash.com/photo-1605146769289-440113cc3d00?w=800"},
        {"town": "Ukwala", "type": "1 Bedroom", "rent": 6000,
         "name": "1 Bedroom - Ukwala",
         "image": "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800"},
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
        f'<h2 style="color:#0F3D2E; margin-bottom:4px;">Homes you might love</h2>'
        f'<p style="color:#6B7A75; font-size:13px; margin-top:0;">'
        f'{len(filtered)} demonstration listing(s) · {town} · {ptype} · {budget}. '
        f'Listings shown are examples, not confirmed available rentals.</p></div>',
        unsafe_allow_html=True
    )

    if filtered:
        cols = st.columns(3)
        for index, house in enumerate(filtered):
            with cols[index % 3]:
                st.image(house["image"], use_container_width=True)
                st.markdown(
                    f"**{house['name']}**\n\n"
                    f"KSh {house['rent']:,} / month\n\n"
                    f"<span class='trust-badge'>Demo listing</span> "
                    f"<span class='trust-badge'>{house['town']}</span>",
                    unsafe_allow_html=True
                )
    else:
        st.info(
            "No demonstration listings match those filters. "
            "Try another town, property type, or monthly budget."
        )


elif st.session_state.page == "landlords":
    st.markdown(
        '<div style="padding:24px 32px 0 32px;">'
        '<h1 style="color:#0F3D2E; font-weight:900;">List your house - Get tenants fast</h1>'
        '<p style="color:#6B7A75;">7 towns covered. Demo verification code 123456 - Support: 0140311646</p>'
        '</div>',
        unsafe_allow_html=True
    )
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    full_name = st.text_input("Full Name *")
    phone = st.text_input("Phone / WhatsApp *", placeholder="07XXXXXXXX")
    town_ll = st.selectbox(
        "Town *",
        ["Kisumu", "Siaya", "Busia", "Bondo", "Ugunja", "Ukwala", "Maseno"]
    )
    rent = st.number_input("Monthly Rent (KSh) *", min_value=0, value=6500, step=500)
    desc = st.text_area("House Description *")
    st.caption("Demo only: this form does not collect a real payment or publish a live listing.")
    if st.button("Demo M-Pesa STK Push - $10", type="primary", key="stk"):
        st.session_state.stk = True
        st.info("Demo flow only. No real STK push has been sent.")
    if st.session_state.stk:
        code = st.text_input("Enter demo verification code", key="code")
        if st.button("Verify Code", key="ver"):
            if code == "123456":
                st.session_state.verified = True
                st.success("Demo verification complete.")
            else:
                st.error("Incorrect demo code. Use 123456.")
    if st.session_state.verified:
        if st.button("Submit demo listing", type="primary", use_container_width=True):
            st.success(
                f"Demo listing details entered for {full_name or 'landlord'} in {town_ll}. "
                "This has not been published to a live property database."
            )
    else:
        st.warning("Complete the demo verification steps to test this flow.")
    st.markdown('</div>', unsafe_allow_html=True)


elif st.session_state.page == "about":
    st.markdown(
        '<div style="padding:24px 32px 0 32px;">'
        '<h1 style="color:#0F3D2E; font-weight:900; font-size:38px;">About Home Search Kenya</h1>'
        '<p style="color:#5A6B66;">Rental search demonstration for Western Kenya. '
        'Customer Service: <b>0140311646</b></p></div>',
        unsafe_allow_html=True
    )
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <div class="form-card" style="margin:16px 0 16px 32px;">
          <h3 style="color:#0F3D2E; margin-top:0;">Who We Are</h3>
          <p style="color:#4A5A55; line-height:1.8;">
          Home Search Kenya is a rental-platform prototype for exploring properties in
          Kisumu, Siaya, Busia, Maseno, Bondo, Ugunja and Ukwala.
          <br><br>
          <b>Important:</b> The properties currently shown are sample listings for demonstration.
          They have not been confirmed as available, and this prototype does not verify landlord IDs.
          </p>
          <h3 style="color:#0F3D2E;">How It Works</h3>
          <p style="color:#4A5A55; line-height:1.8;">
          <b>Tenants:</b> Filter the sample listings by town, property type and budget.
          Always physically view a property and independently confirm the landlord before paying.
          <br><br>
          <b>Landlords:</b> The current form is a demo and does not publish a real listing or process payment.
          </p>
        </div>
        <div style="padding:0 0 0 32px;">
          <h2 style="color:#0F3D2E;">Safety Center</h2>
          <div class="safety-card">
            <h4 style="margin:0 0 8px 0; color:#0F3D2E;">For Tenants - Safety Tips</h4>
            <ol style="color:#4A5A55; line-height:1.9; margin:0;">
              <li>Never pay before viewing the property.</li>
              <li>Meet at the property and check water, electricity and locks.</li>
              <li>Ask for identification and evidence that the person can rent the property.</li>
              <li>Get a written agreement and receipt for any payment.</li>
              <li>Be cautious of unusually low prices or pressure to pay immediately.</li>
            </ol>
          </div>
          <div class="safety-card" style="border-left-color:#C0392B;">
            <h4 style="margin:0 0 8px 0; color:#C0392B;">Red Flags</h4>
            <ul style="color:#4A5A55; line-height:1.8; margin:0;">
              <li>Requests a deposit before a viewing.</li>
              <li>Refuses to meet in person.</li>
              <li>Pressures you to pay immediately.</li>
              <li>Cannot provide evidence of identity or authority to rent the property.</li>
            </ul>
          </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="form-card" style="margin:16px 32px 16px 0;">
          <h3 style="color:#0F3D2E; margin-top:0;">Customer Service</h3>
          <p style="color:#4A5A55; line-height:2;">
          <b>Phone / WhatsApp:</b><br>0140311646<br><br>
          <b>Support hours:</b><br>To be confirmed<br><br>
          <b>Email:</b><br>To be confirmed<br><br>
          <b>Office address:</b><br>To be confirmed
          </p>
          <hr>
          <h4 style="color:#0F3D2E;">Trust and Safety</h4>
          <p style="color:#4A5A55; font-size:13px; line-height:1.7;">
          Listings on this prototype are examples only.<br>
          Landlord identity verification is not yet connected.<br>
          Real M-Pesa payments are not enabled.<br>
          Always view a house before paying.
          </p>
        </div>
        """, unsafe_allow_html=True)


elif st.session_state.page == "signin":
    st.markdown(
        '<div style="padding:24px 32px;">'
        '<h2 style="color:#0F3D2E;">Sign in - Home Search Kenya</h2></div>',
        unsafe_allow_html=True
    )
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.text_input("Phone")
    st.text_input("Password", type="password")
    st.caption("Sign-in is a visual prototype; account authentication is not connected.")
    if st.button("Sign in", type="primary"):
        st.info("Authentication is not yet enabled in this prototype.")
    st.markdown('</div>', unsafe_allow_html=True)


st.markdown(
    '<div style="text-align:center; padding:20px; color:#8A9A95; font-size:12px; '
    'background:white; margin-top:20px; border-top:1px solid #EDE9E0;">'
    '2026 Home Search Kenya - Sample listings for demonstration - '
    'Always view a house before paying</div>',
    unsafe_allow_html=True
)
