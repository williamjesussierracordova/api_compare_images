from flask import Flask, request, jsonify, send_file
import cv2
import numpy as np
import io
from PIL import Image
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

@app.route('/compare', methods=['POST'])
def compare():
    file1 = request.files['image1']
    file2 = request.files['image2']
    image1 = np.array(Image.open(file1))
    image2 = np.array(Image.open(file2))

    result_image, error = compare_images(image1, image2)

    # Convert PIL image to bytes for sending as response
    img_io = io.BytesIO()
    result_image.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
