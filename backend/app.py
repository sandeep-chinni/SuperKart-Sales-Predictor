# Import necessary libraries
import numpy as np
import joblib # to load serialized model
import pandas as pd # for data manipulation
from flask import Flask, request, jsonify # for creating flask API

# Initate the flask application
superkart_api = Flask("Super Kart Sales Predictor")

# Load the trained model
model = joblib.load("superkart_model.joblib")

# Use the exact feature names and order captured when the model was trained.
MODEL_FEATURES = list(model.feature_names_in_)

# Define the categorical columns that were one-hot encoded during training
# This list corresponds to the 'columns' argument in pd.get_dummies during training
TRAINING_CATEGORICAL_COLS = [
    'Product_Sugar_Content', 'Store_Size',
    'Store_Location_City_Type', 'Store_Type', 'Product_Id_char', 'Product_Type'
]

# Read input and convert them to the format the model was trained on
def preprocess_input(input_data):
  if 'Product_Type_Category' in input_data.columns:
      input_data = input_data.rename(columns={'Product_Type_Category': 'Product_Type'})

  if 'Store_Age_Years' in input_data.columns:
      input_data['Store_Establishment_Year'] = 2025 - input_data['Store_Age_Years']
      input_data = input_data.drop(columns=['Store_Age_Years'])

  categorical_columns = [col for col in TRAINING_CATEGORICAL_COLS if col in input_data.columns]
  processed_data = pd.get_dummies(input_data, columns=categorical_columns, sparse=False)
  return processed_data.reindex(columns=MODEL_FEATURES, fill_value=0).astype(float)

# Define a route for the home page (GET request)
@superkart_api.route("/")
def home():
    """
    This function handles GET requests to the root URL ("/").
    It returns a simple welcome message.
    """
    return "<h1>Super Kart Sales Predictor</h1>"

# Define an endpoint for single sales prediction (POST request)
@superkart_api.post('/v1/salespredictor')
def predict_sales():
  """
  This functions handles POST request to the '/v1/salespredictor' endpoint.
  It expects a JSON payload with feature values and returns the predicted sales.
  """
  # Get the JSON data from the request body
  data_payload = request.get_json()

  # Convert the single sample payload to a DataFrame
  sample_df = pd.DataFrame([data_payload])

  processed_df = preprocess_input(sample_df)

  # For debugging:
  if superkart_api.debug:
      print("\nProcessed DataFrame for prediction:")
      print(processed_df)

  # Make prediction
  prediction = model.predict(processed_df)

  # Return the prediction as a JSON response
  return jsonify({'predicted_sales': prediction[0]}) # prediction is an array

# Endpoint for batch prediction
@superkart_api.post('/v1/salespredictorbatch')
def predict_sales_batch():
  """
  This function handles POST requests to the '/v1/salespredictorbatch' endpoint.
  It expects a CSV file in the request body, processes it, and returns the
  predicted sales as a dictionary in the JSON response.
  """
  # Get the uploaded file
  file = request.files['file']

  # Read the CSV file into a DataFrame
  input_data = pd.read_csv(file)

  # Make predictions for all inputs
  processed_data = preprocess_input(input_data)
  predicted_prices = model.predict(processed_data).tolist()

  return jsonify({'predictions': predicted_prices})

# Add the main block to run the Flask app
if __name__ == '__main__':
    # When running in a Codespace, host='0.0.0.0' makes it accessible externally.
    # debug=True should be set to False in a production environment.
    superkart_api.run(debug=True)
