from flask import Blueprint, request, render_template
import pandas as pd
from transformers import pipeline

chat = Blueprint("chat", __name__, url_prefix="/chat")

# Load model for table-question-answering
tqa = pipeline(task="table-question-answering", model="google/tapas-large-finetuned-wtq")

# Load dataset from Excel file
dataset = pd.read_excel("/mnt/data/aws_inventory_detailed.xlsx")
dataset = dataset.reset_index(drop=True)
dataset = dataset.astype(str)

@chat.route("/", methods=["GET", "POST"])
def display_sentence():
    return render_template("./index.html")

@chat.route("/ask", methods=["POST"])
def ask():
    request_parameter = request.get_json(force=True)
    chat_question = request_parameter["chat_box_input"]

    # Generate answer using the model
    return tqa(table=dataset, query=chat_question)
