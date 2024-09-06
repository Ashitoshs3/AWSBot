from flask import Blueprint, request, jsonify, render_template
import pandas as pd
import numpy as np
import torch
from transformers import pipeline
from transformers import TapasConfig, TapasForQuestionAnswering, TapasTokenizer
from transformers import AutoTokenizer, AutoModelForTableQuestionAnswering
from transformers import TapexTokenizer, BartForConditionalGeneration

chat = Blueprint("chat", __name__, url_prefix="/chat")

model_name = "google/tapas-large-finetuned-wtq"
tokenizer = TapasTokenizer.from_pretrained(model_name)
model = TapasForQuestionAnswering.from_pretrained(model_name, local_files_only=False)

def apply_model(table, queries):
    # (Your code for apply_model remains the same)
    pass

tqa = pipeline(task="table-question-answering", model="google/tapas-large-finetuned-wtq")

# Load data from an Excel file
dataset = pd.read_excel("./data_sheet.xlsx")
dataset = dataset.reset_index(drop=True)
dataset = dataset.astype(str)

@chat.route("/", methods=["GET", "POST"])
def display_sentence():
    return render_template("./index.html")

@chat.route("/ask", methods=["POST"])
def ask():
    request_parameter = request.get_json(force=True)
    chat_question = request_parameter["chat_box_input"]

    return tqa(table=dataset, query=chat_question)
