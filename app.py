from flask import Flask, request, jsonify, send_file
import cv2
import numpy as np
import io
from PIL import Image
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def mse(imageA, imageB):
    # Compute the Mean Squared Error between two images
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

def compare_images(image1, image2):
    # Convert images to grayscale
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Resize images to be the same size (if necessary)
    gray1 = cv2.resize(gray1, (640, 480))
    gray2 = cv2.resize(gray2, (640, 480))

    # Compute MSE
    error = mse(gray1, gray2)

    # Find differences
    diff = cv2.absdiff(gray1, gray2)

    # Threshold the difference image
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    # Convert the result to a PIL image for easy handling
    pil_image = Image.fromarray(thresh)
    return pil_image, error

def download_image(url):
    # Download an image from a URL and convert it to a NumPy array
    response = requests.get(url)
    image = Image.open(io.BytesIO(response.content))
    return np.array(image)

@app.route('/compare', methods=['POST'])
def compare():
    data = request.json
    url1 = data.get('image_url1')
    url2 = data.get('image_url2')

    if not url1 or not url2:
        return jsonify({'error': 'Both image URLs are required.'}), 400

    # Download images from URLs
    try:
        image1 = download_image(url1)
        image2 = download_image(url2)
    except Exception as e:
        return jsonify({'error': f'Error downloading images: {str(e)}'}), 500

    result_image, error = compare_images(image1, image2)

    # Convert PIL image to bytes for sending as response
    img_io = io.BytesIO()
    result_image.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
