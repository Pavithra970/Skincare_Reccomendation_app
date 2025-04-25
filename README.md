# 💡 SmartSkin: Personalized Skincare Recommender

SmartSkin is a web-based AI-powered system that classifies a user's skin type using a deep learning model and recommends personalized skincare products based on their skin concern. It combines computer vision, web scraping, and real-time user interaction via Streamlit.

---

##  Features

-  **Detects Skin Type** (Dry, Oily, Normal) from uploaded image using ResNet-50
-  **User selects concern** (Acne, Pigmentation, Aging, etc.)
-  **Recommends top-rated skincare products** by category
- **Uses Nykaa product data** scraped via Selenium
- **Deployed on Streamlit** with a clean UI

---


## 📸 Demo

![SmartSkin Demo](demo.gif)


## How It Works

### 1️ Skin Type Detection
- User uploads a face image via the Streamlit app.
- Image is preprocessed and passed into a fine-tuned **ResNet-50 model**.
- Model outputs one of: **Dry**, **Oily**, **Normal**.

### 2️ Concern Input
- User selects their primary concern:
  - Acne, Pigmentation, Open Pores, Dark Circles, Acne Scars, Aging

### 3️ Product Recommendation
- General product recommendations come from `skincare_product_data.xlsx`
- Concern-specific **serum** recommendations use `serum_skincare_classified.xlsx`
- Recommendations are filtered by:
  - Detected skin type
  - Selected concern (serums only)
- Sorted by **star rating**, top 5 per category are shown

### 4️ Real-Time Streamlit UI
- Upload → Select → View recommendations with price, ingredients, and links

---

## 🗂️ Project Structure

SmartSkin/
├── app.py                  # Streamlit frontend
├── utils.py                # Model logic, product filters
├── model/
│   └── best_resnet50_skin_model.pth
├── data/
│   ├── skincare_product_data.xlsx
│   └── serum_skincare_classified.xlsx
├── requirements.txt        # Dependencies
└── README.md

---

## Tech Stack

| Component        | Tool/Library            |
|------------------|--------------------------|
| Deep Learning    | PyTorch, ResNet-50        |
| Web Framework    | Streamlit                |
| Web Scraping     | Selenium                 |
| Data Handling    | Pandas                   |
| Deployment       | Streamlit Cloud / Local  |

---

## Datasets

- **Skin Image Dataset**  
  - 2,206 training | 550 validation | 134 testing images  
  - Labeled as Dry, Oily, or Normal

- **Product Dataset (Nykaa)**  
  - Scraped using Selenium  
  - Contains product name, ingredients, price, star rating, skin type tags, concern

- **Serum Dataset**  
  - Manually classified by skin concern for better filtering

## Model Performance

- **Model Used:** ResNet-50 (fine-tuned)
- **Test Accuracy:** 93.12%

| Skin Type | Precision | Recall | F1-Score |
|-----------|-----------|--------|----------|
| Dry       | 0.91      | 0.91   | 0.91     |
| Normal    | 0.93      | 0.95   | 0.94     |
| Oily      | 0.94      | 0.92   | 0.93     |


##  Deployment

This app is built using [Streamlit](https://streamlit.io) and can be deployed directly on [Streamlit Community Cloud](https://streamlit.io/cloud).


##  Local Installation

1. Clone this repository:
```bash
git clone https://github.com/Pavithra970/Skincare_Reccomendation_app.git

cd Skincare_Reccomendation_app
