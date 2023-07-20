import os
from flask import Flask, render_template, request, redirect, url_for, send_file
import cv2
import numpy as np
import pytesseract
from PIL import Image
import flask
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Path to the uploads folder
app.config['UPLOAD_FOLDER'] = 'uploads'

def process_image(file_path):
    scaleFactor = 2
    # Read the image using OpenCV
    img = cv2.imread(file_path)
    # Processing to make the image suitable for OCR
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Convert image to greyscale
    img = cv2.threshold(img, 190, 255, cv2.THRESH_BINARY)[1] # Apply threshold effect
    img = cv2.resize(img, None, fx=scaleFactor, fy=scaleFactor, interpolation=cv2.INTER_LINEAR)
    
    # Perform OCR using pytesseract
    text = pytesseract.image_to_string(img)
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
        
    # Process the image and get the OCR result
    ocr_result = process_image(file_path)
        
    return render_template('result.html', extracted_text=ocr_result)

@app.route('/download_text/<text>')
def download_text(text):
    response = flask.Response(text)
    response.headers["Content-Disposition"] = "attachment; filename=extracted_text.txt"
    return response

if __name__ == '__main__':
    app.run(debug=True)
