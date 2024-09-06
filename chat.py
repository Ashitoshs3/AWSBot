from flask import Blueprint, request, jsonify, render_template
import pandas as pd
from transformers import TapasTokenizer, TapasForQuestionAnswering, pipeline

chat = Blueprint("chat", __name__, url_prefix="/chat")

# Load the TAPAS model
model_name = "google/tapas-large-finetuned-wtq"
tokenizer = TapasTokenizer.from_pretrained(model_name)
model = TapasForQuestionAnswering.from_pretrained(model_name)

# Load the aws_inventory_detailed.xlsx dataset
dataset = pd.read_excel("./aws_inventory_detailed.xlsx")
dataset = dataset.astype(str)

# Function to process model results
def apply_model(table, queries):
    inputs = tokenizer(table=table, queries=queries, return_tensors="pt")
    outputs = model(**inputs)
    predicted_answer_coordinates, predicted_aggregation_indices = tokenizer.convert_logits_to_predictions(
        inputs, outputs.logits.detach(), outputs.logits_aggregation.detach()
    )

    id2aggregation = {0: "NONE", 1: "SUM", 2: "AVERAGE", 3: "COUNT"}
    aggregation_predictions_string = [id2aggregation[x] for x in predicted_aggregation_indices]

    answers = []
    for coordinates in predicted_answer_coordinates:
        if len(coordinates) == 1:
            answers.append(table.iat[coordinates[0]])
        else:
            cell_values = [table.iat[coordinate] for coordinate in coordinates]
            answers.append(", ".join(cell_values))

    result = ""
    for query, answer, predicted_agg in zip(queries, answers, aggregation_predictions_string):
        result += f"===> {query}: "
        if predicted_agg == "NONE":
            result += f"{answer}\n"
        else:
            result += f"{predicted_agg} > {answer}\n\n"

    return result

# Define chat routes
@chat.route("/", methods=["GET", "POST"])
def display_sentence():
    return render_template("./index.html")


@chat.route("/ask", methods=["POST"])
def ask():
    request_parameter = request.get_json(force=True)
    chat_question = request_parameter["chat_box_input"]
    
    # Apply TAPAS model to retrieve answers
    result = apply_model(dataset, [chat_question])
    
    return jsonify({"answer": result})
