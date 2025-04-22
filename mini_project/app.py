import pandas as pd
import streamlit as st
from PIL import Image
from utils import load_model, predict_skin_type, load_products, get_recommendations

# ===== Streamlit App Config =====
st.set_page_config(
    page_title="SmartSkin: Skincare Recommender",
    layout="centered"
)

# ===== App Title & Description =====
st.title("💡 SmartSkin: Personalized Skincare Recommender")
st.write("Upload a clear image of your face. SmartSkin will predict your skin type and suggest tailored skincare products!")

# ===== Load Model & Product Data =====
with st.spinner("Loading model & product database..."):
    model = load_model()  # This will now download the model from Google Drive if needed
    products_df = load_products()

# ===== Image Upload Section =====
uploaded_file = st.file_uploader("📸 Upload your face image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="✅ Uploaded Image", use_column_width=True)

    with st.spinner("Analyzing skin type..."):
        skin_type = predict_skin_type(image, model)

    st.success(f"🎯 Detected Skin Type: **{skin_type}**")

    # ===== Show Product Recommendations =====
    recommended_dict = get_recommendations(skin_type, products_df)

    st.subheader("🛍️ Recommended Skincare Products by Category:")

    for category, products in recommended_dict.items():
        st.markdown(f"## 🧴 {category.title()}")

        if not products.empty:
            for _, row in products.iterrows():
                st.markdown(f"""
                    ### {row['Product Name']}
                    💡 {row['Ingredients']}  
                    💸 **Price:** ₹{row['Price']}  
                    ⭐ **Star Rating:** {row['Star Rating']}  
                    🔗 [Buy Here]({row['Product URL']})  
                """)
                st.markdown("---")
        else:
            st.info(f"No suitable products found in {category.title()} for {skin_type} skin.")

# ===== Footer =====
st.caption("💖 Powered by SmartSkin AI — Personalized skincare, simplified.")
