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

# Load data from the Excel file
dataset = pd.read_excel("./aws_inventory_detailed.xlsx")
dataset = dataset.reset_index(drop=True)
dataset = dataset.astype(str)

# Define the chat blueprint
chat = Blueprint("chat", __name__, url_prefix="/chat")

@chat.route("/", methods=["GET", "POST"])
def display_sentence():
    return render_template("./index.html")

@chat.route("/ask", methods=["POST"])
def ask():
    request_parameter = request.get_json(force=True)
    chat_question = request_parameter["chat_box_input"]
    
    # Use the TAPAS pipeline to get the answer
    result = tqa(table=dataset, query=chat_question)
    return jsonify(result)

# Register the blueprint
app.register_blueprint(chat)

# Run the app in a separate thread
def run_app():
    app.run(port=port, use_reloader=False)

threading.Thread(target=run_app).start()
