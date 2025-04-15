import pandas as pd
import pickle
from flask import Flask, request, jsonify
from service.process import process_input_json, rf_predict, process_input_json_multiple
# Create a Flask app
app = Flask(__name__)


@app.route('/keepalive', methods=['GET'])
def api_health():
    return jsonify(Message="Success")

# Define a route for making predictions
@app.route("api/predict", methods=["POST"])
def predict():
    # Get JSON data from the request
    json_ = request.json


    json_ = [process_input_json(json_)]

    # Convert JSON data into a DataFrame
    print("here")
    df = pd.DataFrame(json_)

    # Use the loaded model to make predictions on the DataFrame
    prediction = rf_predict(df)

    # Add predictions to the DataFrame
    df["predicted_time"] = prediction

    result = df.to_dict(orient="records")
    # Return the predictions as a JSON response
    return jsonify({"Prediction": result})

@app.route("api/predict_multiple", methods=["POST"])
def predict_multiple():
    # Get JSON data from the request
    json_ = request.json

    json_ = process_input_json_multiple(json_)

    # Convert JSON data into a DataFrame
    df = pd.DataFrame(json_)

    # Use the loaded model to make predictions on the DataFrame
    predictions = rf_predict(df)

    # Add predictions to the DataFrame
    df["predicted_time"] = predictions

    # Sort the DataFrame by the predictions in ascending order
    sorted_df = df.sort_values(by="predicted_time", ascending=True).reset_index(drop=True)
    sorted_df["predicted_position"] = sorted_df.index + 1
    sorted_results = sorted_df.to_dict(orient="records")

    # Return the sorted predictions as a JSON response
    return jsonify({"Ranked_Predictions": sorted_results})

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
