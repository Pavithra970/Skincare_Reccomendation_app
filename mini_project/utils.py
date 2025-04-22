import torch
from torchvision import models, transforms
from PIL import Image
import pandas as pd
import os
import gdown

# Device configuration
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Skin type labels
class_names = ['Dry', 'Normal', 'Oily']

# Valid product categories
valid_categories = ["CLEANSERS", "FACE_OIL", "SERUM", "MOISTURIZERS", "UNDER_EYE_CREAM", "SUNSCREEN"]

# Image transformation for prediction
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# Load model from Google Drive
def load_model():
    model = models.resnet50(weights=None)
    num_ftrs = model.fc.in_features
    model.fc = torch.nn.Linear(num_ftrs, len(class_names))

    # Google Drive file ID
    file_id = '1FcdyGhWhvhG9L-2BtjTOB6JUWJwqhfWj'
    model_path = 'best_resnet50_skin_model.pth'

    # Check if model file exists, if not, download it
    if not os.path.exists(model_path):
        gdown.download(f'https://drive.google.com/uc?id={file_id}', model_path, quiet=False)

    # Load the model weights
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    return model

# Predict skin type
def predict_skin_type(image, model):
    image = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        outputs = model(image)
        _, predicted = torch.max(outputs, 1)
    return class_names[predicted.item()]

# Load products
def load_products():
    product_df = pd.read_excel(os.path.join("data", "skincare_product_data (2).xlsx"))
    return product_df

# Get recommendations — category-wise
def get_recommendations(skin_type, product_df, top_n=5):
    recommended = {}

    for category in valid_categories:
        filtered = product_df[
            (product_df[skin_type] == 1) &
            (product_df['Category'].str.upper() == category)
        ]
        top_products = filtered.sort_values(by='Star Rating', ascending=False).head(top_n)
        recommended[category] = top_products

    return recommended
