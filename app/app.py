import streamlit as st

st.set_page_config(page_title="Home Search Kenya", layout="wide", page_icon="🏡")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
[data-testid="stHeader"] {display:none;}
.block-container {padding:0 !important; max-width:100% !important;}
.stApp {background:#FFFBF2;}
.navbar {background:#0F3D2E; height:64px; display:flex; align-items:center; justify-content:space-between; padding:0 48px; position:sticky; top:0; z-index:100;}
.nav-logo {color:white; font-weight:800; font-size:22px;}
.nav-logo span {color:#F7E38E;}
.nav-links {display:flex; gap:32px; align-items:center;}
.nav-links a {color:#CBD5D1; text-decoration:none; font-size:14px; padding-bottom:6px;}
.nav-links a.active {color:white; border-bottom:2.5px solid #F7E38E;}
.hero {height:520px; background:linear-gradient(to right, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0.15) 60%), url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1600&q=80'); background-size:cover; background-position:center; padding:64px 48px 0 48px; display:flex; flex-direction:column; justify-content:space-between;}
.hero h1 {color:white; font-size:56px; font-weight:800; line-height:1.05; max-width:420px; margin:0;}
.hero p {color:#E8EDEB; font-size:16px; margin-top:12px; max-width:360px;}
.search-wrap {background:white; border-radius:14px; padding:14px 20px; display:flex; align-items:center; gap:18px; margin:0 48px; box-shadow:0 12px 40px rgba(0,0,0,0.18); margin-top:50px;}
.search-item {flex:1; border-right:1px solid #EEE; padding-right:16px;}
.btn-search {background:#0F3D2E; color:white; border:none; padding:14px 28px; border-radius:10px; font-weight:700;}
.content {padding:36px 48px; display:flex; gap:28px;}
.section-title {font-size:26px; font-weight:800; color:#0F3D2E;}
.title-underline {width:36px; height:3px; background:#F7E38E; margin:6px 0 8px 0;}
.cards {display:flex; gap:16px;}
.card {background:white; border-radius:10px; overflow:hidden; flex:1; border:1px solid #F0EDE8;}
.card-img {height:156px; background-size:cover; background-position:center; position:relative;}
.card-tag {position:absolute; top:10px; right:10px; background:rgba(70,70,70,0.8); color:white; font-size:10px; padding:4px 8px; border-radius:12px;}
.card-body {padding:12px;}
.card-price {font-size:16px; font-weight:800; color:#0F3D2E;}
</style>

<div class="navbar">
    <div class="nav-logo">🏡 Home Search <span>Kenya</span></div>
    <div class="nav-links">
        <a class="active" href="#">Find a Home</a>
        <a href="#">Landlords</a>
        <a href="#">About & Safety</a>
        <span style="background:#F7E38E; color:#0F3D2E; padding:8px 18px; border-radius:12px; font-weight:700; font-size:14px;">👤 Sign in</span>
    </div>
</div>
<div class="hero">
    <div>
        <h1>Find a place to<br>call home.</h1>
        <p>Explore verified rentals in Siaya, Kisumu, Busia and nearby towns.</p>
    </div>
    <div class="search-wrap">
        <div class="search-item"><div style="font-size:12px; color:#6B7A75; font-weight:600;">📍 Town or estate</div><div style="font-weight:600; color:#0F3D2E;">Kisumu ▾</div></div>
        <div class="search-item"><div style="font-size:12px; color:#6B7A75; font-weight:600;">🏠 Property type</div><div style="font-weight:600; color:#0F3D2E;">Any home ▾</div></div>
        <div class="search-item"><div style="font-size:12px; color:#6B7A75; font-weight:600;">💰 Monthly budget</div><div style="font-weight:600; color:#0F3D2E;">Any budget ▾</div></div>
        <button class="btn-search">🔍 Search homes</button>
    </div>
</div>
<div class="content">
    <div style="flex:2.2;">
        <div class="section-title">Homes you might love</div>
        <div class="title-underline"></div>
        <div style="font-size:13px; color:#6B7A75; margin-bottom:18px;">Comfortable, affordable and well-located homes in your area.</div>
        <div class="cards">
            <div class="card"><div class="card-img" style="background-image:url('https://images.unsplash.com/photo-1605146769289-440113cc3d00?w=600')"><div class="card-tag">Sample listing</div></div><div class="card-body"><div style="font-size:11px; color:#5B6E69;">🛏️ Bedsitter • Kisumu</div><div class="card-price">KSh 6,500/mo</div><div style="font-size:11px; color:#8A9A95;">📍 Kisumu, Nyalenda</div></div></div>
            <div class="card"><div class="card-img" style="background-image:url('https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=600')"><div class="card-tag">Sample listing</div></div><div class="card-body"><div style="font-size:11px; color:#5B6E69;">🛏️ 1 Bedroom • Siaya</div><div class="card-price">KSh 9,000/mo</div><div style="font-size:11px; color:#8A9A95;">📍 Siaya Town</div></div></div>
            <div class="card"><div class="card-img" style="background-image:url('https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=600')"><div class="card-tag">Sample listing</div></div><div class="card-body"><div style="font-size:11px; color:#5B6E69;">🛏️ 2 Bedroom • Busia</div><div class="card-price">KSh 14,000/mo</div><div style="font-size:11px; color:#8A9A95;">📍 Busia Town</div></div></div>
        </div>
    </div>
    <div style="flex:1;">
        <div style="font-weight:700; color:#0F3D2E; font-size:14px; margin-bottom:12px;">📍 Explore homes near you ›</div>
        <div style="background:#E8F0EC; border-radius:12px; height:300px; border:1px solid #E0E8E4; display:flex; align-items:center; justify-content:center; color:#5B6E69; text-align:center;">Map<br>Siaya • Kisumu • Busia<br>Lake Victoria</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.success("Beautiful design loaded! If you see this green bar, it worked!")
