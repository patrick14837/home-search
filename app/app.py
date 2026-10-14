import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Home Search - Siaya & Kisumu", page_icon="🏠", layout="wide")

# Sample data with real GPS coords
if 'houses' not in st.session_state:
    st.session_state.houses = pd.DataFrame([
        {"id":1, "town":"Siaya", "type":"Single Room", "rent":3500, "deposit":3500, "lat":-0.0626, "lon":34.2878, "phone":"0712345678", "photo":"https://images.unsplash.com/photo-1522708323590-d24dbb6b0267", "landlord":"Otieno"},
        {"id":2, "town":"Bondo", "type":"Bedsitter", "rent":5500, "deposit":5500, "lat":-0.0893, "lon":34.2762, "phone":"0722112233", "photo":"https://images.unsplash.com/photo-1502672023488-70e25813eb80", "landlord":"Akinyi"},
        {"id":3, "town":"Kisumu", "type":"1BR", "rent":12000, "deposit":12000, "lat":-0.0917, "lon":34.7680, "phone":"0700123456", "photo":"https://images.unsplash.com/photo-1493809842364-3750e0684b6e", "landlord":"Odhiambo"},
        {"id":4, "town":"Ugunja", "type":"2BR", "rent":8000, "deposit":8000, "lat":0.0860, "lon":34.3100, "phone":"0711223344", "photo":"https://images.unsplash.com/photo-1560448204-603b3fc33ddc", "landlord":"Atieno"},
        {"id":5, "town":"Siaya", "type":"Bedsitter", "rent":6000, "deposit":6000, "lat":-0.0590, "lon":34.2900, "phone":"0722334455", "photo":"https://images.unsplash.com/photo-1502005229762-cf1b2da7c5d6", "landlord":"Okello"},
    ])

df = st.session_state.houses

# Sidebar
st.sidebar.title("🏠 Home Search")
st.sidebar.markdown("**Kenya Business + Rental BI**")
town_filter = st.sidebar.multiselect("Filter Town", df['town'].unique(), default=df['town'].unique())
price_filter = st.sidebar.slider("Max Rent (Ksh)", 3000, 20000, 15000)
filtered = df[(df['town'].isin(town_filter)) & (df['rent'] <= price_filter)]

tab1, tab2, tab3 = st.tabs(["🔍 Find Home + Map", "📊 Interactive Dashboard", "🏘️ Landlord Portal ($10)"])

with tab1:
    st.subheader(f"Found {len(filtered)} houses - Live Map")
    st.map(filtered, latitude="lat", longitude="lon", size=20)
    cols = st.columns(3)
    for i, row in filtered.iterrows():
        with cols[i % 3]:
            st.image(row['photo'], use_column_width=True)
            st.markdown(f"**{row['type']} - {row['town']}**")
            st.markdown(f"Ksh {row['rent']} | Deposit Ksh {row['deposit']}")
            st.markdown(f"📞 {row['phone']}")
            st.link_button("Book on WhatsApp", f"https://wa.me/254{row['phone'][1:]}?text=Hi, I want to book your {row['type']} in {row['town']}")
            if st.button(f"Pay Deposit+Rent Ksh {row['rent']+row['deposit']}", key=f"pay{i}"):
                st.success("M-Pesa STK sent! You pay, landlord receives minus 5% fee. (Demo)")

with tab2:
    st.subheader("Rental Market BI - Siaya & Kisumu")
    c1, c2, c3 = st.columns(3)
    c1.metric("Avg Rent Siaya", f"Ksh {df[df.town=='Siaya']['rent'].mean():.0f}")
    c2.metric("Total Listings", len(df))
    c3.metric("Your Earnings (Demo $10 x)", f"Ksh {len(df)*1300}")
    
    fig1 = px.bar(df.groupby('town')['rent'].mean().reset_index(), x='town', y='rent', title="Avg Rent per Town", color='town')
    fig2 = px.pie(df, names='type', title="House Types Distribution")
    fig3 = px.histogram(df, x='rent', title="Price Distribution")
    st.plotly_chart(fig1, use_container_width=True)
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig2, use_container_width=True)
    col2.plotly_chart(fig3, use_container_width=True)

with tab3:
    st.subheader("Landlord - List Your House ($10 ~ Ksh 1,300)")
    st.info("Step 1: Pay $10 listing fee via M-Pesa. Step 2: Upload real photos + location.")
    paid = st.checkbox("I have paid Ksh 1,300 via M-Pesa to 0712XXXXXX (Demo tick)")
    if paid:
        with st.form("landlord_form"):
            town = st.selectbox("Town", ["Siaya","Bondo","Ugunja","Kisumu","Usenge"])
            h_type = st.selectbox("Type", ["Single Room","Bedsitter","1BR","2BR","3BR"])
            rent = st.number_input("Monthly Rent (Ksh)", 2000, 50000, 5000)
            phone = st.text_input("Your Phone Number")
            lat = st.number_input("GPS Latitude (Click Share Location on phone)", value=-0.0626, format="%.6f")
            lon = st.number_input("GPS Longitude", value=34.2878, format="%.6f")
            photos = st.file_uploader("Upload 4 Real Photos", accept_multiple_files=True)
            submit = st.form_submit_button("List My House")
            if submit:
                new = pd.DataFrame([{"id":len(df)+1, "town":town, "type":h_type, "rent":rent, "deposit":rent, "lat":lat, "lon":lon, "phone":phone, "photo":"https://images.unsplash.com/photo-1522708323590-d24dbb6b0267", "landlord":"You"}])
                st.session_state.houses = pd.concat([df, new], ignore_index=True)
                st.success("House listed! Tenants will see it on map. You paid $10. Rent will come via app (you keep 95%)")
    else:
        st.warning("Pay Ksh 1,300 to unlock listing. In real app: M-Pesa STK will auto-verify.")
        if st.button("Simulate M-Pesa Pay Ksh 1,300"):
            st.success("Payment received! Now tick the checkbox above.")
