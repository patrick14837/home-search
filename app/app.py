import streamlit as st
st.set_page_config(page_title="Home Search Kenya", layout="wide", page_icon="🏠")

if "page" in st.query_params:
    st.session_state.page = st.query_params["page"]
if "page" not in st.session_state:
    st.session_state.page = "home"
if "verified" not in st.session_state: st.session_state.verified=False
if "stk" not in st.session_state: st.session_state.stk=False

st.markdown("""
<style>
[data-testid="stHeader"]{display:none;}
.block-container{padding:0!important; max-width:100%!important; padding-top:0!important;}
.stApp{background:#FFFBF2;}
div.topbar{background:#0F3D2E; height:64px; width:100%; display:flex; align-items:center; justify-content:space-between; padding:0 32px; box-sizing:border-box;}
div.topbar.logo{color:#FFFFFF!important; font-weight:900; font-size:21px;}
div.topbar.logo span{color:#F7E38E!important;}
div.topbar.nav{display:flex; gap:14px; align-items:center;}
div.topbar.nav a{color:#E0EDE8!important; font-size:14px; font-weight:600; padding:8px 16px; border-radius:8px; text-decoration:none!important;}
div.topbar.nav a.active{background:#F7E38E!important; color:#0F3D2E!important; font-weight:800;}
div.topbar.nav a.signin{border:1px solid #F7E38E; color:#F7E38E!important;}
.hero{height:460px; background:linear-gradient(to right, rgba(0,0,0,0.62), rgba(0,0,0,0.2)), url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1600&q=80'); background-size:cover; background-position:center; padding:40px 32px; display:flex; flex-direction:column; justify-content:center;}
.hero h1{color:white; font-size:52px; font-weight:800; line-height:1.05; margin:0;}
.search-box{background:white; border-radius:16px; padding:16px; margin:-32px 32px 0 32px; box-shadow:0 12px 40px rgba(0,0,0,0.18);}
.form-card{background:white; border-radius:16px; padding:24px; box-shadow:0 8px 30px rgba(0,0,0,0.08); border:1px solid #EFE9E0; margin:24px 32px;}
</style>
""", unsafe_allow_html=True)

def active(p): return "active" if st.session_state.page==p else ""

st.markdown(f"""
<div class="topbar">
  <div class="logo">Home Search <span>Kenya</span></div>
  <div class="nav">
    <a href="?page=home" class="{active('home')}">Find a Home</a>
    <a href="?page=landlords" class="{active('landlords')}">Landlords</a>
    <a href="?page=about" class="{active('about')}">About & Safety</a>
    <a href="?page=signin" class="signin">Sign in</a>
  </div>
</div>
""", unsafe_allow_html=True)

# HERO ONLY ON HOME PAGE
if st.session_state.page=="home":
    st.markdown("""
    <div class="hero">
      <h1>Find a place to<br>call home.</h1>
      <p style="color:#E8EDEB; font-size:15px; max-width:360px; margin-top:12px;">Explore verified rentals in Siaya, Kisumu, Busia, Maseno and nearby towns.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="search-box">', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns([2,2,2,1.3])
    with c1: town=st.selectbox("Town or estate", ["Kisumu","Siaya","Busia","Bondo","Ugunja","Ukwala","Maseno"])
    with c2: ptype=st.selectbox("Property type", ["Any home","Bedsitter","1 Bedroom","2 Bedroom","3 Bedroom"])
    with c3: budget=st.selectbox("Monthly budget", ["Any budget","Below 5k","5k-10k","10k-15k","15k+"])
    with c4:
        st.write(""); st.write("")
        go=st.button("Search homes", type="primary", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    homes=[
        {"town":"Kisumu","type":"Bedsitter","price":"KSh 6,500/mo","area":"Nyalenda","img":"https://images.unsplash.com/photo-1605146769289-440113cc3d00?w=600"},
        {"town":"Maseno","type":"Bedsitter","price":"KSh 5,500/mo","area":"Maseno University","img":"https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=600"},
        {"town":"Maseno","type":"1 Bedroom","price":"KSh 8,000/mo","area":"Maseno Town","img":"https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=600"},
    ]
    st.markdown('<div style="padding:24px 32px 0 32px;"><h2 style="color:#0F3D2E;">Homes you might love</h2></div>', unsafe_allow_html=True)
    cols=st.columns(3)
    for i,h in enumerate(homes):
        with cols[i%3]:
            st.image(h["img"], use_container_width=True)
            st.write(f'**{h["type"]} • {h["town"]}** {h["price"]} {h["area"]}')

# ===== LANDLORDS CREDENTIALS FORM =====
elif st.session_state.page=="landlords":
    st.markdown("""
    <div style="padding:28px 32px 0 32px;">
      <h1 style="color:#0F3D2E; font-weight:900;">List your house - Get tenants fast</h1>
      <p style="color:#6B7A75;">Enter your credentials. Towns: Kisumu, Siaya, Busia, Maseno, Bondo, Ugunja, Ukwala. Verification KSh 500 (DEMO code 123456)</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.subheader("1. Landlord Credentials")
    col1, col2 = st.columns(2)
    with col1:
        full_name = st.text_input("Full Name *", placeholder="e.g. John Otieno")
        id_number = st.text_input("ID Number *", placeholder="e.g. 34567890")
        phone = st.text_input("Phone Number / WhatsApp *", placeholder="e.g. 0740311646")
    with col2:
        town_ll = st.selectbox("Town *", ["Kisumu","Siaya","Busia","Bondo","Ugunja","Ukwala","Maseno"])
        estate = st.text_input("Estate / Area *", placeholder="e.g. Maseno University, Siaya Town")
        alt_phone = st.text_input("Alternative Phone", placeholder="Optional")

    st.divider()
    st.subheader("2. House Details")
    c1,c2,c3 = st.columns(3)
    with c1: p_type = st.selectbox("Property Type *", ["Bedsitter","1 Bedroom","2 Bedroom","3 Bedroom","Single Room","Maisonette"])
    with c2: rent = st.number_input("Monthly Rent (KSh) *", min_value=1000, max_value=100000, value=6500, step=500)
    with c3: rooms = st.selectbox("Number of Rooms", ["1","2","3","4+"])

    desc = st.text_area("House Description *", placeholder="e.g. 2 rooms, tiled, water 24/7, near Maseno University gate, secure, parking...")

    st.divider()
    st.subheader("3. Photos & Verification")
    photos = st.file_uploader("Upload 3-5 clear photos of house (inside + outside) *", accept_multiple_files=True, type=["jpg","jpeg","png"])
    if photos:
        cols = st.columns(len(photos))
        for i,f in enumerate(photos):
            with cols[i]: st.image(f, use_container_width=True)

    st.divider()
    colA, colB = st.columns(2)
    with colA:
        st.write("**M-Pesa Verification (DEMO)**")
        if st.button("Request M-Pesa STK Push - KSh 500", type="primary", use_container_width=True):
            st.success("✅ STK sent to your phone! Check M-Pesa. For DEMO enter code 123456")
            st.session_state.stk=True
        if st.session_state.stk:
            code = st.text_input("Enter M-Pesa Code", placeholder="Enter 123456 for demo")
            if st.button("Verify Code", use_container_width=True):
                if code=="123456":
                    st.session_state.verified=True
                    st.balloons()
                    st.success("🎉 Verified! Your credentials are confirmed.")
                else:
                    st.error("Wrong code - use 123456 for demo")
    with colB:
        st.write("**Submit Listing**")
        if st.session_state.verified:
            if st.button("Submit - Make My House LIVE 🚀", type="primary", use_container_width=True):
                if full_name and phone and estate and desc:
                    st.balloons()
                    st.success(f"🏠 Thank you {full_name}! Your {p_type} in {estate}, {town_ll} is now LIVE! Tenants can contact you on {phone}. WhatsApp: 0740311646 will call you.")
                    st.query_params["page"]="home"
                else:
                    st.error("Please fill all * fields")
        else:
            st.warning("🔒 Complete M-Pesa verification first to submit")
            st.info("DEMO: No real M-Pesa needed. Click STK then enter 123456")

    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page=="about":
    st.markdown('<div style="padding:28px 32px;"><h2 style="color:#0F3D2E;">About & Safety</h2><p>Towns: Kisumu, Siaya, Busia, Maseno, Bondo, Ugunja, Ukwala<br>Never pay before viewing<br>WhatsApp: 0740311646</p></div>', unsafe_allow_html=True)

elif st.session_state.page=="signin":
    st.markdown('<div style="padding:28px 32px;"><h2>Sign in</h2><p>Landlords sign in to manage houses</p></div>', unsafe_allow_html=True)
    st.text_input("Phone or ID")
    st.text_input("Password", type="password")
    if st.button("Sign in", type="primary"):
        st.success("Signed in! Go to Landlords to list house")
        st.query_params["page"]="landlords"

st.markdown('<div style="text-align:center; padding:20px; color:#8A9A95; font-size:12px;">© 2026 Home Search Kenya • Maseno added</div>', unsafe_allow_html=True)
