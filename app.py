import streamlit as st
import pandas as pd
import pickle
import numpy as np

# 1. Advanced page configuration
st.set_page_config(page_title="Bengaluru Valuation Engine", page_icon="🏠", layout="centered")

# 2. Injecting a custom CSS animation loop for an eye-pleasing, shifting background
st.markdown("""
    <style>
    /* Animated Gradient Background covering the entire screen */
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

    /* Glassmorphism Floating Input Box Card */
    div[data-testid="stVerticalBlock"] > div:has(div.stSelectbox) {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.18);
        color: #1E1B4B !important;
    }

    /* Target fonts inside the card back to readable dark tones */
    label, p, h3, .stSelectbox p, div[data-baseweb="select"] {
        color: #1E1B4B !important;
        font-weight: 600 !important;
    }

    /* Custom Header Styling */
    .header-text {
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        text-align: center;
        color: white;
    }

    /* Glowing Premium Calculate Button */
    .stButton>button {
        background-image: linear-gradient(to right, #4F46E5 0%, #7C3AED 100%);
        color: white !important;
        font-weight: bold;
        border-radius: 12px;
        width: 100%;
        border: none;
        padding: 12px;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.6);
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Clean Centered App Presentation Text
st.markdown("<h1 class='header-text'>🏠 Bengaluru House Price Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #f3f4f6; font-size:16px; margin-bottom: 25px;'>An elegant, data-driven utility to estimate property valuations instantly.</p>", unsafe_allow_html=True)

# 4. Safe model extraction logic
@st.cache_resource
def load_model():
    with open("house_model.pkl", "rb") as f:
        return pickle.load(f)

try:
    model = load_model()
except Exception as e:
    st.error("Model brain 'house_model.pkl' missing from the working branch folder directory!")

# 5. User Input Panel Layout (renders cleanly embedded on the glass structure)
location = st.selectbox("🗺️ Select Premium Location", ['Whitefield', 'Electronic City', 'Sarjapur Road', 'Yelahanka', 'Thanisandra'])
total_sqft = st.number_input("📐 Total Floor Area (sqft)", min_value=300, max_value=25000, value=1200, step=50)

col1, col2 = st.columns(2)
with col1:
    bath = st.slider("🚿 Number of Bathrooms", 1, 5, 2)
with col2:
    bedrooms = st.slider("🛏️ Number of Bedrooms (BHK)", 1, 5, 2)

st.markdown("<br>", unsafe_allow_html=True)

# Prediction Pipeline Run execution
if st.button("Calculate Estimated Price"):
    user_input = pd.DataFrame([{
        'location': location,
        'total_sqft': float(total_sqft),
        'bath': int(bath),
        'bedrooms': int(bedrooms)
    }])
    
    try:
        prediction = model.predict(user_input)[0]
        st.markdown(f"""
            <div style='background-color: #ffffff; border-left: 6px solid #7C3AED; padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-top: 15px;'>
                <h4 style='margin:0; color: #6B7280; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;'>💰 Final Estimated Valuation</h4>
                <p style='font-size: 32px; font-weight: 800; color: #1E1B4B; margin: 5px 0 0 0;'>₹ {prediction:.2f} Lakhs</p>
            </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Execution Error. Details: {e}")
