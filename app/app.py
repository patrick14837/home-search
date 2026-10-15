import streamlit as st
st.set_page_config(page_title="Home Search Kenya", layout="wide", page_icon="🏠")

if "verified" not in st.session_state: st.session_state.verified=False
if "stk" not in st.session_state: st.session_state.stk=False

st.markdown("""
<style>
[data-testid="stHeader"]{display:none;}
.block-container{padding:0!important; max-width:100%!important; padding-top:0!important;}
.stApp{background:#FFFBF2;}
html{scroll-behavior:smooth;}
.topbar {background:#0F3D2E; height:64px; width:100%; display:flex; align-items:center; justify-content:space-between; padding:0 32px; position:sticky; top:0; z-index:999;}
.topbar .logo {color:white!important; font-weight:900; font-size:22px;}
.topbar .logo span {color:#F7E38E!important;}
.topbar .nav {display:flex; gap:14px; align-items:center;}
.topbar .nav a {color:#E0EDE8!important; font-size:14px; font-weight:600; padding:8px 16px; border-radius:8px; text-decoration:none!important;}
.topbar .nav a.active {background:#F7E38E!important; color:#0F3D2E!important; font-weight:800;}
.topbar .nav a.signin {border:1px solid #F7E38E!important; color:#F7E38E!important;}
.hero{height:460px; background:linear-gradient(to right, rgba(0,0,0,0.62), rgba(0,0,0,0.2)), url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1600&q=80'); background-size:cover; background-position:center; padding:40px 32px; display:flex; flex-direction:column; justify-content:center;}
.hero h1{color:white; font-size:52px; font-weight:800; line-height:1.05; margin:0;}
.search-box{background:white; border-radius:16px; padding:16px; margin:-32px 32px 0 32px; box-shadow:0 12px 40px rgba(0,0,0,0.18);}
.form-card{background:white; border-radius:16px; padding:24px; box-shadow:0 8px 30px rgba(0,0,0,0.08); border:1px solid #EFE9E0; margin:24px 32px;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="topbar">
  <div class="logo">Home Search <span>Kenya</span></div>
  <div class="nav">
    <a href="#home" class="active">Find a Home</a>
    <a href="#landlords">Landlords</a>
    <a href="#about">About & Safety</a>
    <a href="#signin" class="signin">Sign in</a>
  </div>
</div>
<div id="home"></div>
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

st.markdown('<div id="landlords"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="padding:28px 32px 0 32px;">
  <h1 style="color:#0F3D2E; font-weight:900;">List your house - Get tenants fast</h1>
  <p style="color:#6B7A75;">Enter your credentials. Towns: Kisumu, Siaya, Busia, Maseno, Bondo, Ugunja, Ukwala. Verification $10 (DEMO code 123456)</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="form-card">', unsafe_allow_html=True)
st.subheader("1. Landlord Credentials")
col1, col2 = st.columns(2)
with col1:
    full_name = st.text_input("Full Name *", placeholder="e.g. John Otieno", key="name")
    id_number = st.text_input("ID Number *", placeholder="e.g. 34567890", key="id")
    phone = st.text_input("Phone Number / WhatsApp *", placeholder="e.g. 0740311646", key="phone")
with col2:
    town_ll = st.selectbox("Town *", ["Kisumu","Siaya","Busia","Bondo","Ugunja","Ukwala","Maseno"], key="townll")
    estate = st.text_input("Estate / Area *", placeholder="e.g. Maseno University, Siaya Town", key="estate")
    alt_phone = st.text_input("Alternative Phone", placeholder="Optional", key="alt")

st.divider()
st.subheader("2. House Details")
c1,c2,c3 = st.columns(3)
with c1: p_type = st.selectbox("Property Type *", ["Bedsitter","1 Bedroom","2 Bedroom","3 Bedroom","Single Room"], key="ptype2")
with c2: rent = st.number_input("Monthly Rent (KSh) *", min_value=1000, max_value=100000, value=6500, step=500, key="rent")
with c3: rooms = st.selectbox("Number of Rooms", ["1","2","3","4+"], key="rooms")
desc = st.text_area("House Description *", placeholder="e.g. 2 rooms, tiled, water 24/7, near Maseno University...", key="desc")

st.divider()
st.subheader("3. Photos & Verification")
photos = st.file_uploader("Upload 3-5 clear photos of house (inside + outside) *", accept_multiple_files=True, type=["jpg","jpeg","png"], key="photos")

st.divider()
colA, colB = st.columns(2)
with colA:
    st.write("**M-Pesa Verification (DEMO)**")
    if st.button("Request M-Pesa STK Push - $10", type="primary", use_container_width=True, key="stk"):
        st.success("✅ STK sent! For DEMO enter 123456")
        st.session_state.stk=True
    if st.session_state.stk:
        code = st.text_input("Enter M-Pesa Code", placeholder="123456 for demo", key="code")
        if st.button("Verify Code", use_container_width=True, key="verify"):
            if code=="123456":
                st.session_state.verified=True
                st.balloons()
                st.success("🎉 Verified!")
            else:
                st.error("Use 123456")
with colB:
    st.write("**Submit Listing**")
    if st.session_state.verified:
        if st.button("Submit - Make My House LIVE 🚀", type="primary", use_container_width=True, key="submit"):
            if full_name and phone and estate and desc:
                st.balloons()
                st.success(f"🏠 Thank you {full_name}! Your {p_type} in {estate}, {town_ll} is LIVE!")
            else:
                st.error("Fill all * fields")
    else:
        st.warning("Complete M-Pesa verification first")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div id="about"></div><div style="padding:28px 32px;"><h2 style="color:#0F3D2E;">About & Safety</h2><p>WhatsApp: 0740311646</p></div>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center; padding:20px; color:#8A9A95;">© 2026 Home Search Kenya • $10 verification • Maseno</div>', unsafe_allow_html=True)
