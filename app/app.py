import streamlit as st
st.set_page_config(page_title="Home Search Kenya", layout="wide", page_icon="🏠")

if "page" not in st.session_state: st.session_state.page="home"
if "verified" not in st.session_state: st.session_state.verified=False
if "stk" not in st.session_state: st.session_state.stk=False

params = st.query_params
if "page" in params:
    st.session_state.page = params["page"]

def go(p):
    st.session_state.page = p
    st.query_params["page"]=p
    st.rerun()

st.markdown("""
<style>
[data-testid="stHeader"]{display:none!important;}
footer{display:none!important;}
.block-container{padding-top:0!important; padding-left:0!important; padding-right:0!important; max-width:100%!important;}
.stApp{background:#FFFBF2;}
#top-nav {background:#0F3D2E; padding:12px 24px; margin:0; width:100%;}
div[data-testid="stHorizontalBlock"]{align-items:center;}
.hero{height:480px; background:linear-gradient(to right, rgba(0,0,0,0.65), rgba(0,0,0,0.2)), url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1600&q=80'); background-size:cover; background-position:center; padding:50px 32px; display:flex; flex-direction:column; justify-content:center;}
.hero h1{color:white; font-size:54px; font-weight:800; line-height:1.05; margin:0;}
.search-box{background:white; border-radius:16px; padding:18px; margin:-30px 32px 0 32px; box-shadow:0 12px 40px rgba(0,0,0,0.18);}
.form-card{background:white; border-radius:16px; padding:24px; box-shadow:0 8px 30px rgba(0,0,0,0.08); border:1px solid #EFE9E0; margin:24px 32px;}
.safety-card{background:white; border-radius:12px; padding:20px; border-left:4px solid #0F3D2E; margin-bottom:16px;}
</style>
""", unsafe_allow_html=True)

# === REAL CLICKABLE TOP BAR - STREAMLIT BUTTONS ONLY ===
st.markdown('<div id="top-nav">', unsafe_allow_html=True)
col_logo, c1, c2, c3, c4 = st.columns([2.8, 1.1, 1, 1.3, 0.9], vertical_alignment="center")

with col_logo:
    st.markdown('<div style="color:white; font-weight:900; font-size:20px;">🏠 Home Search <span style="color:#F7E38E;">Kenya</span></div>', unsafe_allow_html=True)

with c1:
    st.button("Find a Home", type="primary" if st.session_state.page=="home" else "secondary", use_container_width=True, key="b_home", on_click=lambda: go("home"))

with c2:
    st.button("Landlords", type="primary" if st.session_state.page=="landlords" else "secondary", use_container_width=True, key="b_land", on_click=lambda: go("landlords"))

with c3:
    st.button("About & Safety", type="primary" if st.session_state.page=="about" else "secondary", use_container_width=True, key="b_about", on_click=lambda: go("about"))

with c4:
    st.button("Sign in", type="secondary", use_container_width=True, key="b_sign", on_click=lambda: go("signin"))

st.markdown('</div>', unsafe_allow_html=True)
# === END TOP BAR ===

if st.session_state.page=="home":
    st.markdown('<div class="hero"><h1>Find a place to<br>call home.</h1><p style="color:#E8EDEB; font-size:15px; max-width:380px; margin-top:14px;">Explore verified rentals in Siaya, Kisumu, Busia, Maseno and nearby towns. Customer Service: 0140311646</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="search-box">', unsafe_allow_html=True)
    sc1,sc2,sc3,sc4 = st.columns([2,2,2,1.3])
    with sc1: town=st.selectbox("Town or estate", ["Kisumu","Siaya","Busia","Bondo","Ugunja","Ukwala","Maseno"])
    with sc2: ptype=st.selectbox("Property type", ["Any home","Bedsitter","1 Bedroom","2 Bedroom","3 Bedroom"])
    with sc3: budget=st.selectbox("Monthly budget", ["Any budget","Below 5k","5k-10k","10k-15k","15k+"])
    with sc4: st.write(""); st.write(""); st.button("Search homes", type="primary", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="padding:24px 32px 0 32px;"><h2 style="color:#0F3D2E;">Homes you might love</h2></div>', unsafe_allow_html=True)
    cols=st.columns(3)
    with cols[0]: st.image("https://images.unsplash.com/photo-1605146769289-440113cc3d00?w=600", use_container_width=True); st.write("**Bedsitter • Maseno** KSh 5,500")
    with cols[1]: st.image("https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=600", use_container_width=True); st.write("**1 Bedroom • Maseno** KSh 8,000")
    with cols[2]: st.image("https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=600", use_container_width=True); st.write("**2 Bedroom • Kisumu** KSh 14,000")

elif st.session_state.page=="landlords":
    st.markdown('<div style="padding:24px 32px 0 32px;"><h1 style="color:#0F3D2E; font-weight:900;">List your house - Get tenants fast</h1><p style="color:#6B7A75;">Towns: Kisumu, Siaya, Busia, Maseno, Bondo, Ugunja, Ukwala. Verification $10 (DEMO 123456) | Support: 0140311646</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        full_name = st.text_input("Full Name *")
        id_number = st.text_input("ID Number *")
        phone = st.text_input("Phone / WhatsApp *", placeholder="0140311646")
    with col2:
        town_ll = st.selectbox("Town *", ["Kisumu","Siaya","Busia","Bondo","Ugunja","Ukwala","Maseno"])
        estate = st.text_input("Estate / Area *", placeholder="Maseno University")
        alt_phone = st.text_input("Alternative Phone")
    st.divider()
    c1,c2,c3 = st.columns(3)
    with c1: p_type = st.selectbox("Property Type *", ["Bedsitter","1 Bedroom","2 Bedroom","3 Bedroom"])
    with c2: rent = st.number_input("Monthly Rent (KSh) *", value=6500, step=500)
    with c3: rooms = st.selectbox("Number of Rooms", ["1","2","3","4+"])
    desc = st.text_area("House Description *")
    photos = st.file_uploader("Upload 3-5 photos *", accept_multiple_files=True, type=["jpg","jpeg","png"])
    st.divider()
    colA, colB = st.columns(2)
    with colA:
        if st.button("Request M-Pesa STK Push - $10", type="primary", use_container_width=True, key="stk1"):
            st.success("STK sent! Enter 123456"); st.session_state.stk=True
        if st.session_state.stk:
            code = st.text_input("Enter M-Pesa Code", key="code1")
            if st.button("Verify Code", key="ver1"):
                if code=="123456": st.session_state.verified=True; st.balloons(); st.success("Verified!")
                else: st.error("Use 123456")
    with colB:
        if st.session_state.verified:
            if st.button("Submit - Make LIVE 🚀", type="primary", use_container_width=True, key="sub1"):
                if full_name and phone: st.balloons(); st.success(f"Thank you {full_name}! LIVE! Support: 0140311646"); go("home")
        else: st.warning("Complete verification first - $10")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page=="about":
    st.markdown('<div style="padding:24px 32px 0 32px;"><h1 style="color:#0F3D2E; font-weight:900; font-size:38px;">About Home Search Kenya</h1><p style="color:#5A6B66;">Kenya trusted rental platform. Customer Service: 0140311646</p></div>', unsafe_allow_html=True)
    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown("""
        <div class="form-card" style="margin:16px 0 16px 32px;">
          <h3 style="color:#0F3D2E;">Who We Are</h3>
          <p style="color:#4A5A55; line-height:1.7;">We cover 7 towns: <b>Kisumu, Siaya, Busia, Maseno, Bondo, Ugunja, Ukwala</b>. Every landlord ID-verified. Fee $10.</p>
          <h3 style="color:#0F3D2E; margin-top:24px;">How It Works</h3>
          <p style="color:#4A5A55; line-height:1.7;">1. Tenants search<br>2. Landlords $10 verification (123456)<br>3. Always view physically before paying.</p>
        </div>
        <div style="padding:0 32px;">
          <h2 style="color:#0F3D2E;">Safety Center - Call 0140311646</h2>
          <div class="safety-card">
            <h4 style="margin:0;">For Tenants - Avoid Scams</h4>
            <ul style="color:#4A5A55; line-height:1.8;">
              <li><b>NEVER pay before viewing</b></li>
              <li>Meet at property, check water, electricity, locks</li>
              <li>Get receipt with ID and signature</li>
              <li>Report to 0140311646</li>
            </ul>
          </div>
          <div class="safety-card" style="border-left-color:#C0392B;">
            <h4 style="margin:0;">Red Flags - Call 0140311646</h4>
            <p style="color:#4A5A55;">Asks money before viewing, no ID, pressure to pay TODAY - we remove in 2hrs.</p>
          </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="form-card" style="margin:16px 32px 16px 0;">
          <h3 style="color:#0F3D2E;">Customer Service</h3>
          <p style="color:#4A5A55; line-height:1.8;">
          <b>Phone:</b> 0140311646<br>
          <b>WhatsApp:</b> 0140311646<br>
          <b>Email:</b> support@homesearch.co.ke<br>
          <b>Location:</b> Maseno Town<br>
          </p>
          <hr>
          <h4 style="color:#0F3D2E;">Verification $10</h4>
          <p style="color:#4A5A55;">DEMO 123456</p>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.page=="signin":
    st.markdown('<div style="padding:24px 32px;"><h2 style="color:#0F3D2E;">Sign in - Support: 0140311646</h2></div>', unsafe_allow_html=True)
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.text_input("Phone")
    st.text_input("Password", type="password")
    if st.button("Sign in", type="primary"): st.success("Signed in!")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="text-align:center; padding:20px; color:#8A9A95; font-size:12px;">© 2026 Home Search Kenya • Customer Service: 0140311646 • $10 verification</div>', unsafe_allow_html=True)
