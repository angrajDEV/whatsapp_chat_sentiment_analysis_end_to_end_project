from flask import Flask, request, render_template
import os
from src.parser import parse_whatsapp
from src.sentiment import analyze_sentiment
from src.visualize import generate_visualizations
from src.logger import logging

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    messages = parse_whatsapp(file_path)
    messages = analyze_sentiment(messages)
    top_positive, top_negative, senders = generate_visualizations(messages)
    
    logging.info('Analysis completed')
    return render_template('result.html',
        top_positive=top_positive.to_dict('records'),
        top_negative=top_negative.to_dict('records'),
        senders=senders
    )

if __name__ == '__main__':
    app.run(debug=True)