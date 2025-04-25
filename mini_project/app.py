import pandas as pd
import streamlit as st
from PIL import Image
from utils import load_model, predict_skin_type, load_products, load_serum_data, get_recommendations

# ===== Streamlit Config =====
st.set_page_config(
    page_title="SmartSkin: Skincare Recommender",
    layout="centered"
)

# ===== App Header =====
st.title("💡 SmartSkin: Personalized Skincare Recommender")
st.write("Upload a clear image of your face. SmartSkin will detect your skin type and recommend products for your concern!")

# ===== Concern Descriptions =====
concern_options = {
    "Acne": "A skin condition that occurs when the hair follicles under the skin become clogged.",
    "Open Pores": "A result of excess oil production, reduced elasticity, or thick hair follicles.",
    "Pigmentation": "A condition in which patches of skin become darker than surrounding skin.",
    "Acne Marks & Scars": "A result of inflamed blemishes caused by clogged pores.",
    "Aging": "A result of rough skin texture and lack of elasticity."
}

# ===== Load Model & Data =====
with st.spinner("🔄 Loading model and product databases..."):
    model = load_model()
    products_df = load_products()
    serum_df = load_serum_data()

# ===== Upload Section =====
uploaded_file = st.file_uploader("📸 Upload your face image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="✅ Uploaded Image", use_column_width=True)

    # ===== Concern Selection =====
    st.subheader("❓ What's your primary skin concern?")
    concern = st.selectbox("Select one", list(concern_options.keys()))
    st.caption(f"💬 {concern_options[concern]}")

    # ===== Prediction & Recommendations =====
    with st.spinner("🔍 Analyzing your skin type..."):
        skin_type = predict_skin_type(image, model)
    st.success(f"🎯 Detected Skin Type: *{skin_type}*")

    # ===== Get Recommendations =====
    recommended_dict = get_recommendations(skin_type, concern, products_df, serum_df)

    st.subheader("🛍 Recommended Skincare Products by Category")

    for category, products in recommended_dict.items():
        st.markdown(f"### 🧴 {category.title()}")
        if not products.empty:
            for _, row in products.iterrows():
                st.markdown(f"""
                #### {row['Product Name']}
                💡 {row.get('Ingredients', 'No description available')}  
                💸 *Price:* ₹{row.get('Price', 'N/A')}  
                ⭐ *Star Rating:* {row.get('Star Rating', 'N/A')}  
                🔗 [Buy Here]({row.get('Product URL', '#')})
                """)
                st.markdown("---")
        else:
            st.info(f"No suitable products found in {category.title()} for *{skin_type}* skin and concern: *{concern}*.")

# ===== Footer =====
st.caption("💖 Powered by SmartSkin AI — Personalized skincare, simplified.")
