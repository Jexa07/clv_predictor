import streamlit as st
import pickle
import pandas as pd

st.set_page_config(page_title="💸 CLV Predictor", layout="wide")

st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-size: 18px !important;
    }
    .big-font {
        font-size: 28px !important;
        font-weight: 600;
        color: #f39c12;
    }
    .clv-box {
        background: linear-gradient(90deg, #00c853, #b2ff59);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: black;
        font-size: 22px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-font">🔮 Predict Customer Lifetime Value</div>', unsafe_allow_html=True)

model = pickle.load(open('models/rfm_model.pkl', 'rb'))
country_map = pickle.load(open('models/country_map.pkl', 'rb'))
reverse_map = {v: k for k, v in country_map.items()}

conversion_rates = {
    "GBP (£)": 1,
    "INR (₹)": 106.5
}

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🛍️ Customer Info")
    recency = st.slider("📅 Days since last purchase", 0, 365, 90)
    frequency = st.number_input("🧾 Total invoices", 1, 500, 10)
    country_name = st.selectbox("🌍 Select country", sorted(list(country_map.keys())))
    currency = st.radio("💱 Show CLV in:", list(conversion_rates.keys()))
    country_code = country_map[country_name]

    if st.button("🎯 Predict Lifetime Value"):
        features = [[recency, frequency, country_code]]
        pred_gbp = model.predict(features)[0]
        converted = pred_gbp * conversion_rates[currency]
        symbol = currency.split()[1]

        st.markdown(
            f"""
            <div class='clv-box'>
                💰 <b>Estimated CLV:</b><br><br>
                {symbol}{converted:,.2f} ({currency})
            </div>
            """, unsafe_allow_html=True
        )

with col2:
    st.subheader("📊 Summary Insights")
    try:
        df_top = pd.read_csv("data/top_customers.csv")
        avg = df_top["PredictedCLV"].mean()
        max_val = df_top["PredictedCLV"].max()
        st.metric("🔢 Average CLV", f"£{avg:.2f}")
        st.metric("👑 Max CLV", f"£{max_val:.2f}")
        st.metric("🧍‍♀️ Total Customers", len(df_top))
    except:
        st.warning("⚠️ Train the model first to see insights.")

st.markdown("---")
if st.checkbox("📋 Show Top 20 Predicted Customers"):
    try:
        st.dataframe(df_top.head(20), use_container_width=True)
    except:
        st.error("File not found. Make sure 'data/top_customers.csv' exists.")

st.markdown("---")
st.subheader("📥 Predict CLV from CSV Upload")
st.markdown("Upload a file with `Recency`, `Frequency`, `Country` columns.")

file = st.file_uploader("Upload CSV", type=["csv"])
if file:
    try:
        df_input = pd.read_csv(file)
        df_input['CountryCode'] = df_input['Country'].map(country_map)
        features = df_input[['Recency', 'Frequency', 'CountryCode']]
        preds = model.predict(features)
        df_input['Predicted CLV (£)'] = preds
        df_input['Predicted CLV (₹)'] = df_input['Predicted CLV (£)'] * conversion_rates['INR (₹)']
        st.success("✅ Predictions complete.")
        st.dataframe(df_input[['Recency', 'Frequency', 'Country', 'Predicted CLV (£)', 'Predicted CLV (₹)']])
    except Exception as e:
        st.error(f"❌ Error: {e}")
