from flask import Flask, render_template, request, send_file
import requests
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# Replace with your Hugging Face API key
API_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
HUGGINGFACE_API_KEY = "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"

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
}

def query_huggingface_api(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to get a response. Status code: {response.status_code}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_image', methods=['POST'])
def generate_image():
    text_prompt = request.form['text_prompt']

    # Send request to Hugging Face API
    payload = {
        "inputs": text_prompt
    }
    try:
        image_bytes = query_huggingface_api(payload)
        image = Image.open(BytesIO(image_bytes))
        
        # Save the image in memory to serve it later
        img_io = BytesIO()
        image.save(img_io, 'JPEG', quality=70)
        img_io.seek(0)

        return send_file(img_io, mimetype='image/jpeg')
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)


