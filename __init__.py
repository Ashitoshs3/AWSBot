from flask import Flask, Blueprint, request, jsonify, render_template
import pandas as pd
from transformers import pipeline
from flask_cors import CORS
from pyngrok import ngrok
import threading
import os

os.environ['FLASK_ENV'] = "development"

app = Flask(__name__, instance_relative_config=True)
CORS(app)

# Set up ngrok for exposing the Flask app
port = 5000
ngrok.set_auth_token("2clJ8ZLAFYkVM4o0OdRokc7FJfV_UnbPAbRQ8Z19R9Rn1sBn")
public_url = ngrok.connect(port).public_url
app.config['BASE_URL'] = public_url

print(f"url is {public_url} and port is {port}")

# Initialize the TAPAS pipeline
tqa = pipeline(task="table-question-answering", model="google/tapas-large-finetuned-wtq")

# Define a function to load the dataset
def load_dataset(file_path):
    try:
        dataset = pd.read_excel(file_path)
        dataset = dataset.reset_index(drop=True)
        dataset = dataset.astype(str)
        return dataset
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of an error

# Load data initially
dataset = load_dataset("./aws_inventory_detailed.xlsx")

# Define the chat blueprint
chat = Blueprint("chat", __name__, url_prefix="/chat")

@chat.route("/", methods=["GET", "POST"])
def display_sentence():
    return render_template("./index.html")

@chat.route("/ask", methods=["POST"])
def ask():
    request_parameter = request.get_json(force=True)
    chat_question = request_parameter.get("chat_box_input", "")

    if dataset.empty:
        return jsonify({"error": "Dataset is empty or failed to load."})

    try:
        # Use the TAPAS pipeline to get the answer
        result = tqa(table=dataset, query=chat_question)
        
        # For debugging purposes, print the result
        print(result)
        
        return jsonify(result)
    except Exception as e:
        print(f"Error processing the query: {e}")
        return jsonify({"error": "An error occurred while processing the query."})

# Register the blueprint
app.register_blueprint(chat)

# Run the app in a separate thread
def run_app():
    app.run(port=port, use_reloader=False)

threading.Thread(target=run_app).start()
