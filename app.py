import streamlit as st
import pandas as pd
import pickle
import numpy as np

# Set up a beautiful page config
st.set_page_config(page_title="Bengaluru House Price Predictor", page_icon="🏠", layout="centered")

# Custom CSS styling to force a premium, centered blue-purple aesthetic
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    h1 { color: #4F46E5; text-align: center; font-family: 'Helvetica Neue', sans-serif; }
    .stButton>button {
        background-image: linear-gradient(to right, #4F46E5 0%, #7C3AED 100%);
        color: white; border-radius: 8px; width: 100%; border: none; padding: 10px;
    }
    .stButton>button:hover { color: #f3f4f6; }
    </style>
""", unsafe_allow_html=True)

st.title("🏠 Bengaluru House Price Predictor")
st.markdown("<p style='text-align: center; color: #6B7280;'>An elegant, data-driven utility to estimate property valuations instantly.</p>", unsafe_allow_html=True)

# Load the saved model brain securely
@st.cache_resource
def load_model():
    with open("house_model.pkl", "rb") as f:
        return pickle.load(f)

try:
    model = load_model()
except Exception as e:
    st.error("Could not load house_model.pkl. Make sure it's in the same folder!")

# Setup beautiful structured input form cards
with st.container():
    st.markdown("### 📋 Property Specifications")
    
    location = st.selectbox("🗺️ Select Location", ['Whitefield', 'Electronic City', 'Sarjapur Road', 'Yelahanka', 'Thanisandra'])
    total_sqft = st.number_input("📐 Total Area (sqft)", min_value=300, max_value=25000, value=1200, step=50)
    
    col1, col2 = st.columns(2)
    with col1:
        bath = st.slider("🚿 Number of Bathrooms", 1, 5, 2)
    with col2:
        bedrooms = st.slider("🛏️ Number of Bedrooms (BHK)", 1, 5, 2)

    # Calculation trigger button
    if st.button("Calculate Estimated Price"):
        # Construct layout matching model expectation
        user_input = pd.DataFrame([{
            'location': location,
            'total_sqft': float(total_sqft),
            'bath': int(bath),
            'bedrooms': int(bedrooms)
        }])
        
        try:
            # If your model needs encoded columns, ensure you pass data formatting correctly
            prediction = model.predict(user_input)[0]
            st.markdown(f"""
                <div style='background-color: #EEF2F6; border-left: 5px solid #4F46E5; padding: 15px; border-radius: 8px; margin-top: 15px;'>
                    <h3 style='margin:0; color: #1E1B4B;'>💰 Estimated Market Price</h3>
                    <p style='font-size: 24px; font-weight: bold; color: #4F46E5; margin: 5px 0 0 0;'>₹ {prediction:.2f} Lakhs</p>
                </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Prediction Error: Check if feature format matches template. Details: {e}")