from flask import Flask, request, jsonify
import os
from flask_cors import CORS
from pyngrok import ngrok
import threading
import pandas as pd
from transformers import pipeline

# Flask app initialization
app = Flask(__name__, instance_relative_config=True)
CORS(app)

# Ngrok initialization
port = 5000
ngrok.set_auth_token("YOUR_NGROK_AUTH_TOKEN")
public_url = ngrok.connect(port).public_url
app.config['BASE_URL'] = public_url
print(f"url is {public_url} and port is {port}")

# Start Flask in a separate thread
threading.Thread(target=app.run, kwargs={"use_reloader": False}).start()

# Load model and dataset
tqa = pipeline(task="table-question-answering", model="google/tapas-large-finetuned-wtq")

# Load the aws_inventory_detailed.xlsx file instead of the CSV
dataset = pd.read_excel("./aws_inventory_detailed.xlsx")
dataset = dataset.astype(str)  # Convert to string for consistency

@app.route("/chat", methods=["GET", "POST"])
def display_sentence():
    return render_template("./index.html")


@app.route("/chat/ask", methods=["POST"])
def ask():
    request_parameter = request.get_json(force=True)
    chat_question = request_parameter["chat_box_input"]
    
    # Apply the TAPAS model to query the dataset
    result = tqa(table=dataset, query=chat_question)
    if result:
        return jsonify({"answer": result['answer']})
    else:
        return jsonify({"answer": "Sorry, I couldn't find an answer related to your query."})
