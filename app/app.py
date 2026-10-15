import streamlit as st
st.set_page_config(page_title="Home Search Kenya", layout="wide", page_icon="🏠")

# PAGE LOGIC - SAME TAB, DIFFERENT PAGES, BACK BUTTON WORKS
params = st.query_params
if "page" in params:
    st.session_state.page = params["page"]
if "page" not in st.session_state:
    st.session_state.page = "home"
if "verified" not in st.session_state:
    st.session_state.verified=False
if "stk" not in st.session_state:
    st.session_state.stk=False

st.markdown("""
<style>
[data-testid="stHeader"]{display:none;}
.block-container{padding:0!important; max-width:100%!important; padding-top:0!important;}
.stApp{background:#FFFBF2;}
.topbar {background:#0F3D2E; height:64px; width:100%; display:flex; align-items:center; justify-content:space-between; padding:0 32px; position:sticky; top:0; z-index:9999;}
.topbar.logo {color:white!important; font-weight:900; font-size:22px; text-decoration:none; cursor:pointer;}
.topbar.logo span {color:#F7E38E!important;}
.topbar.nav {display:flex; gap:14px; align-items:center;}
.topbar.nav a {color:#E0EDE8!important; font-size:14px; font-weight:600; padding:8px 16px; border-radius:8px; text-decoration:none!important; cursor:pointer;}
.topbar.nav a.active {background:#F7E38E!important; color:#0F3D2E!important; font-weight:800;}
.topbar.nav a.signin {border:1px solid #F7E38E!important; color:#F7E38E!important;}
.hero{height:460px; background:linear-gradient(to right, rgba(0,0,0,0.62), rgba(0,0,0,0.2)), url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1600&q=80'); background-size:cover; background-position:center; padding:40px 32px; display:flex; flex-direction:column; justify-content:center;}
.hero h1{color:white; font-size:52px; font-weight:800; line-height:1.05; margin:0;}
.search-box{background:white; border-radius:16px; padding:16px; margin:-32px 32px 0 32px; box-shadow:0 12px 40px rgba(0,0,0,0.18);}
.form-card{background:white; border-radius:16px; padding:24px; box-shadow:0 8px 30px rgba(0,0,0,0.08); border:1px solid #EFE9E0; margin:24px 32px;}
.safety-card{background:white; border-radius:12px; padding:20px; border-left:4px solid #0F3D2E; box-shadow:0 4px 16px rgba(0,0,0,0.06); margin-bottom:16px;}
</style>

<script>
window.addEventListener('popstate', function() {
    window.location.reload();
});
function goPage(page){
    const url = new URL(window.location);
    url.searchParams.set('page', page);
    window.history.pushState({}, '', url);
    window.location.reload();
}
</script>
""", unsafe_allow_html=True)

def active(p): return "active" if st.session_state.page==p else ""

st.markdown(f"""
<div class="topbar">
  <a onclick="goPage('home')" class="logo">Home Search <span>Kenya</span></a>
  <div class="nav">
    <a onclick="goPage('home')" class="{active('home')}">Find a Home</a>
    <a onclick="goPage('landlords')" class="{active('landlords')}">Landlords</a>
    <a onclick="goPage('about')" class="{active('about')}">About & Safety</a>
    <a onclick="goPage('signin')" class="signin {active('signin')}">Sign in</a>
  </div>
</div>
""", unsafe_allow_html=True)

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
    st.markdown('<div style="padding:24px 32px 0 32px;"><h2 style="color:#0F3D2E;">Homes you might love</h2><p>Verified homes in Kisumu, Siaya, Busia, Maseno</p></div>', unsafe_allow_html=True)
    cols=st.columns(3)
    with cols[0]:
        st.image("https://images.unsplash.com/photo-1605146769289-440113cc3d00?w=600", use_container_width=True)
        st.write("**Bedsitter • Maseno** KSh 5,500 - Maseno University")
    with cols[1]:
        st.image("https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=600", use_container_width=True)
        st.write("**1 Bedroom • Maseno** KSh 8,000 - Maseno Town")
    with cols[2]:
        st.image("https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=600", use_container_width=True)
        st.write("**2 Bedroom • Kisumu** KSh 14,000 - Milimani")
    if go: st.balloons(); st.success(f"Showing homes in {town} - Maseno added!")

elif st.session_state.page=="landlords":
    st.markdown("""
    <div style="padding:28px 32px 0 32px;">
      <h1 style="color:#0F3D2E; font-weight:900;">List your house - Get tenants fast</h1>
      <p style="color:#6B7A75;">Towns: Kisumu, Siaya, Busia, Maseno, Bondo, Ugunja, Ukwala. Verification $10 (DEMO code 123456) | Support: 0140311646</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        full_name = st.text_input("Full Name *", placeholder="e.g. John Otieno")
        id_number = st.text_input("ID Number *", placeholder="e.g. 34567890")
        phone = st.text_input("Phone Number / WhatsApp *", placeholder="0140311646")
    with col2:
        town_ll = st.selectbox("Town *", ["Kisumu","Siaya","Busia","Bondo","Ugunja","Ukwala","Maseno"])
        estate = st.text_input("Estate / Area *", placeholder="e.g. Maseno University")
        alt_phone = st.text_input("Alternative Phone", placeholder="Optional")
    st.divider()
    st.subheader("2. House Details")
    c1,c2,c3 = st.columns(3)
    with c1: p_type = st.selectbox("Property Type *", ["Bedsitter","1 Bedroom","2 Bedroom","3 Bedroom","Single Room"])
    with c2: rent = st.number_input("Monthly Rent (KSh) *", min_value=1000, max_value=100000, value=6500, step=500)
    with c3: rooms = st.selectbox("Number of Rooms", ["1","2","3","4+"])
    desc = st.text_area("House Description *", placeholder="e.g. 2 rooms, tiled, water 24/7, near Maseno University gate...")
    st.divider()
    st.subheader("3. Photos & Verification")
    photos = st.file_uploader("Upload 3-5 clear photos of house (inside + outside) *", accept_multiple_files=True, type=["jpg","jpeg","png"])
    if photos:
        cols = st.columns(min(len(photos),3))
        for i,f in enumerate(photos):
            with cols[i%3]: st.image(f, use_container_width=True)
    st.divider()
    colA, colB = st.columns(2)
    with colA:
        st.write("**M-Pesa Verification (DEMO)**")
        if st.button("Request M-Pesa STK Push - $10", type="primary", use_container_width=True):
            st.success("✅ STK sent! For DEMO enter 123456"); st.session_state.stk=True
        if st.session_state.stk:
            code = st.text_input("Enter M-Pesa Code", placeholder="123456")
            if st.button("Verify Code", use_container_width=True):
                if code=="123456":
                    st.session_state.verified=True; st.balloons(); st.success("🎉 Verified!")
                else: st.error("Wrong code - use 123456")
    with colB:
        st.write("**Submit Listing**")
        if st.session_state.verified:
            if st.button("Submit - Make My House LIVE 🚀", type="primary", use_container_width=True):
                if full_name and phone and estate and desc:
                    st.balloons(); st.success(f"🏠 Thank you {full_name}! Your {p_type} in {estate}, {town_ll} is LIVE! Support: 0140311646"); st.query_params["page"]="home"
                else: st.error("Please fill all * fields")
        else: st.warning("🔒 Complete M-Pesa verification first - $10")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page=="about":
    st.markdown("""
    <div style="padding:28px 32px 0 32px;">
      <h1 style="color:#0F3D2E; font-weight:900; font-size:38px;">About Home Search Kenya</h1>
      <p style="color:#5A6B66; font-size:15px; max-width:800px;">Kenya's trusted rental platform for students, families and professionals in Western Kenya. We verify every listing to reduce scams and connect real landlords with real tenants.</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns([2][1])
    with col1:
        st.markdown("""
        <div class="form-card" style="margin:16px 0 16px 32px;">
          <h3 style="color:#0F3D2E;">Who We Are</h3>
          <p style="color:#4A5A55; line-height:1.7;">Home Search Kenya started to solve a big problem: fake listings, agents disappearing with deposits, and students arriving in Maseno, Siaya, Kisumu with no verified houses.<br><br>
          We now cover 7 towns: <b>Kisumu, Siaya, Busia, Maseno, Bondo, Ugunja, Ukwala</b>. Every landlord is ID-verified and every house is photo-verified before going LIVE. Our verification fee is <b>$10</b> to keep scammers away.</p>
          <h3 style="color:#0F3D2E; margin-top:24px;">How It Works</h3>
          <p style="color:#4A5A55; line-height:1.7;">
          <b>1. Tenants:</b> Search by town, estate, type, budget. View verified photos, WhatsApp landlord directly, arrange physical viewing.<br>
          <b>2. Landlords:</b> Click Landlords, enter credentials, upload clear photos, pay $10 verification (DEMO code 123456), house goes LIVE in 24hrs.<br>
          <b>3. Viewing:</b> Always view physically before paying. We never hold money for you.
          </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div style="padding:0 32px;">
          <h2 style="color:#0F3D2E;">Safety Center - Read Before Paying</h2>
          <div class="safety-card">
            <h4 style="color:#0F3D2E; margin:0;">For Tenants - Avoid Scams</h4>
            <ul style="color:#4A5A55; line-height:1.8; margin:8px 0 0 0;">
              <li><b>NEVER pay before viewing:</b> No deposit, no booking fee before you physically enter the house with keys.</li>
              <li><b>Meet at the property:</b> Meet landlord at the house, not in town. Check water, electricity, locks, neighbours.</li>
              <li><b>Verify documents:</b> Ask for ID, proof of ownership or caretaker letter.</li>
              <li><b>Get a receipt:</b> Every payment must have written receipt with house, amount, date, signature, ID.</li>
              <li><b>Beware too-cheap prices:</b> If 1-bedroom in Maseno is KSh 2,000, it's likely fake.</li>
              <li><b>Use verified badge:</b> VERIFIED houses have passed ID and photo checks. Still view physically.</li>
            </ul>
          </div>
          <div class="safety-card" style="border-left-color:#D4A017;">
            <h4 style="color:#0F3D2E; margin:0;">For Landlords - Protect Yourself</h4>
            <ul style="color:#4A5A55; line-height:1.8; margin:8px 0 0 0;">
              <li>Only upload your own houses. Do not use other people's photos.</li>
              <li>Keep ID private - only share last 4 digits until viewing.</li>
              <li>Do not ask tenants to pay via personal Till before viewing.</li>
              <li>Report suspicious inquiries to Customer Service 0140311646.</li>
            </ul>
          </div>
          <div class="safety-card" style="border-left-color:#C0392B;">
            <h4 style="color:#0F3D2E; margin:0;">Red Flags - Report Immediately</h4>
            <p style="color:#4A5A55; line-height:1.7;">Landlord asks for money before viewing, refuses video call, has no ID, pressure to pay TODAY, price changes after arrival. Call Customer Service <b>0140311646</b> and we remove listing within 2 hours.</p>
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
          <b>Hours:</b> Mon-Sat 8AM-8PM, Sun 10AM-6PM<br>
          <b>Location:</b> Maseno Town, Next to Maseno University<br>
          </p>
          <hr>
          <h4 style="color:#0F3D2E;">Coverage Towns</h4>
          <p style="color:#4A5A55;">Kisumu, Siaya, Busia, Maseno, Bondo, Ugunja, Ukwala - expanding to Kakamega soon.</p>
          <hr>
          <h4 style="color:#0F3D2E;">Verification</h4>
          <p style="color:#4A5A55;">$10 one-time fee per house. Covers ID check, photo review, call verification. DEMO code: 123456.</p>
          <hr>
          <p style="font-size:12px; color:#8A9A95;">Disclaimer: We are a listing platform. We verify IDs and photos but do not own houses. Tenants must do physical due diligence. Not liable for landlord-tenant agreements.</p>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.page=="signin":
    st.markdown('<div style="padding:28px 32px;"><h2 style="color:#0F3D2E;">Sign in</h2><p>Customer Service: 0140311646</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.text_input("Phone Number", placeholder="0140311646")
    st.text_input("Password", type="password")
    if st.button("Sign in", type="primary", use_container_width=True):
        st.success("Signed in! Support: 0140311646")
        st.query_params["page"]="home"
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="text-align:center; padding:20px; color:#8A9A95; font-size:12px;">© 2026 Home Search Kenya • Customer Service: 0140311646 • $10 verification • Maseno, Kisumu, Siaya, Busia, Bondo, Ugunja, Ukwala</div>', unsafe_allow_html=True)
