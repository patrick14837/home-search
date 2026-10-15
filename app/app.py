import streamlit as st
st.set_page_config(page_title="Home Search Kenya", layout="wide", page_icon="🏠")

if "page" not in st.session_state: st.session_state.page="home"
if "verified" not in st.session_state: st.session_state.verified=False
if "stk" not in st.session_state: st.session_state.stk=False

if "page" in st.query_params:
    st.session_state.page = st.query_params["page"]

def go(p):
    st.session_state.page = p
    st.query_params["page"]=p
    st.rerun()

# GREEN TOP - STEP BACK VERSION THAT SHOWED BUTTONS
st.markdown("""
<style>
[data-testid="stHeader"]{display:none!important;}
footer{display:none!important;}
.block-container{padding-top:0!important; padding-left:0!important; padding-right:0!important; max-width:100%!important;}
.stApp{background:#FFFBF2;}

/* THIS MAKES THE TOP ROW GREEN WITHOUT HIDING BUTTONS */
[data-testid="stHorizontalBlock"] {
    background: #0F3D2E;
    padding: 12px 20px;
}

.hero{height:480px; background:linear-gradient(to right, rgba(0,0,0,0.65), rgba(0,0,0,0.2)), url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1600&q=80'); background-size:cover; background-position:center; padding:50px 32px; display:flex; flex-direction:column; justify-content:center;}
.hero h1{color:white; font-size:54px; font-weight:800; line-height:1.05; margin:0;}
.search-box{background:white; border-radius:16px; padding:18px; margin:-30px 32px 0 32px; box-shadow:0 12px 40px rgba(0,0,0,0.18);}
.form-card{background:white; border-radius:16px; padding:24px; box-shadow:0 8px 30px rgba(0,0,0,0.08); border:1px solid #EFE9E0; margin:24px 32px;}
.safety-card{background:white; border-radius:12px; padding:20px; border-left:4px solid #0F3D2E; margin-bottom:16px;}
</style>
""", unsafe_allow_html=True)

col_logo, c1, c2, c3, c4 = st.columns([2.8, 1.1, 1, 1.3, 0.9], vertical_alignment="center")

with col_logo:
    st.markdown('<div style="color:white; font-weight:900; font-size:20px;">🏠 Home Search <span style="color:#F7E38E;">Kenya</span></div>', unsafe_allow_html=True)

with c1:
    if st.button("Find a Home", type="primary" if st.session_state.page=="home" else "secondary", use_container_width=True, key="bh"):
        go("home")
with c2:
    if st.button("Landlords", type="primary" if st.session_state.page=="landlords" else "secondary", use_container_width=True, key="bl"):
        go("landlords")
with c3:
    if st.button("About & Safety", type="primary" if st.session_state.page=="about" else "secondary", use_container_width=True, key="ba"):
        go("about")
with c4:
    if st.button("Sign in", type="secondary", use_container_width=True, key="bs"):
        go("signin")

if st.session_state.page=="home":
    st.markdown('<div class="hero"><h1>Find a place to<br>call home.</h1><p style="color:#E8EDEB; font-size:15px; max-width:380px; margin-top:14px;">Explore verified rentals in Siaya, Kisumu, Busia, Maseno and nearby towns. Customer Service: 0140311646</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="search-box">', unsafe_allow_html=True)
    sc1,sc2,sc3,sc4 = st.columns([2,2,2,1.3])
    with sc1: st.selectbox("Town or estate", ["Kisumu","Siaya","Busia","Bondo","Ugunja","Ukwala","Maseno"])
    with sc2: st.selectbox("Property type", ["Any home","Bedsitter","1 Bedroom","2 Bedroom","3 Bedroom"])
    with sc3: st.selectbox("Monthly budget", ["Any budget","Below 5k","5k-10k","10k-15k","15k+"])
    with sc4: st.write(""); st.write(""); st.button("Search homes", type="primary", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="padding:24px 32px 0 32px;"><h2 style="color:#0F3D2E;">Homes you might love</h2></div>', unsafe_allow_html=True)
    cols=st.columns(3)
    with cols[0]: st.image("https://images.unsplash.com/photo-1605146769289-440113cc3d00?w=600", use_container_width=True); st.write("**Bedsitter • Maseno** KSh 5,500")
    with cols[1]: st.image("https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=600", use_container_width=True); st.write("**1 Bedroom • Maseno** KSh 8,000")
    with cols[2]: st.image("https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=600", use_container_width=True); st.write("**2 Bedroom • Kisumu** KSh 14,000")

elif st.session_state.page=="landlords":
    st.markdown('<div style="padding:24px 32px 0 32px;"><h1 style="color:#0F3D2E; font-weight:900;">List your house</h1><p>Support: 0140311646 - $10 verification code 123456</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    full_name = st.text_input("Full Name *")
    phone = st.text_input("Phone *")
    town_ll = st.selectbox("Town *", ["Kisumu","Siaya","Busia","Bondo","Ugunja","Ukwala","Maseno"])
    rent = st.number_input("Rent *", value=6500)
    desc = st.text_area("Description *")
    if st.button("Request M-Pesa $10", type="primary"):
        st.session_state.stk=True; st.success("Use 123456")
    if st.session_state.stk:
        code = st.text_input("M-Pesa Code")
        if st.button("Verify"):
            if code=="123456": st.session_state.verified=True; st.success("Verified!")
    if st.session_state.verified:
        if st.button("Submit LIVE 🚀", type="primary"):
            st.balloons(); st.success("LIVE!"); go("home")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page=="about":
    st.markdown('<div style="padding:24px 32px;"><h1 style="color:#0F3D2E;">About - Safety Center 0140311646</h1><p>We cover 7 towns. NEVER pay before viewing. $10 verification.</p></div>', unsafe_allow_html=True)

elif st.session_state.page=="signin":
    st.markdown('<div style="padding:24px 32px;"><h2 style="color:#0F3D2E;">Sign in - 0140311646</h2></div>', unsafe_allow_html=True)
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.text_input("Phone"); st.text_input("Password", type="password")
    if st.button("Sign in", type="primary"): go("home")
    st.markdown('</div>', unsafe_allow_html=True)
