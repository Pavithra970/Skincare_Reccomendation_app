import torch
from torchvision import models, transforms
from PIL import Image
import pandas as pd
import os

# Device configuration
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Skin type labels
class_names = ['Dry', 'Normal', 'Oily']

# Product categories
valid_categories = ["CLEANSERS", "FACE_OIL", "SERUM", "MOISTURIZERS", "UNDER_EYE_CREAM", "SUNSCREEN"]

# Image transformation for ResNet model
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# Load the pretrained ResNet50 model
def load_model():
    model = models.resnet50(weights=None)
    num_ftrs = model.fc.in_features
    model.fc = torch.nn.Linear(num_ftrs, len(class_names))
    model_path = os.path.join("model", "best_resnet50_skin_model.pth")
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    return model

# Predict skin type from uploaded image
def predict_skin_type(image, model):
    image = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        outputs = model(image)
        _, predicted = torch.max(outputs, 1)
    return class_names[predicted.item()]

# Load general skincare products dataset
def load_products():
    product_df = pd.read_excel(r"C:/Users/DELL/Documents/2ndmini/data/skincare_product_data (2).xlsx")
    product_df.columns = product_df.columns.str.strip()
    return product_df

# Load serum products dataset
def load_serum_data():
    serum_df = pd.read_excel(r"C:/Users/DELL/Documents/2ndmini/data/serum_skincare_classified.xlsx")
    serum_df.columns = serum_df.columns.str.strip()
    return serum_df

# Concern mapping (optional enhancement)
concern_mapping = {
    "acne": "Acne",
    "pores": "Open Pores",
    "pigmentation": "Pigmentation",
    "dark circles": "Dark Circles",
    "scars": "Acne Marks & Scars",
    "aging": "Aging"
}

# Get top N recommended products by skin type and concern
def get_recommendations(skin_type, concern, product_df, serum_df, top_n=5):
    recommended = {}
    concern_col = concern_mapping.get(concern.lower(), concern.title())

    for category in valid_categories:
        if category == "SERUM":
            if concern_col in serum_df.columns:
                filtered = serum_df[
                    (serum_df[concern_col] == 1) &
                    (serum_df[skin_type] == 1)
                ]
                top_products = filtered.sort_values(by="Star Rating", ascending=False).head(top_n)
                recommended[category] = top_products
            else:
                recommended[category] = pd.DataFrame()  # Empty if concern column not found
        else:
            filtered = product_df[
                (product_df[skin_type] == 1) &
                (product_df['Category'].str.upper() == category)
            ]
            top_products = filtered.sort_values(by='Star Rating', ascending=False).head(top_n)
            recommended[category] = top_products

    return recommended
#streamlit run app.py
