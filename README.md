# Image Comparison API with Flask

This project is an API built with Flask that allows for the comparison of two images using the Mean Squared Error (MSE) and detects differences between them. The API can download images from provided URLs, convert them to grayscale, and return an image that highlights the differences.

## Features

- **Image Comparison**: Uses Mean Squared Error (MSE) to calculate the difference between two images.
- **Visual Differences**: Generates a grayscale image that highlights areas where the images differ.
- **URL Support**: Images can be provided via URLs, making it easy to integrate into web applications.
- **REST API**: Simple interface with a `/compare` endpoint for comparing two images via a POST request.
- **CORS Enabled**: Configured to accept requests from any origin, allowing use from different web clients.

## How It Works

1. The client sends a `POST` request to `/compare` with a JSON containing two image URLs (`image_url1` and `image_url2`).
2. The API downloads both images and converts them to grayscale.
3. MSE is calculated to determine the level of difference between the images.
4. A binary image is created to highlight the differences.
5. The API returns the resulting image as a response, ready to be viewed.

## Example Request

```json
POST /compare
{
  "image_url1": "https://example.com/image1.png",
  "image_url2": "https://example.com/image2.png"
}
```

The response will be a PNG image that shows the differences between the two provided images.

## Requirements

- Python 3.x
- Flask
- OpenCV (cv2)
- NumPy
- Pillow
- Requests
- Flask-CORS

## Usage Instructions

1. Clone this repository and navigate to the project folder.
2. Install the dependencies with:
```bash
pip install -r requirements.txt
```
3. Run the application:
```bash
python app.py
```
4. The API will be available at http://localhost:5000.

## Deployed API

You can consume the deployed version of this API using the following URL:

**Base URL:** `https://api-compare-images.onrender.com`

### Example Request to the Deployed API

```bash
POST https://api-compare-images.onrender.com/compare
Content-Type: application/json

{
  "image_url1": "https://example.com/image1.png",
  "image_url2": "https://example.com/image2.png"
}
