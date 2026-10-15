import streamlit as st
st.set_page_config(page_title="Home Search Kenya", layout="wide", page_icon="🏠")

params = st.query_params
if "page" in params: st.session_state.page = params["page"]
if "page" not in st.session_state: st.session_state.page = "home"
if "verified" not in st.session_state: st.session_state.verified=False

st.markdown("""
<style>
[data-testid="stHeader"]{display:none;}
.block-container{padding:0!important; max-width:100%!important; padding-top:0!important;}
.stApp{background:#FFFBF2;}
.topbar {
  background:#0F3D2E!important;
  height:65px;
  width:100%;
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:0 28px;
}
.topbar.logo {
  color:white!important;
  font-weight:900!important;
  font-size:22px!important;
  display:block!important;
}
.topbar.logo span {
  color:#F7E38E!important;
}
.topbar.nav {
  display:flex!important;
  gap:12px!important;
  align-items:center!important;
}
.topbar.nav a {
  color:#D1DDD9!important;
  font-size:14px!important;
  font-weight:600!important;
  padding:9px 16px!important;
  border-radius:8px!important;
  text-decoration:none!important;
  background:transparent!important;
  display:inline-block!important;
}
.topbar.nav a.active {
  background:#F7E38E!important;
  color:#0F3D2E!important;
  font-weight:800!important;
}
.topbar.nav a.signin {
  border:1px solid #F7E38E!important;
  color:#F7E38E!important;
}
.hero{height:460px; background:linear-gradient(to right, rgba(0,0,0,0.62), rgba(0,0,0,0.2)), url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1600&q=80'); background-size:cover; background-position:center; padding:40px 32px; display:flex; flex-direction:column; justify-content:center;}
.hero h1{color:white; font-size:52px; font-weight:800; line-height:1.05; margin:0;}
.search-box{background:white; border-radius:16px; padding:16px; margin:-32px 32px 0 32px; box-shadow:0 12px 40px rgba(0,0,0,0.18);}
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
    st.markdown(f'<div style="padding:24px 32px 0 32px;"><h2 style="color:#0F3D2E;">Homes you might love</h2><p>{len(filt)} homes in {town}</p></div>', unsafe_allow_html=True)
    cols=st.columns(3)
    for i,h in enumerate(filt):
        with cols[i%3]:
            st.image(h["img"], use_container_width=True)
            st.write(f'**{h["type"]} • {h["town"]}** {h["price"]} {h["area"]}')
    if go: st.balloons(); st.success(f"Found {len(filt)} in {town}!")

elif st.session_state.page=="landlords":
    st.markdown('<div style="padding:28px 32px;"><h2 style="color:#0F3D2E;">For Landlords</h2><p>Kisumu, Siaya, Busia, Maseno - KSh 500 demo</p></div>', unsafe_allow_html=True)
elif st.session_state.page=="about":
    st.markdown('<div style="padding:28px 32px;"><h2>About & Safety</h2><p>Towns: Kisumu, Siaya, Busia, Maseno, Bondo, Ugunja, Ukwala<br>WhatsApp 0740311646</p></div>', unsafe_allow_html=True)
elif st.session_state.page=="signin":
    st.write("## Sign in - Use 123456 for demo")
    if st.button("Request STK", type="primary"): st.success("Use 123456"); st.session_state.verified=True
elif st.session_state.page=="detail":
    h=st.session_state.get("selected", homes[0])
    if st.button("Back"): st.query_params["page"]="home"; st.rerun()
    st.image(h["img"], use_container_width=True)

st.markdown('<div style="text-align:center; padding:20px; color:#8A9A95;">© 2026 Home Search Kenya • Maseno added</div>', unsafe_allow_html=True)
