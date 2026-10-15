import streamlit as st
st.set_page_config(page_title="Home Search Kenya", layout="wide", page_icon="🏠")

if "page" not in st.session_state:
    st.session_state.page="home"
if "verified" not in st.session_state:
    st.session_state.verified=False
if "stk" not in st.session_state:
    st.session_state.stk=False

st.markdown('''
<style>
[data-testid="stHeader"]{display:none;}
.block-container{padding:0 !important; max-width:100% !important;}
.stApp{background:#FFFBF2;}
.header{background:#0F3D2E; height:62px; display:flex; align-items:center; padding:0 32px;}
.hero{height:460px; background:linear-gradient(to right, rgba(0,0,0,0.62), rgba(0,0,0,0.2)), url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1600&q=80'); background-size:cover; background-position:center; padding:40px 32px; display:flex; flex-direction:column; justify-content:center;}
.hero h1{color:white; font-size:52px; font-weight:800; line-height:1.05; margin:0;}
.search-wrapper{background:white; border-radius:16px; padding:16px; margin:-32px 32px 0 32px; box-shadow:0 12px 40px rgba(0,0,0,0.18);}
.card{border-radius:12px; border:1px solid #F0EDE8; background:white; overflow:hidden;}
</style>
<div class="header"><div style="color:white; font-weight:800; font-size:20px;">🏠 Home Search <span style="color:#F7E38E;">Kenya</span></div></div>
<div class="hero"><h1>Find a place to<br>call home.</h1><p style="color:#E8EDEB; max-width:360px; margin-top:12px;">Explore verified rentals in Siaya, Kisumu, Busia and nearby towns.</p></div>
''', unsafe_allow_html=True)

c1,c2,c3,c4,c5=st.columns([3,1,1,1.2,1])
with c2:
    if st.button("Find a Home", use_container_width=True):
        st.session_state.page="home"; st.rerun()
with c3:
    if st.button("Landlords", use_container_width=True):
        st.session_state.page="landlords"; st.rerun()
with c4:
    if st.button("About & Safety", use_container_width=True):
        st.session_state.page="about"; st.rerun()
with c5:
    if st.button("👤 Sign in", use_container_width=True):
        st.session_state.page="signin"; st.rerun()

st.markdown('<div class="search-wrapper">', unsafe_allow_html=True)
a,b,c,d=st.columns([2,2,2,1.3])
with a: town=st.selectbox("📍 Town or estate", ["Kisumu","Siaya","Busia","Bondo","Ugunja","Ukwala"])
with b: ptype=st.selectbox("🏠 Property type", ["Any home","Bedsitter","1 Bedroom","2 Bedroom"])
with c: budget=st.selectbox("💰 Monthly budget", ["Any budget","Below 5k","5k-10k","10k-15k","15k+"])
with d:
    st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
    search=st.button("🔍 Search homes", type="primary", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# DATA
homes=[
    {"town":"Kisumu","type":"Bedsitter","price":"KSh 6,500/mo","n":6500,"area":"Nyalenda","img":"https://images.unsplash.com/photo-1605146769289-440113cc3d00?w=600"},
    {"town":"Siaya","type":"1 Bedroom","price":"KSh 9,000/mo","n":9000,"area":"Siaya Town","img":"https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=600"},
    {"town":"Busia","type":"2 Bedroom","price":"KSh 14,000/mo","n":14000,"area":"Busia Town","img":"https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=600"},
    {"town":"Bondo","type":"Bedsitter","price":"KSh 5,000/mo","n":5000,"area":"Bondo","img":"https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=600"},
    {"town":"Ugunja","type":"1 Bedroom","price":"KSh 8,500/mo","n":8500,"area":"Ugunja","img":"https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?w=600"},
    {"town":"Kisumu","type":"2 Bedroom","price":"KSh 18,000/mo","n":18000,"area":"Milimani","img":"https://images.unsplash.com/photo-1600585154526-990dced4db0d?w=600"},
]

if st.session_state.page=="home":
    filtered=homes
    if town!="Kisumu": filtered=[h for h in filtered if h["town"]==town]
    if ptype!="Any home": filtered=[h for h in filtered if h["type"]==ptype]
    if budget=="Below 5k": filtered=[h for h in filtered if h["n"]<5000]
    if budget=="5k-10k": filtered=[h for h in filtered if 5000<=h["n"]<=10000]
    if budget=="10k-15k": filtered=[h for h in filtered if 10000<=h["n"]<=15000]
    if budget=="15k+": filtered=[h for h in filtered if h["n"]>=15000]
    
    st.markdown(f'<div style="padding:20px 32px;"><h2 style="color:#0F3D2E;">Homes you might love</h2><p style="color:#6B7A75; font-size:13px;">Found {len(filtered)} homes</p></div>', unsafe_allow_html=True)
    cols=st.columns(3)
    for i,h in enumerate(filtered):
        with cols[i%3]:
            st.image(h["img"], use_container_width=True)
            st.write(f'**{h["type"]} • {h["town"]}**\n{h["price"]}\n📍 {h["area"]}')
            if st.button(f'View {h["area"]}', key=f'v{i}', use_container_width=True):
                st.toast(f'Opening {h["area"]} - {h["price"]}')
                st.session_state.selected=h; st.session_state.page="detail"; st.rerun()
    if search: st.balloons(); st.success(f'Searched {ptype} in {town} - {len(filtered)} results!')

elif st.session_state.page=="landlords":
    st.markdown('<div style="padding:28px 32px;"><h2>For Landlords</h2><p>List your house - KSh 500 verification (DEMO mode, no real M-Pesa needed).</p></div>', unsafe_allow_html=True)
    if st.button("List my house now →"): st.session_state.page="signin"; st.rerun()

elif st.session_state.page=="about":
    st.markdown('<div style="padding:28px 32px;"><h2>About & Safety</h2><p>✅ We verify landlords in Siaya, Kisumu, Busia<br>✅ Never pay before viewing<br>✅ M-Pesa protected<br>✅ WhatsApp: 0740311646</p></div>', unsafe_allow_html=True)

elif st.session_state.page=="signin":
    st.markdown('<div style="padding:20px 32px;"><h2>Sign in / Register</h2></div>', unsafe_allow_html=True)
    l,r=st.columns(2)
    with l:
        st.subheader("Step 1: M-Pesa (DEMO - use 123456)")
        if st.button("Request M-Pesa STK", type="primary"):
            st.success("STK sent! Use code 123456"); st.session_state.stk=True
        if st.session_state.stk:
            code=st.text_input("Enter Code")
            if st.button("Verify"):
                if code=="123456": st.session_state.verified=True; st.success("Verified!"); st.balloons()
                else: st.error("Use 123456")
    with r:
        st.subheader("Step 2: Upload House")
        if st.session_state.verified:
            files=st.file_uploader("Photos", accept_multiple_files=True)
            if files:
                for f in files: st.image(f, width=150)
                if st.button("Submit Listing", type="primary"): st.balloons(); st.success("Listing LIVE!")
        else: st.warning("Verify M-Pesa first")
