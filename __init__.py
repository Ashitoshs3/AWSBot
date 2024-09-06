from flask import Flask, render_template, request, jsonify
from flask_ngrok import run_with_ngrok  # Add this import
import openai
import os
import pandas as pd

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Flask app
app = Flask(__name__)
run_with_ngrok(app)  # Enable ngrok for public URL

# Load the xlsx data file
file_path = "path/to/your/file.xlsx"
df = pd.read_excel(file_path)

# Define a route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Define a route for processing chatbot queries
@app.route('/chat/ask', methods=['POST'])
def chat():
    user_input = request.json['chat_box_input']
    # Add your OpenAI query logic here using the user_input
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}]
    )
    answer = response.choices[0].message['content']
    return jsonify({"answer": answer})

# Run the app
if __name__ == "__main__":
    app.run()
