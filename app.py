import streamlit as st
import pandas as pd
import pickle
import numpy as np

# 1. Advanced page configuration
st.set_page_config(page_title="Bengaluru Valuation Engine", page_icon="🏠", layout="centered")

# 2. Injecting custom CSS animation loop
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab, #4F46E5, #7C3AED);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #ffffff;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    div[data-testid="stVerticalBlock"] > div:has(div.stSelectbox) {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
        color: #1E1B4B !important;
    }
    label, p, h3, .stSelectbox p, div[data-baseweb="select"] {
        color: #1E1B4B !important;
        font-weight: 600 !important;
    }
    .header-text {
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        text-align: center;
        color: white;
    }
    .stButton>button {
        background-image: linear-gradient(to right, #4F46E5 0%, #7C3AED 100%);
        color: white !important;
        font-weight: bold;
        border-radius: 12px;
        width: 100%;
        border: none;
        padding: 12px;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='header-text'>🏠 Bengaluru House Price Predictor</h1>", unsafe_allow_html=True)

# 3. Secure model load
@st.cache_resource
def load_model():
    with open("house_model.pkl", "rb") as f:
        return pickle.load(f)

try:
    model = load_model()
except Exception as e:
    st.error("Model brain missing!")

# 4. Interactive user controls
locations_list = ['Whitefield', 'Electronic City', 'Sarjapur Road', 'Yelahanka', 'Thanisandra']
location = st.selectbox("🗺️ Select Premium Location", locations_list)
total_sqft = st.number_input("📐 Total Floor Area (sqft)", min_value=300, max_value=25000, value=1200, step=50)

col1, col2 = st.columns(2)
with col1:
    bath = st.slider("🚿 Number of Bathrooms", 1, 5, 2)
with col2:
    bedrooms = st.slider("🛏️ Number of Bedrooms (BHK)", 1, 5, 2)

# 5. Math Prediction block matching your exact Colab columns
if st.button("Calculate Estimated Price"):
    try:
        # Create a dictionary with base inputs
        input_data = {
            'total_sqft': float(total_sqft),
            'bath': int(bath),
            'bedrooms': int(bedrooms)
        }
        
        # Manually construct dummy variables matching notebook drop_first=True rules
        for loc in locations_list[1:]: # Skip the first one to replicate drop_first=True
            input_data[f'location_{loc}'] = 1 if location == loc else 0
            
        user_df = pd.DataFrame([input_data])
        
        # Run prediction calculation
        prediction = model.predict(user_df)[0]
        
        st.markdown(f"""
            <div style='background-color: #ffffff; border-left: 6px solid #7C3AED; padding: 20px; border-radius: 12px; margin-top: 15px;'>
                <h4 style='margin:0; color: #6B7280; font-size: 14px;'>💰 Final Estimated Valuation</h4>
                <p style='font-size: 32px; font-weight: 800; color: #1E1B4B; margin: 5px 0 0 0;'>₹ {prediction:.2f} Lakhs</p>
            </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Execution Error. Details: {e}")
