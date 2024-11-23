from flask import Flask, render_template, request
import requests
import json
from PIL import Image 
from pytesseract import pytesseract 
import base64

app = Flask(__name__)

### GLOBAL VARIABLES ###

# Path of the tesseract executable
path_to_tesseract = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
# image_path = r"pprac\\images\\img1.png"
# Providing the tesseract executable location to pytesseract library
pytesseract.tesseract_cmd = path_to_tesseract 
subscription_key = "8e91c42b-68d5-472c-bbf6-657de65bded6"
language_codes = {"english": "en-IN", "hindi": "hi-IN", "tamil": "ta-IN", "telugu": "te-IN", "kannada": "kn-IN"}

### FUNCTIONS ###

def get_text_from_image(image_path):
    # load the image
    img = Image.open(image_path)
    # use pytesseract to get the text from the image
    text = pytesseract.image_to_string(img)
    return text

# function to generate .wav audio file from json response
def generate_file_from_json(json_response, file_name):
    with open(file_name, 'wb') as f:
        f.write(json_response)

def translate_text(text, target_language):
    url = "https://api.sarvam.ai/translate"

    payload = {
        "input": text,
        "source_language_code": language_codes["english"],
        "target_language_code": language_codes[target_language],
        "speaker_gender": "Female",
        "model": "mayura:v1",
        "enable_preprocessing": True
    }
    headers = {
        "api-subscription-key": subscription_key,
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    print(response.json()["translated_text"])
    return response.json()["translated_text"]


def generate_speech_from_image(filename, target_language):
    url = "https://api.sarvam.ai/text-to-speech"
    image_text = get_text_from_image(filename)
    translated_text = translate_text(image_text, target_language)

    payload = {
        "target_language_code": language_codes[target_language],
        "inputs": [translated_text],
        "model": "bulbul:v1",
        "speaker": "meera",
        "pitch": 1,
        "pace": 1,
        "loudness": 1,
        "speech_sample_rate": 16000,
        "enable_preprocessing": True
    }

    headers = {
        "api-subscription-key": subscription_key,
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    wav_audio = base64.b64decode(response.json()["audios"][0])

    generate_file_from_json(wav_audio, filename.split('.')[0] +".wav")

# ### MAIN ###
# generate_speech_from_image("img1", "tamil")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image_file = request.files['image']
        target_language = request.form['language']

        # Save the uploaded image to a temporary file
        image_path = 'temp_image.jpg'
        image_file.save(image_path)

        # Generate speech from the image
        generate_speech_from_image(image_path, target_language)

        return "Audio file generated successfully!"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
