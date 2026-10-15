import streamlit as st
st.set_page_config(page_title="Home Search Kenya", layout="wide", page_icon="🏠")

if "page" not in st.session_state: st.session_state.page="home"
if "verified" not in st.session_state: st.session_state.verified=False
if "stk" not in st.session_state: st.session_state.stk=False

st.markdown("""
<style>
[data-testid="stHeader"]{display:none;}
.block-container{padding:0!important; max-width:100%!important; padding-top:0!important;}
.stApp{background:#FFFBF2;}

/* FORCE TOP BAR DARK GREEN */
div[data-testid="stVerticalBlock"] > div:nth-child(1) > div[data-testid="stHorizontalBlock"]{
    background:#0F3D2E!important;
    padding:10px 20px 14px 20px!important;
    margin:0!important;
    width:100%!important;
    max-width:100%!important;
}
div[data-testid="stVerticalBlock"] > div:nth-child(1) button{
    color:white!important;
    border:1px solid rgba(255,255,255,0.3)!important;
    background:transparent!important;
}
div[data-testid="stVerticalBlock"] > div:nth-child(1) button[kind="primary"]{
    background:#F7E38E!important;
    color:#0F3D2E!important;
    border:none!important;
    font-weight:800!important;
}

.hero{height:430px; background:linear-gradient(to right, rgba(0,0,0,0.62), rgba(0,0,0,0.15)), url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1600&q=80'); background-size:cover; background-position:center; padding:40px 32px; display:flex; flex-direction:column; justify-content:center; margin-top:0!important;}
.hero h1{color:white; font-size:54px; font-weight:800; line-height:1.05; margin:0;}
.search-box{background:white; border-radius:16px; padding:16px; margin:-28px 32px 0 32px; box-shadow:0 12px 40px rgba(0,0,0,0.18);}
</style>
""", unsafe_allow_html=True)

# TOP BAR - DARK GREEN WITH BUTTONS INSIDE
t1, t2, t3, t4, t5 = st.columns([2.5, 1, 0.9, 1.3, 1])
with t1:
    st.markdown('<div style="color:white; font-weight:800; font-size:21px; padding-top:6px;">🏠 Home Search <span style="color:#F7E38E;">Kenya</span></div>', unsafe_allow_html=True)
with t2:
    if st.button("Find a Home", key="top1", use_container_width=True, type="primary" if st.session_state.page=="home" else "secondary"):
        st.session_state.page="home"; st.rerun()
with t3:
    if st.button("Landlords", key="top2", use_container_width=True):
        st.session_state.page="landlords"; st.rerun()
with t4:
    if st.button("About & Safety", key="top3", use_container_width=True):
        st.session_state.page="about"; st.rerun()
with t5:
    if st.button("Sign in", key="top4", use_container_width=True):
        st.session_state.page="signin"; st.rerun()

# Hero
st.markdown("""
<div class="hero">
<h1>Find a place to<br>call home.</h1>
<p style="color:#E8EDEB; font-size:15px; max-width:360px; margin-top:12px;">Explore verified rentals in Siaya, Kisumu, Busia, Maseno and nearby towns.</p>
</div>
""", unsafe_allow_html=True)

# SEARCH - NO EMOJIS NOW
st.markdown('<div class="search-box">', unsafe_allow_html=True)
c1,c2,c3,c4 = st.columns([2,2,2,1.3])
with c1:
    town=st.selectbox("Town or estate", ["Kisumu","Siaya","Busia","Bondo","Ugunja","Ukwala","Maseno"])
with c2:
    ptype=st.selectbox("Property type", ["Any home","Bedsitter","1 Bedroom","2 Bedroom","3 Bedroom"])
with c3:
    budget=st.selectbox("Monthly budget", ["Any budget","Below 5k","5k-10k","10k-15k","15k+"])
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

    st.markdown(f'<div style="padding:20px 32px;"><h2 style="color:#0F3D2E;">Homes you might love</h2><p style="color:#6B7A75;">{len(filt)} homes - Maseno included</p></div>', unsafe_allow_html=True)
    cols=st.columns(3)
    for i,h in enumerate(filt):
        with cols[i%3]:
            st.image(h["img"], use_container_width=True)
            st.write(f'**{h["type"]} • {h["town"]}**\n{h["price"]}\n{h["area"]}')
            if st.button(f'View {h["area"]}', key=f'v{i}', use_container_width=True):
                st.session_state.selected=h; st.session_state.page="detail"; st.rerun()
    if go: st.balloons(); st.success(f"Found {len(filt)} homes in {town}!")

elif st.session_state.page=="landlords":
    st.markdown('<div style="padding:28px 32px;"><h2 style="color:#0F3D2E;">For Landlords</h2><p>Kisumu, Siaya, Busia, Maseno - KSh 500 (DEMO 123456)</p></div>', unsafe_allow_html=True)
elif st.session_state.page=="about":
    st.markdown('<div style="padding:28px 32px;"><h2>About</h2><p>Towns: Kisumu, Siaya, Busia, Bondo, Ugunja, Ukwala, Maseno<br>WhatsApp: 0740311646</p></div>', unsafe_allow_html=True)
elif st.session_state.page=="signin":
    st.write("## Sign in");
    if st.button("Request STK", type="primary"):
        st.success("Use 123456"); st.session_state.stk=True
    if st.session_state.stk:
        cd=st.text_input("Code")
        if st.button("Verify") and cd=="123456": st.session_state.verified=True; st.success("Verified!")
elif st.session_state.page=="detail":
    h=st.session_state.get("selected", homes[0])
    if st.button("Back"): st.session_state.page="home"; st.rerun()
    st.image(h["img"], use_container_width=True)
    st.title(f'{h["type"]} in {h["area"]}')

st.markdown('<div style="text-align:center; padding:20px; color:#8A9A95; font-size:12px;">© 2026 Home Search Kenya • Maseno added</div>', unsafe_allow_html=True)
