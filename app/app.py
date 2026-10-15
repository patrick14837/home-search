import streamlit as st

st.set_page_config(page_title="Home Search Kenya", page_icon="🏠", layout="wide")

for key, value in {
    "page": "home", "verified": False, "stk": False,
    "search_submitted": False,
    "properties": [
        {"town":"Maseno","type":"Bedsitter","rent":5500,"title":"Affordable bedsitter in Maseno","image":"https://images.unsplash.com/photo-1605146769289-440113cc3d00?auto=format&fit=crop&w=900&q=85","description":"A compact rental option close to local amenities."},
        {"town":"Maseno","type":"1 Bedroom","rent":8000,"title":"Comfortable one-bedroom home","image":"https://images.unsplash.com/photo-1568605114967-8130f3a36994?auto=format&fit=crop&w=900&q=85","description":"A practical home with space to relax."},
        {"town":"Kisumu","type":"2 Bedroom","rent":14000,"title":"Spacious two-bedroom home","image":"https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=900&q=85","description":"A spacious option for a small family or housemates."},
    ]
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

try:
    page = st.query_params.get("page", "")
    if page in {"home", "landlords", "about", "signin"}:
        st.session_state.page = page
except Exception:
    pass

def go(page):
    st.session_state.page = page
    try:
        st.query_params["page"] = page
    except Exception:
        pass
    st.rerun()

st.markdown("""
<style>
:root{--green:#0F3D2E;--gold:#F7E38E;--cream:#FFFBF2;--muted:#64736D}
[data-testid="stHeader"],footer,#MainMenu{visibility:hidden;height:0}
.block-container{padding:0 0 2rem!important;max-width:100%!important}
.stApp{background:var(--cream)}
.brand{font-size:23px;font-weight:900;color:white;padding:8px 0;white-space:nowrap}
.brand span{color:var(--gold)}
div[data-testid="stButton"] button{border-radius:10px;min-height:42px;font-weight:700}
div[data-testid="stButton"] button[kind="primary"]{background:var(--green);border:1px solid var(--green);color:white}
.hero{min-height:480px;display:flex;flex-direction:column;justify-content:center;padding:50px 4%;color:white;background-image:linear-gradient(90deg,rgba(0,0,0,.66),rgba(0,0,0,.12)),url("https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=2000&q=90");background-size:cover;background-position:center 55%}
.hero h1{font-size:clamp(40px,5vw,68px);font-weight:850;line-height:1.02;margin:0 0 20px;color:white}
.hero p{font-size:18px;line-height:1.6;max-width:480px;color:#f0f3f1}
.search-shell{background:white;border-radius:18px;padding:18px 22px;margin:-42px auto 0;width:88%;position:relative;z-index:5;box-shadow:0 14px 40px #0002;border:1px solid #eee9df}
.section{padding:30px 4% 0}.section h2{color:var(--green);font-size:28px;font-weight:850;margin-bottom:4px}.subtle{color:var(--muted)}
.property-card{background:white;border:1px solid #eee9df;border-radius:16px;overflow:hidden;box-shadow:0 5px 18px #0f3d2e12;margin-bottom:18px}
.property-card img{width:100%;height:205px;object-fit:cover;display:block}.property-content{padding:16px}
.price{font-size:21px;font-weight:850;color:var(--green)}.pill{display:inline-block;background:#edf5ef;color:var(--green);padding:5px 9px;border-radius:30px;font-size:12px;font-weight:700}
.form-card{background:white;border-radius:16px;padding:24px;box-shadow:0 8px 30px #0001;border:1px solid #eee9e0;margin:22px 4%}
.safety-card{background:white;border-radius:12px;padding:20px;border-left:4px solid var(--green);box-shadow:0 4px 16px #0001;margin-bottom:16px}
.footer{text-align:center;padding:30px 15px 10px;color:#82918b;font-size:12px}
@media(max-width:700px){.hero{min-height:390px;padding:35px 6%}.search-shell{width:92%;padding:15px}.brand{font-size:18px}}
</style>
""", unsafe_allow_html=True)

# Navigation remains functional through native Streamlit buttons.
st.markdown('<div style="background:#0F3D2E;padding:8px 3.5% 0">', unsafe_allow_html=True)
brand, n1, n2, n3, n4 = st.columns([2.8,1.2,1,1.4,.9], vertical_alignment="center")
with brand:
    st.markdown('<div class="brand">🏠 Home Search <span>Kenya</span></div>', unsafe_allow_html=True)
with n1:
    if st.button("Find a Home", key="nav_home", use_container_width=True): go("home")
with n2:
    if st.button("Landlords", key="nav_landlords", use_container_width=True): go("landlords")
with n3:
    if st.button("About & Safety", key="nav_about", use_container_width=True): go("about")
with n4:
    if st.button("👤 Sign in", key="nav_signin", use_container_width=True): go("signin")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown("""<style>
/* Secondary buttons in the navigation are light against the green header. */
div[data-testid="stHorizontalBlock"] button[kind="secondary"]{background:rgba(255,255,255,.08);color:white;border:1px solid rgba(255,255,255,.22)}
</style>""", unsafe_allow_html=True)

if st.session_state.page == "home":
    st.markdown('<section class="hero"><h1>Find a place to<br>call home.</h1><p>Explore rental homes in Siaya, Kisumu, Busia, Maseno and nearby towns.</p></section>', unsafe_allow_html=True)
    st.markdown('<div class="search-shell">', unsafe_allow_html=True)
    a,b,c,d = st.columns([2,2,2,1.35], vertical_alignment="bottom")
    with a: town = st.selectbox("📍 Town or estate", ["Kisumu","Siaya","Busia","Bondo","Ugunja","Ukwala","Maseno"], key="home_town")
    with b: ptype = st.selectbox("🏠 Property type", ["Any home","Bedsitter","1 Bedroom","2 Bedroom","3 Bedroom"], key="home_type")
    with c: budget = st.selectbox("💰 Monthly budget", ["Any budget","Below 5k","5k–10k","10k–15k","15k+"], key="home_budget")
    with d:
        if st.button("🔎 Search homes", type="primary", use_container_width=True):
            st.session_state.search_town = town
            st.session_state.search_type = ptype
            st.session_state.search_budget = budget
            st.session_state.search_submitted = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="section"><h2>Homes you might love</h2><p class="subtle">Explore available rental options.</p></div>', unsafe_allow_html=True)
    listings = st.session_state.properties
    if st.session_state.search_submitted:
        listings = [p for p in listings if p["town"] == st.session_state.search_town]
        if st.session_state.search_type != "Any home":
            listings = [p for p in listings if p["type"] == st.session_state.search_type]
        budget = st.session_state.search_budget
        if budget == "Below 5k": listings = [p for p in listings if p["rent"] < 5000]
        elif budget == "5k–10k": listings = [p for p in listings if 5000 <= p["rent"] <= 10000]
        elif budget == "10k–15k": listings = [p for p in listings if 10000 <= p["rent"] <= 15000]
        elif budget == "15k+": listings = [p for p in listings if p["rent"] > 15000]
        st.caption(f'Results for {st.session_state.search_town} · {st.session_state.search_type} · {budget}')
    if not listings:
        st.info("No matching properties are listed yet. Try another town, type or budget.")
    else:
        cards = st.columns(3)
        for i, p in enumerate(listings):
            with cards[i % 3]:
                st.markdown(f'''<div class="property-card"><img src="{p['image']}" alt="Rental property"><div class="property-content"><span class="pill">{p['type']} · {p['town']}</span><h3 style="color:#173f32;margin:12px 0 6px">{p['title']}</h3><div class="price">KSh {p['rent']:,}<span style="font-size:13px;font-weight:500;color:#64736D"> / month</span></div><p style="color:#64736D;font-size:14px">{p['description']}</p></div></div>''', unsafe_allow_html=True)

elif st.session_state.page == "landlords":
    st.markdown('<div class="section"><h2>List your house — get tenants faster</h2><p class="subtle">Submit property details for Kisumu, Siaya, Busia, Maseno and nearby towns.</p></div>', unsafe_allow_html=True)
    st.warning("DEMO ONLY: verification below does not send a real M-Pesa request or confirm payment.")
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        full_name = st.text_input("Full name *")
        id_number = st.text_input("National ID number *")
        phone = st.text_input("Phone / WhatsApp *", placeholder="07XXXXXXXX")
    with c2:
        town_ll = st.selectbox("Town *", ["Kisumu","Siaya","Busia","Bondo","Ugunja","Ukwala","Maseno"])
        estate = st.text_input("Estate / area *", placeholder="Maseno town")
        alt_phone = st.text_input("Alternative phone (optional)")
    x,y,z = st.columns(3)
    with x: p_type = st.selectbox("Property type *", ["Bedsitter","1 Bedroom","2 Bedroom","3 Bedroom"])
    with y: rent = st.number_input("Monthly rent (KSh) *", min_value=0, value=6500, step=500)
    with z: rooms = st.selectbox("Number of rooms", ["1","2","3","4+"])
    desc = st.text_area("House description *")
    photos = st.file_uploader("Upload at least 3 property photos", accept_multiple_files=True, type=["jpg","jpeg","png"])
    if st.button("Demo: request M-Pesa STK push — $10", type="primary", use_container_width=True):
        st.session_state.stk = True
        st.warning("Demo only: no actual STK push was sent. Connect Safaricom Daraja before accepting payments.")
    if st.session_state.stk:
        code = st.text_input("Demo verification code", key="demo_code", help="Prototype code: 123456")
        if st.button("Verify demo code", key="verify_demo"):
            if code == "123456":
                st.session_state.verified = True
                st.success("Demo code accepted; identity and payment are not verified.")
            else: st.error("Incorrect demo code. Prototype code is 123456.")
    if st.session_state.verified and st.button("Submit property for review", type="primary", use_container_width=True):
        missing = [label for label,val in [("full name",full_name),("ID number",id_number),("phone",phone),("estate/area",estate),("description",desc)] if not val.strip()]
        if missing: st.error("Please complete: " + ", ".join(missing) + ".")
        elif len(photos or []) < 3: st.error("Please upload at least 3 photos.")
        else: st.success("Demo form validated. The listing is not saved or published yet; database and admin review still need connecting.")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "about":
    st.markdown('<div class="section"><h2>About Home Search Kenya</h2><p class="subtle">A rental-search project focused on Siaya, Kisumu, Busia, Maseno and nearby towns.</p></div>', unsafe_allow_html=True)
    left,right = st.columns([1.7,1], gap="large")
    with left:
        st.markdown('''<div class="form-card"><h3 style="color:#0F3D2E">Our goal</h3><p style="color:#4A5A55;line-height:1.8">Help tenants discover rental options and help landlords present properties clearly. Listings should be reviewed before being described as verified.</p><h3 style="color:#0F3D2E">Tenant safety</h3><ul style="color:#4A5A55;line-height:1.9"><li>View the property before paying rent or a deposit.</li><li>Confirm the landlord or agent's identity and authority.</li><li>Never share one-time PINs or M-Pesa confirmation codes.</li><li>Keep payment and viewing records.</li></ul></div>''', unsafe_allow_html=True)
    with right:
        st.markdown('''<div class="form-card"><h3 style="color:#0F3D2E">Customer support</h3><p style="color:#4A5A55;line-height:1.8">Add your confirmed official phone and WhatsApp details here.</p><p style="color:#4A5A55">Location focus: Maseno and nearby towns.</p></div>''', unsafe_allow_html=True)

elif st.session_state.page == "signin":
    st.markdown('<div class="section"><h2>Welcome back</h2><p class="subtle">Sign in to Home Search Kenya.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    phone_login = st.text_input("Phone number")
    password_login = st.text_input("Password", type="password")
    if st.button("Sign in", type="primary", use_container_width=True):
        st.warning("Sign-in is currently a visual prototype. Authentication and accounts are not connected yet.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">© 2026 Home Search Kenya · Rental listings for Western Kenya</div>', unsafe_allow_html=True)
