import os
import time
import requests
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Home Search Kenya", page_icon="🏡", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 1.5rem; max-width: 1200px;}
.hero {padding: 1.5rem; border-radius: 18px; background: linear-gradient(120deg,#0f5132,#198754); color: white;}
.property {border: 1px solid #e5e7eb; padding: 1rem; border-radius: 14px; margin-bottom: .7rem;}
.small-muted {color: #6b7280; font-size: .9rem;}
</style>
""", unsafe_allow_html=True)

API_BASE = st.secrets.get("PAYMENT_API_BASE", os.getenv("PAYMENT_API_BASE", "http://localhost:8000")).rstrip("/")
REGISTRATION_FEE_KES = int(st.secrets.get("REGISTRATION_FEE_KES", 1300))
API_TIMEOUT = 20

# Demonstration listings: clearly labeled as samples, not real or verified homes.
SAMPLE_PROPERTIES = [
    {"town":"Siaya","type":"Bedsitter","rent":4500,"deposit":4500,"title":"Sample bedsitter — Siaya","description":"Example listing only. Replace with a verified property.","phone":""},
    {"town":"Kisumu","type":"One-bedroom","rent":9000,"deposit":9000,"title":"Sample one-bedroom — Kisumu","description":"Example listing only. Replace with a verified property.","phone":""},
    {"town":"Busia","type":"Bedsitter","rent":4000,"deposit":4000,"title":"Sample bedsitter — Busia","description":"Example listing only. Replace with a verified property.","phone":""},
]

def api_get(path, params=None):
    return requests.get(f"{API_BASE}{path}", params=params, timeout=API_TIMEOUT)

def api_post(path, payload):
    return requests.post(f"{API_BASE}{path}", json=payload, timeout=API_TIMEOUT)

st.markdown("""
<div class="hero">
<h1>🏡 Home Search Kenya</h1>
<p>Find a place to call home in Siaya, Kisumu, Busia and nearby towns.</p>
</div>
""", unsafe_allow_html=True)
st.caption("Early-access project. Sample listings are illustrative and are not verified properties.")

page = st.sidebar.radio("Navigate", ["Find a Home", "Landlord / Caretaker Registration", "About & Safety"])

if page == "Find a Home":
    st.subheader("Find a rental")
    c1, c2, c3 = st.columns(3)
    with c1:
        town = st.selectbox("Town", ["All", "Siaya", "Kisumu", "Busia"])
    with c2:
        ptype = st.selectbox("Property type", ["All", "Bedsitter", "One-bedroom", "Two-bedroom", "House"])
    with c3:
        max_rent = st.number_input("Maximum monthly rent (KSh)", min_value=0, value=15000, step=500)

    data = [p for p in SAMPLE_PROPERTIES
            if (town == "All" or p["town"] == town)
            and (ptype == "All" or p["type"] == ptype)
            and p["rent"] <= max_rent]
    if not data:
        st.info("No sample listings match those filters yet.")
    for p in data:
        with st.container(border=True):
            left, right = st.columns([3, 1])
            with left:
                st.markdown(f"### {p['title']}")
                st.write(f"**Town:** {p['town']} · **Type:** {p['type']}")
                st.write(p["description"])
                st.caption("Sample listing — not available for viewing or booking.")
            with right:
                st.metric("Monthly rent", f"KSh {p['rent']:,}")
                st.write(f"Deposit: KSh {p['deposit']:,}")
                st.write(f"Move-in estimate: KSh {p['rent'] + p['deposit']:,}")

    st.info("The current version uses sample data. Connect a database and add verified landlord listings before public launch.")

elif page == "Landlord / Caretaker Registration":
    st.subheader("Landlord / caretaker registration")
    st.write(f"Registration fee: **KSh {REGISTRATION_FEE_KES:,}**")
    st.caption("The fee is configured as an approximate KSh equivalent of US$10. Set the exact amount and fee/refund terms before launch. No payment is charged by this screen unless the payment API is configured and connected to an approved Safaricom Daraja account.")

    with st.form("start_payment"):
        full_name = st.text_input("Full name")
        phone = st.text_input("M-Pesa phone number", placeholder="e.g. 0712345678 or 254712345678")
        email = st.text_input("Email (optional)")
        role = st.selectbox("I am a", ["Landlord", "Caretaker / agent"])
        accepted = st.checkbox("I understand the registration fee and have read the fee/refund terms.")
        submitted = st.form_submit_button("Request M-Pesa payment", type="primary")

    if submitted:
        if not full_name.strip():
            st.error("Enter your full name.")
        elif not accepted:
            st.error("Please confirm the fee/refund terms.")
        else:
            try:
                resp = api_post("/payments/stk-push", {
                    "full_name": full_name.strip(),
                    "phone": phone.strip(),
                    "email": email.strip(),
                    "role": role,
                    "amount": REGISTRATION_FEE_KES,
                })
                if resp.ok:
                    result = resp.json()
                    st.session_state["pending_payment"] = {
                        "payment_id": result["payment_id"],
                        "full_name": full_name.strip(),
                        "email": email.strip(),
                        "role": role,
                    }
                    st.success("Payment request sent. Check your phone and enter your M-Pesa PIN only in the official M-Pesa prompt.")
                    st.info(f"Reference: {result['payment_id']}. Keep this reference for support.")
                else:
                    try:
                        detail = resp.json().get("detail", resp.text)
                    except Exception:
                        detail = resp.text
                    st.error(f"Could not start payment: {detail}")
            except requests.RequestException:
                st.error("The payment service is not reachable. This app will not unlock registration without confirmation from the payment service.")
                st.caption("For local testing, start payment_api.py in a second terminal. Live payments require approved Daraja production credentials and a public HTTPS callback.")

    pending = st.session_state.get("pending_payment")
    if pending:
        st.divider()
        st.markdown("#### Check payment status")
        st.write(f"Payment reference: `{pending['payment_id']}`")
        if st.button("Refresh payment status"):
            try:
                r = api_get(f"/payments/{pending['payment_id']}")
                if r.ok:
                    status = r.json().get("status", "pending")
                    if status == "paid":
                        st.session_state["payment_verified"] = pending
                        st.success("Payment verified. You can continue to the registration form.")
                    elif status in ("failed", "cancelled", "expired"):
                        st.error(f"Payment status: {status}. You can start a new payment request.")
                    else:
                        st.warning("Payment is still pending. Wait a little and refresh.")
                else:
                    st.error("Could not check payment status.")
            except requests.RequestException:
                st.error("Payment service unavailable.")
        if st.button("Auto-check for 20 seconds"):
            status_box = st.empty()
            for _ in range(10):
                try:
                    r = api_get(f"/payments/{pending['payment_id']}")
                    if r.ok:
                        status = r.json().get("status", "pending")
                        status_box.info(f"Payment status: {status}")
                        if status == "paid":
                            st.session_state["payment_verified"] = pending
                            status_box.success("Payment verified. Registration is unlocked.")
                            break
                        if status in ("failed", "cancelled", "expired"):
                            break
                except requests.RequestException:
                    status_box.error("Payment service unavailable.")
                    break
                time.sleep(2)
            st.rerun()

    verified = st.session_state.get("payment_verified")
    if verified:
        st.divider()
        st.success("Payment confirmed by the payment service. Complete the initial property submission below.")
        with st.form("property_submission"):
            property_title = st.text_input("Property title")
            town2 = st.selectbox("Property town", ["Siaya", "Kisumu", "Busia", "Other"])
            property_type = st.selectbox("Property type", ["Bedsitter", "One-bedroom", "Two-bedroom", "House", "Shop / commercial"])
            rent = st.number_input("Monthly rent (KSh)", min_value=0, step=500)
            deposit = st.number_input("Deposit (KSh)", min_value=0, step=500)
            contact = st.text_input("Public contact phone number")
            location = st.text_input("Estate / area (do not enter a private home address here)")
            description = st.text_area("Property description")
            submit_property = st.form_submit_button("Submit property for review")
        if submit_property:
            st.info("Payment has been verified, but property submission storage is not enabled in this starter version. The next development step is to save the landlord profile and property to a protected database and place the listing in pending review.")
            st.write("Submission preview:")
            st.json({
                "registrant": verified["full_name"],
                "role": verified["role"],
                "property_title": property_title,
                "town": town2,
                "property_type": property_type,
                "rent_kes": rent,
                "deposit_kes": deposit,
                "contact": contact,
                "area": location,
                "description": description,
                "review_status": "pending",
            })

elif page == "About & Safety":
    st.subheader("About Home Search Kenya")
    st.write("Home Search Kenya aims to help tenants find rental properties and connect with landlords and caretakers in Siaya, Kisumu, Busia and nearby areas.")
    st.markdown("**Before public launch**")
    st.markdown("""
    - Replace sample listings with properties whose owners or agents have been checked.
    - Publish clear registration fee, service, and refund terms.
    - Set up a secure database and protected photo storage.
    - Keep identity documents out of this prototype; use a secure verification process if documents are required.
    - Configure HTTPS, secrets, access controls, backups, and an admin review workflow.
    - Test successful, cancelled, failed, duplicate, and delayed M-Pesa callbacks.
    """)
    st.warning("This is a starter project, not yet production-ready. Do not collect real fees until Safaricom production credentials, callback verification, persistent records, and business terms are in place.")
