import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Set the title for the page
st.title("Super Kart Sales Predictor")

# Heading
st.subheader("Enter Details for Prediction")

# Collect user input for sales prediction
product_weight = st.number_input("Product Weight", min_value=0.00, step=0.01)
Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Low Sugar", "No Sugar", "Regular"])
product_allocated_area = st.number_input("Product Allocated Area", min_value=0.00, step=0.001)
product_mrp = st.number_input("Product MRP", min_value=0.00, step=0.01)
store_size = st.selectbox("Store Size", ["High", "Low", "Medium"])
store_location_city_type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
store_type = st.selectbox("Store Type", ["Departmental Store", "Food Mart", "Supermarket Type1", "Supermarket Type2"])
product_id_char = st.selectbox("Product ID Character", ["DR", "FD", "NC"])
store_age_years = st.number_input("Store Age in Years", min_value=0, step=1)
product_type_category = st.selectbox("Product Type Category", ["Baking Goods", "Breads", "Breakfast", "Canned", "Dairy", "Drinks", "Frozen Foods", "Fruits and Vegetables", "Hard Drinks", "Health and Hygiene", "Household", "Meat", "Others", "Seafood", "Snack Foods", "Soft Drinks", "Starchy Foods"])

# Convert user input into dataframe
data = {
    'Product_Weight': product_weight,
    'Product_Sugar_Content': Product_Sugar_Content,
    'Product_Allocated_Area': product_allocated_area,
    'Product_MRP': product_mrp,
    'Store_Size': store_size,
    'Store_Location_City_Type': store_location_city_type,
    'Store_Type': store_type,
    'Product_Id_char': product_id_char,
    'Store_Age_Years': store_age_years,
    'Product_Type_Category': product_type_category
}

# Make prediction API call when "Predict" button is clicked
if st.button("Predict"):
    # Send a POST request to the Flask backend
    response = requests.post(f"{BACKEND_URL}/v1/salespredictor", json=data)
    if response.status_code == 200:
      prediction = response.json()["predicted_sales"]
      st.success(f"Predicted Sales: {prediction}")
    else:
      st.error(f"Error: {response.status_code}")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload a CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch"):
        # Send a POST request to the Flask
        response = requests.post(f"{BACKEND_URL}/v1/salespredictorbatch", files={"file": uploaded_file})
        if response.status_code == 200:
            prediction = response.json()
            st.success("Batch prediction successful!")
            st.json(prediction) # Display the predictions
        else:
            st.error(f"Error: {response.status_code}")
