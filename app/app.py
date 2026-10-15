import streamlit as st

st.set_page_config(page_title="Home Search Kenya", layout="wide", page_icon="🏠")

if "page" not in st.session_state: st.session_state.page="home"
if "verified" not in st.session_state: st.session_state.verified=False
if "stk" not in st.session_state: st.session_state.stk=False

st.markdown("""
<style>
[data-testid="stHeader"]{display:none;}
.block-container{padding:0!important; max-width:100%!important;}
.stApp{background:#FFFBF2;}
.hero{height:420px; background:linear-gradient(to right, rgba(0,0,0,0.62), rgba(0,0,0,0.15)), url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1600&q=80'); background-size:cover; background-position:center; padding:40px 32px; display:flex; flex-direction:column; justify-content:center;}
.hero h1{color:white; font-size:52px; font-weight:800; line-height:1.05; margin:0; text-shadow:0 2px 20px rgba(0,0,0,0.4);}
.search-box{background:white; border-radius:16px; padding:16px 16px; margin:-28px 32px 0 32px; box-shadow:0 12px 40px rgba(0,0,0,0.18); position:relative; z-index:10;}
</style>
""", unsafe_allow_html=True)

# ===== TOP BAR WITH NAV BUTTONS INSIDE - DARK GREEN =====
t1, t2, t3, t4, t5 = st.columns([2.6, 1, 0.9, 1.3, 1])
with t1:
    st.markdown('<div style="background:#0F3D2E; color:white; font-weight:800; font-size:20px; padding:14px 12px; margin-bottom:0;">🏠 Home Search <span style="color:#F7E38E;">Kenya</span></div>', unsafe_allow_html=True)
with t2:
    if st.button("Find a Home", use_container_width=True, key="nav_home"):
        st.session_state.page="home"; st.rerun()
with t3:
    if st.button("Landlords", use_container_width=True, key="nav_land"):
        st.session_state.page="landlords"; st.rerun()
with t4:
    if st.button("About & Safety", use_container_width=True, key="nav_about"):
        st.session_state.page="about"; st.rerun()
with t5:
    if st.button("👤 Sign in", use_container_width=True, key="nav_sign"):
        st.session_state.page="signin"; st.rerun()

st.markdown('<div style="background:#0F3D2E; height:60px; margin-top:-60px;"></div>', unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
<h1>Find a place to<br>call home.</h1>
<p style="color:#E8EDEB; font-size:15px; max-width:360px; margin-top:12px;">Explore verified rentals in Siaya, Kisumu, Busia, Maseno and nearby towns.</p>
</div>
""", unsafe_allow_html=True)

# Search - WITH MASENO ADDED
st.markdown('<div class="search-box">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns([2,2,2,1.3])
with c1:
    town = st.selectbox("📍 Town or estate", ["Kisumu","Siaya","Busia","Bondo","Ugunja","Ukwala","Maseno"], key="town_sel")
with c2:
    ptype = st.selectbox("🏠 Property type", ["Any home","Bedsitter","1 Bedroom","2 Bedroom","3 Bedroom"], key="type_sel")
with c3:
    budget = st.selectbox("💰 Monthly budget", ["Any budget","Below 5k","5k-10k","10k-15k","15k+"], key="bud_sel")
with c4:
    st.write(""); st.write("")
    do_search = st.button("🔍 Search homes", type="primary", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Data - INCLUDING MASENO
all_homes = [
    {"town":"Kisumu","type":"Bedsitter","price":"KSh 6,500/mo","n":6500,"area":"Nyalenda","img":"https://images.unsplash.com/photo-1605146769289-440113cc3d00?w=600"},
    {"town":"Siaya","type":"1 Bedroom","price":"KSh 9,000/mo","n":9000,"area":"Siaya Town","img":"https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=600"},
    {"town":"Busia","type":"2 Bedroom","price":"KSh 14,000/mo","n":14000,"area":"Busia Town","img":"https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=600"},
    {"town":"Bondo","type":"Bedsitter","price":"KSh 5,000/mo","n":5000,"area":"Bondo Center","img":"https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=600"},
    {"town":"Maseno","type":"Bedsitter","price":"KSh 5,500/mo","n":5500,"area":"Maseno University","img":"https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=600"},
    {"town":"Maseno","type":"1 Bedroom","price":"KSh 8,000/mo","n":8000,"area":"Maseno Town","img":"https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=600"},
    {"town":"Kisumu","type":"2 Bedroom","price":"KSh 18,000/mo","n":18000,"area":"Milimani","img":"https://images.unsplash.com/photo-1600585154526-990dced4db0d?w=600"},
    {"town":"Ugunja","type":"1 Bedroom","price":"KSh 8,500/mo","n":8500,"area":"Ugunja Market","img":"https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?w=600"},
]

# Pages
if st.session_state.page == "home":
    filtered = all_homes
    if ptype!= "Any home":
        filtered = [h for h in filtered if h["type"]==ptype]
    if town:
        filtered = [h for h in filtered if h["town"]==town] if town!= "Kisumu" or do_search else filtered
        if do_search:
            filtered = [h for h in all_homes if h["town"]==town]
            if ptype!="Any home": filtered=[h for h in filtered if h["type"]==ptype]

    if budget == "Below 5k": filtered=[h for h in filtered if h["n"]<5000]
    if budget == "5k-10k": filtered=[h for h in filtered if 5000<=h["n"]<=10000]
    if budget == "10k-15k": filtered=[h for h in filtered if 10000<=h["n"]<=15000]
    if budget == "15k+": filtered=[h for h in filtered if h["n"]>=15000]

    st.markdown(f'<div style="padding:22px 32px 0 32px;"><h2 style="color:#0F3D2E; font-weight:800; margin:0;">Homes you might love</h2><p style="color:#6B7A75; font-size:13px;">Found {len(filtered)} homes in {town}</p></div>', unsafe_allow_html=True)

    cols = st.columns(3)
    for i, h in enumerate(filtered[:9]):
        with cols[i%3]:
            st.image(h["img"], use_container_width=True)
            st.markdown(f'**{h["type"]} • {h["town"]}** \n{h["price"]} \n📍 {h["area"]}')
            if st.button(f"View • {h['area']}", key=f"view_{i}", use_container_width=True):
                st.toast(f"Viewing {h['area']}")
                st.session_state.selected = h
                st.session_state.page = "detail"
                st.rerun()
    if do_search:
        st.balloons()
        st.success(f"Found {len(filtered)} {ptype} in {town}!")

elif st.session_state.page == "landlords":
    st.markdown('<div style="padding:28px 32px;"><h2 style="color:#0F3D2E;">For Landlords</h2><p>List your house in Kisumu, Siaya, Busia, Maseno. KSh 500 verification (DEMO - use 123456).</p></div>', unsafe_allow_html=True)
    if st.button("→ List my house now", type="primary"):
        st.session_state.page="signin"; st.rerun()

elif st.session_state.page == "about":
    st.markdown("""
    <div style="padding:28px 32px;">
    <h2 style="color:#0F3D2E;">About & Safety</h2>
    <p><b>We verify every house in Nyanza.</b></p>
    <ul>
    <li>✅ Towns: Kisumu, Siaya, Busia, Bondo, Ugunja, Ukwala, Maseno</li>
    <li>✅ Never pay before viewing physically</li>
    <li>✅ M-Pesa protected</li>
    <li>✅ WhatsApp: 0740311646</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.page == "signin":
    st.markdown('<div style="padding:20px 32px;"><h2 style="color:#0F3D2E;">Sign in / Register</h2></div>', unsafe_allow_html=True)
    L,R = st.columns(2)
    with L:
        st.subheader("Step 1: M-Pesa (DEMO)")
        if st.button("Request M-Pesa STK Push", type="primary", use_container_width=True):
            st.success("✅ STK sent! Check phone. For DEMO use code 123456")
            st.session_state.stk=True
        if st.session_state.stk:
            code = st.text_input("Enter M-Pesa Code", placeholder="Enter 123456 for demo")
            if st.button("Verify Code", use_container_width=True):
                if code=="123456":
                    st.session_state.verified=True
                    st.balloons()
                    st.success("🎉 Verified! You can now upload.")
                else:
                    st.error("Wrong code - use 123456 for demo")
    with R:
        st.subheader("Step 2: Upload House")
        if st.session_state.verified:
            files = st.file_uploader("Upload 3-5 photos", accept_multiple_files=True, type=["jpg","png","jpeg"])
            if files:
                for f in files: st.image(f, width=150)
                st.success(f"{len(files)} photos uploaded")
                if st.button("Submit - Go Live!", type="primary", use_container_width=True):
                    st.balloons()
                    st.success("🏠 Your house is LIVE! Tenants in Maseno, Kisumu can see it now.")
                    st.session_state.page="home"
        else:
            st.warning("🔒 Complete M-Pesa verification first")
            st.info("DEMO: No real Daraja needed. Use 123456")

elif st.session_state.page == "detail":
    h = st.session_state.get("selected", all_homes[0])
    if st.button("← Back to homes"): st.session_state.page="home"; st.rerun()
    st.image(h["img"], use_container_width=True)
    st.title(f"{h['type']} in {h['area']}")
    st.subheader(h["price"])
    st.write(f"📍 {h['town']}, {h['area']} - Verified ✓")
    st.write("2 rooms, water, electricity, near road, safe area.")
    st.link_button("Contact on WhatsApp", "https://wa.me/254740311646")

st.markdown('<div style="text-align:center; padding:30px; color:#8A9A95; font-size:12px;">© 2026 Home Search Kenya • Towns: Kisumu, Siaya, Busia, Bondo, Ugunja, Ukwala, Maseno</div>', unsafe_allow_html=True)
