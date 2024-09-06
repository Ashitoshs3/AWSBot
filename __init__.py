from flask import Flask, request, jsonify, render_template
import os
from flask_cors import CORS
from pyngrok import ngrok
import threading
import pandas as pd
from transformers import pipeline

os.environ['FLASK_ENV'] = "development"

app = Flask(__name__, instance_relative_config=True)
CORS(app)
port = 5000

# Set up ngrok for exposing the Flask app
ngrok.set_auth_token("2clJ8ZLAFYkVM4o0OdRokc7FJfV_UnbPAbRQ8Z19R9Rn1sBn")
public_url = ngrok.connect(port).public_url
app.config['BASE_URL'] = public_url

print(f"url is {public_url} and port is {port}")

# Load the TAPAS model and tokenizer
tqa = pipeline(task="table-question-answering", model="google/tapas-large-finetuned-wtq")

# Load data from the Excel file
dataset = pd.read_excel("./aws_inventory_detailed.xlsx")
dataset = dataset.reset_index(drop=True)
dataset = dataset.astype(str)

@app.route("/chat", methods=["GET", "POST"])
def display_sentence():
    return render_template("./index.html")

@app.route("/chat/ask", methods=["POST"])
def ask():
    request_parameter = request.get_json(force=True)
    chat_question = request_parameter["chat_box_input"]
    return jsonify(tqa(table=dataset, query=chat_question))

# Run the app
threading.Thread(target=app.run, kwargs={"use_reloader": False}).start()
