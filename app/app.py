import streamlit as st
st.set_page_config(page_title="Home Search Kenya", layout="wide", page_icon="🏠")

# Get page from URL
params = st.query_params
page = params.get("page", "home")
if "page" not in st.session_state: st.session_state.page = page
else:
    if "page" in params:
        st.session_state.page = params["page"]

if "verified" not in st.session_state: st.session_state.verified=False
if "stk" not in st.session_state: st.session_state.stk=False

st.markdown("""
<style>
[data-testid="stHeader"]{display:none;}
.block-container{padding:0!important; max-width:100%!important; padding-top:0!important;}
.stApp{background:#FFFBF2;}
a{ text-decoration:none!important; }
.topbar{
  background:#0F3D2E;
  height:62px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:0 32px;
  position:sticky;
  top:0;
  z-index:100;
}
.topbar.logo{color:white; font-weight:800; font-size:20px;}
.topbar.logo span{color:#F7E38E;}
.topbar.nav{display:flex; gap:18px; align-items:center;}
.topbar.nav a{color:#CBD5D1; font-size:13px; font-weight:600; padding:8px 14px; border-radius:8px;}
.topbar.nav a:hover{color:white; background:rgba(255,255,255,0.15);}
.topbar.nav a.active{background:#F7E38E; color:#0F3D2E; font-weight:800;}
.hero{height:460px; background:linear-gradient(to right, rgba(0,0,0,0.62) 0%, rgba(0,0,0,0.2) 60%), url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1600&q=80'); background-size:cover; background-position:center; padding:40px 32px; display:flex; flex-direction:column; justify-content:center;}
.hero h1{color:white; font-size:52px; font-weight:800; line-height:1.05; margin:0;}
.search-box{background:white; border-radius:16px; padding:16px; margin:-32px 32px 0 32px; box-shadow:0 12px 40px rgba(0,0,0,0.18); position:relative; z-index:10;}
.card{border-radius:12px; border:1px solid #F0EDE8; background:white; overflow:hidden;}
</style>
""", unsafe_allow_html=True)

# ACTIVE CLASS
def active(p): return "active" if st.session_state.page==p else ""

# TOP BAR - PURE HTML - WILL ALWAYS BE DARK GREEN - NO WHITE!
st.markdown(f"""
<div class="topbar">
  <div class="logo">🏠 Home Search <span>Kenya</span></div>
  <div class="nav">
    <a href="?page=home" class="{active('home')}">Find a Home</a>
    <a href="?page=landlords" class="{active('landlords')}">Landlords</a>
    <a href="?page=about" class="{active('about')}">About & Safety</a>
    <a href="?page=signin" class="{active('signin')}" style="border:1px solid #F7E38E; color:#F7E38E;">Sign in</a>
  </div>
</div>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
  <h1>Find a place to<br>call home.</h1>
  <p style="color:#E8EDEB; font-size:15px; max-width:360px; margin-top:12px;">Explore verified rentals in Siaya, Kisumu, Busia, Maseno and nearby towns.</p>
</div>
""", unsafe_allow_html=True)

# SEARCH - NO EMOJIS - WITH MASENO
st.markdown('<div class="search-box">', unsafe_allow_html=True)
c1,c2,c3,c4 = st.columns([2,2,2,1.3])
with c1: town=st.selectbox("Town or estate", ["Kisumu","Siaya","Busia","Bondo","Ugunja","Ukwala","Maseno"])
with c2: ptype=st.selectbox("Property type", ["Any home","Bedsitter","1 Bedroom","2 Bedroom","3 Bedroom"])
with c3: budget=st.selectbox("Monthly budget", ["Any budget","Below 5k","5k-10k","10k-15k","15k+"])
with c4:
    st.write(""); st.write("")
    go=st.button("Search homes", type="primary", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Data
homes=[
    {"town":"Kisumu","type":"Bedsitter","price":"KSh 6,500/mo","n":6500,"area":"Nyalenda","img":"https://images.unsplash.com/photo-1605146769289-440113cc3d00?w=600"},
    {"town":"Siaya","type":"1 Bedroom","price":"KSh 9,000/mo","n":9000,"area":"Siaya Town","img":"https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=600"},
    {"town":"Busia","type":"2 Bedroom","price":"KSh 14,000/mo","n":14000,"area":"Busia Town","img":"https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=600"},
    {"town":"Maseno","type":"Bedsitter","price":"KSh 5,500/mo","n":5500,"area":"Maseno University","img":"https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=600"},
    {"town":"Maseno","type":"1 Bedroom","price":"KSh 8,000/mo","n":8000,"area":"Maseno Town","img":"https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=600"},
    {"town":"Kisumu","type":"2 Bedroom","price":"KSh 18,000/mo","n":18000,"area":"Milimani","img":"https://images.unsplash.com/photo-1600585154526-990dced4db0d?w=600"},
]

if st.session_state.page=="home":
    filt=homes
    if go:
        filt=[h for h in homes if h["town"]==town]
        if ptype!="Any home": filt=[h for h in filt if h["type"]==ptype]
    if budget=="Below 5k": filt=[h for h in filt if h["n"]<5000]
    if budget=="5k-10k": filt=[h for h in filt if 5000<=h["n"]<=10000]
    if budget=="10k-15k": filt=[h for h in filt if 10000<=h["n"]<=15000]
    if budget=="15k+": filt=[h for h in filt if h["n"]>=15000]

    st.markdown(f'<div style="padding:24px 32px 0 32px;"><h2 style="color:#0F3D2E; font-weight:800;">Homes you might love</h2><p style="color:#6B7A75; font-size:13px;">{len(filt)} homes in {town} - Maseno included</p></div>', unsafe_allow_html=True)
    cols=st.columns(3)
    for i,h in enumerate(filt):
        with cols[i%3]:
            st.markdown(f'<div class="card"><div style="height:160px; background:url({h["img"]}); background-size:cover;"></div><div style="padding:12px;"><div style="font-size:11px; color:#5B6E69;">{h["type"]} • {h["town"]}</div><div style="font-weight:800; color:#0F3D2E;">{h["price"]}</div><div style="font-size:11px; color:#8A9A95;">{h["area"]}</div></div></div>', unsafe_allow_html=True)
            if st.button(f"View {h['area']}", key=f"v{i}", use_container_width=True):
                st.session_state.selected=h; st.session_state.page="detail"; st.query_params["page"]="detail"; st.rerun()
    if go: st.balloons(); st.success(f"Found {len(filt)} homes in {town}!")

elif st.session_state.page=="landlords":
    st.markdown('<div style="padding:28px 32px;"><h2 style="color:#0F3D2E;">For Landlords</h2><p>List in Kisumu, Siaya, Busia, Maseno, Bondo, Ugunja, Ukwala. KSh 500 (DEMO 123456)</p><br><a href="?page=signin"><button style="background:#0F3D2E; color:white; padding:10px 20px; border-radius:8px; border:none;">List my house →</button></a></div>', unsafe_allow_html=True)
elif st.session_state.page=="about":
    st.markdown('<div style="padding:28px 32px;"><h2 style="color:#0F3D2E;">About & Safety</h2><p>✅ Towns: Kisumu, Siaya, Busia, Bondo, Ugunja, Ukwala, Maseno<br>✅ Verify before paying<br>✅ WhatsApp: 0740311646</p></div>', unsafe_allow_html=True)
elif st.session_state.page=="signin":
    st.markdown('<div style="padding:28px 32px;"><h2>Sign in / Register</h2></div>', unsafe_allow_html=True)
    L,R=st.columns(2)
    with L:
        if st.button("Request M-Pesa STK", type="primary", use_container_width=True):
            st.success("Use 123456 for demo"); st.session_state.stk=True
        if st.session_state.stk:
            code=st.text_input("Enter code")
            if st.button("Verify"):
                if code=="123456": st.session_state.verified=True; st.balloons(); st.success("Verified!")
    with R:
        if st.session_state.verified:
            f=st.file_uploader("Upload photos", accept_multiple_files=True)
            if f: st.success(f"{len(f)} uploaded"); st.balloons()
elif st.session_state.page=="detail":
    h=st.session_state.get("selected", homes[0])
    st.markdown(f'<div style="padding:20px 32px;"><a href="?page=home">← Back to homes</a><br><br><img src="{h["img"]}" style="width:100%; border-radius:12px; max-height:400px; object-fit:cover;"><h1>{h["type"]} in {h["area"]}</h1><h3>{h["price"]}</h3><p>📍 {h["town"]}, {h["area"]}</p></div>', unsafe_allow_html=True)
    st.link_button("Contact on WhatsApp", "https://wa.me/254740311646")

st.markdown('<div style="text-align:center; padding:20px; color:#8A9A95; font-size:12px;">© 2026 Home Search Kenya • Maseno added • No emojis</div>', unsafe_allow_html=True)
