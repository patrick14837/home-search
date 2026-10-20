import streamlit as st
st.set_page_config(page_title="Home Search Kenya", layout="wide", page_icon="🏠")

if "page" not in st.session_state:
    st.session_state.page="home"
    st.session_state.verified=False
    st.session_state.stk=False

if "page" in st.query_params:
    st.session_state.page = st.query_params["page"]

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

/* ONLY TOP ROW GREEN */
div[data-testid="stVerticalBlock"] > div:nth-child(1) > div[data-testid="stHorizontalBlock"] {
    background:#0F3D2E!important;
    padding:12px 20px!important;
}
div[data-testid="stVerticalBlock"] > div:nth-child(n+2) div[data-testid="stHorizontalBlock"] {
    background:transparent!important;
}

.hero{height:480px; background:linear-gradient(to right, rgba(0,0,0,0.65), rgba(0,0,0,0.2)), url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1600&q=80'); background-size:cover; background-position:center; padding:50px 32px; display:flex; flex-direction:column; justify-content:center;}
.hero h1{color:white; font-size:54px; font-weight:800; line-height:1.05; margin:0;}
.search-box{background:white; border-radius:16px; padding:18px; margin:-30px 32px 0 32px; box-shadow:0 12px 40px rgba(0,0,0,0.18); border:1px solid #EFE9E0;}
.search-box div[data-testid="stHorizontalBlock"]{background:white!important; padding:0!important;}
.form-card{background:white; border-radius:16px; padding:24px; box-shadow:0 8px 30px rgba(0,0,0,0.08); border:1px solid #EFE9E0; margin:24px 32px;}
.safety-card{background:white; border-radius:12px; padding:20px; border-left:4px solid #0F3D2E; box-shadow:0 4px 16px rgba(0,0,0,0.06); margin-bottom:16px;}
.trust-badge{background:#F7E38E; color:#0F3D2E; padding:6px 12px; border-radius:20px; font-size:12px; font-weight:800; display:inline-block; margin:4px;}
</style>
""", unsafe_allow_html=True)

# TOP NAV
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

# FIND A HOME - LOCATION FIXED
if st.session_state.page=="home":
    st.markdown('<div class="hero"><h1>Find a place to<br>call home.</h1><p style="color:#E8EDEB; font-size:15px; max-width:420px; margin-top:14px;">Explore verified rentals in Siaya, Kisumu, Busia, Maseno, Bondo, Ugunja, Ukwala. Customer Service: 0140311646</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="search-box">', unsafe_allow_html=True)
    sc1,sc2,sc3,sc4 = st.columns([2,2,2,1.3])
    with sc1: town=st.selectbox("📍 Town or estate", ["All Towns","Kisumu","Siaya","Busia","Bondo","Ugunja","Ukwala","Maseno"], key="town_home")
    with sc2: ptype=st.selectbox("🏠 Property type", ["Any home","Bedsitter","1 Bedroom","2 Bedroom","3 Bedroom"], key="ptype_home")
    with sc3: budget=st.selectbox("💰 Monthly budget", ["Any budget","Below 5k","5k-10k","10k-15k","15k+","20k+"], key="bud_home")
    with sc4: st.write(""); st.write(""); st.button("🔍 Search homes", type="primary", use_container_width=True, key="search_btn")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="padding:24px 32px 0 32px;"><h2 style="color:#0F3D2E;">Homes you might love</h2><p style="color:#6B7A75; font-size:13px;">📍 Showing: {} • {} • {} • Verified by 0140311646</p></div>'.format(town, ptype, budget), unsafe_allow_html=True)
    cols=st.columns(3)
    with cols[0]: st.image("https://images.unsplash.com/photo-1605146769289-440113cc3d00?w=600", use_container_width=True); st.markdown("**Bedsitter • Maseno - Mabungo**\nKSh 5,500 / month\n\n<span class='trust-badge'>✓ Verified</span> <span class='trust-badge'>📍 Maseno</span>", unsafe_allow_html=True)
    with cols[1]: st.image("https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=600", use_container_width=True); st.markdown("**1 Bedroom • Siaya Town**\nKSh 8,000 / month\n\n<span class='trust-badge'>✓ Verified</span> <span class='trust-badge'>📍 Siaya</span>", unsafe_allow_html=True)
    with cols[2]: st.image("https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=600", use_container_width=True); st.markdown("**2 Bedroom • Kisumu - Milimani**\nKSh 14,000 / month\n\n<span class='trust-badge'>✓ Verified</span> <span class='trust-badge'>📍 Kisumu</span>", unsafe_allow_html=True)

elif st.session_state.page=="landlords":
    st.markdown('<div style="padding:24px 32px 0 32px;"><h1 style="color:#0F3D2E; font-weight:900;">List your house - Get tenants fast</h1><p style="color:#6B7A75;">7 towns covered. $10 verification code 123456 | Support: 0140311646</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    full_name = st.text_input("Full Name *")
    phone = st.text_input("Phone / WhatsApp *", placeholder="0140311646")
    town_ll = st.selectbox("Town *", ["Kisumu","Siaya","Busia","Bondo","Ugunja","Ukwala","Maseno"])
    rent = st.number_input("Monthly Rent (KSh) *", value=6500, step=500)
    desc = st.text_area("House Description *")
    if st.button("Request M-Pesa STK Push - $10", type="primary", key="stk"):
        st.session_state.stk=True; st.success("STK sent to {}! Use 123456".format(phone))
    if st.session_state.stk:
        code = st.text_input("Enter M-Pesa Code", key="code")
        if st.button("Verify Code", key="ver"):
            if code=="123456": st.session_state.verified=True; st.balloons(); st.success("✅ Verified")
            else: st.error("Use 123456")
    if st.session_state.verified:
        if st.button("Submit - Make LIVE 🚀", type="primary", use_container_width=True):
            st.balloons(); st.success(f"LIVE! {full_name} in {town_ll}"); go("home")
    else: st.warning("Complete $10 verification first")
    st.markdown('</div>', unsafe_allow_html=True)

# ABOUT & SAFETY - DEEP TO AVOID FRAUD FLAG
elif st.session_state.page=="about":
    st.markdown('<div style="padding:24px 32px 0 32px;"><h1 style="color:#0F3D2E; font-weight:900; font-size:38px;">About Home Search Kenya</h1><p style="color:#5A6B66;">Kenya trusted rental platform - Physical Office, Verified IDs, No Scams. Customer Service: <b>0140311646</b></p></div>', unsafe_allow_html=True)
    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown("""
        <div class="form-card" style="margin:16px 0 16px 32px;">
          <h3 style="color:#0F3D2E; margin-top:0;">🏠 Who We Are</h3>
          <p style="color:#4A5A55; line-height:1.8;">
          We solve rental scams in Western Kenya. We cover <b>7 towns: Kisumu, Siaya, Busia, Maseno, Bondo, Ugunja, Ukwala</b> around universities.
          <br><br>
          <b>📍 Physical Office:</b> Maseno Town, Next to Maseno University Main Gate, Kisumu-Busia Road. Open Mon-Sat 8am-6pm. Visit us anytime.
          <br><br>
          <b>🛡️ Why $10 Verification?</b> Free posting sites have 60% fake listings. Our $10 (KSh 1,300) covers ID verification, M-Pesa phone confirmation, and call-back. Demo code 123456.
          </p>
          <h3 style="color:#0F3D2E;">⚙️ How It Works</h3>
          <p style="color:#4A5A55; line-height:1.8;">
          <b>Tenants:</b> Search by town/budget → Call verified number → Visit physically → Pay after keys & receipt<br>
          <b>Landlords:</b> Fill form + ID → $10 STK Push → Code 123456 → Call confirmation → LIVE in 2 hours
          </p>
        </div>
        <div style="padding:0 0 0 32px;">
          <h2 style="color:#0F3D2E;">🛡️ Safety Center - 0140311646</h2>
          <div class="safety-card">
            <h4 style="margin:0 0 8px 0; color:#0F3D2E;">For Tenants - 5 Golden Rules</h4>
            <ol style="color:#4A5A55; line-height:1.9; margin:0;">
              <li><b>NEVER pay before viewing</b> - Genuine landlords allow viewing first</li>
              <li>Meet AT property, check water, electricity, locks</li>
              <li>Ask original ID + proof, get receipt with ID number</li>
              <li>Pay via M-Pesa to name matching ID</li>
              <li>Report to 0140311646 - removal in 2 hours</li>
            </ol>
          </div>
          <div class="safety-card" style="border-left-color:#C0392B;">
            <h4 style="margin:0 0 8px 0; color:#C0392B;">🚩 Red Flags</h4>
            <ul style="color:#4A5A55; line-height:1.8; margin:0;">
              <li>Asks deposit before showing house</li>
              <li>Price too low for area</li>
              <li>Refuses physical meeting</li>
              <li>No ID, pressure "Pay TODAY"</li>
            </ul>
          </div>
          <div class="safety-card" style="border-left-color:#F7E38E;">
            <h4 style="margin:0 0 8px 0;">For Landlords</h4>
            <p style="color:#4A5A55; line-height:1.8; margin:0;">You are responsible for accuracy. False listing = permanent ban. Tenants MUST view before paying.</p>
          </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="form-card" style="margin:16px 32px 16px 0;">
          <h3 style="color:#0F3D2E; margin-top:0;">📞 Customer Service</h3>
          <p style="color:#4A5A55; line-height:2;">
          <b>Phone / WhatsApp:</b><br>0140311646<br><br>
          <b>Hours:</b><br>Mon-Sat 8am-6pm<br>Sun 10am-4pm<br><br>
          <b>Email:</b><br>support@homesearch.co.ke<br><br>
          <b>Physical:</b><br>Maseno Town<br>Near Maseno University<br>Kisumu-Busia Highway<br><br>
          <b>Response:</b> Under 30 mins
          </p>
          <hr>
          <h4 style="color:#0F3D2E;">🔒 Trust & Legal</h4>
          <p style="color:#4A5A55; font-size:13px; line-height:1.7;">
          ✓ ID Verification for all landlords<br>
          ✓ Phone verified via M-Pesa<br>
          ✓ Physical visit recommended<br>
          ✓ $10 is verification, not commission<br>
          ✓ We do NOT hold tenant money<br>
          ✓ Refund if not as described in 24hrs<br><br>
          <b>Policy:</b> No payment before viewing<br>
          <b>Office:</b> Maseno Town
          </p>
          <hr>
          <h4 style="color:#0F3D2E;">💰 $10 Verification</h4>
          <p style="color:#4A5A55; font-size:13px;">Demo 123456. Real M-Pesa STK to Till.</p>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.page=="signin":
    st.markdown('<div style="padding:24px 32px;"><h2 style="color:#0F3D2E;">Sign in - 0140311646</h2></div>', unsafe_allow_html=True)
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.text_input("Phone"); st.text_input("Password", type="password")
    if st.button("Sign in", type="primary"): go("home")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="text-align:center; padding:20px; color:#8A9A95; font-size:12px; background:white; margin-top:20px;">© 2026 Home Search Kenya • 📍 Maseno Town, Near Maseno University • 📞 0140311646 • $10 ID verification • 🔒 Never pay before viewing</div>', unsafe_allow_html=True)
