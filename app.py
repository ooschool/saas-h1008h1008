import getpass, os
from flask import Flask, request, redirect, url_for , render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory
from PIL import Image
from dotenv import load_dotenv
import io
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import time
import openai
import re
import requests
import base64
import json
import service
load_dotenv()
# NB: host url is not prepended with \"https\" nor does it have a trailing slash.
STABILITY_HOST = os.getenv('ALLOWED_EXTENSIONS')
# To get your API key, visit https://beta.dreamstudio.ai/membership
STABILITY_KEY = os.getenv('STABILITY_KEY')
MOKKER_KEY = os.getenv('MOKKER_KEY')
stability_api = client.StabilityInference(
    key=STABILITY_KEY, 
    verbose=True,
)

ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS')
app = Flask(__name__,template_folder='templates')
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')
MAX_CONTENT_LENGTH = os.getenv('MAX_CONTENT_LENGTH')
app.config['MAX_CONTENT_LENGTH'] = int(MAX_CONTENT_LENGTH)

@app.route('/', methods=['GET'])
def upload_file():
    return render_template('index.html' , filename1 = None)

@app.route('/', methods=['POST'])
def uploading_file():
    flag = request.form.get('flag')
    if flag == 'rand':
        filename = service.random_gen_prompts()
        title = 'Your Poster'
        return {'filename': filename, 'title': title}
    thought = request.form.get('thought')
    json_string = service.extend_prompts(thought)
    data = json.loads(json_string)
    title = data["title"]
    prompt = data["prompt"]
    print(prompt)
    if flag == 'poster':
        file = request.files['file'].read()
        response = service.poster_image(file , prompt, MOKKER_KEY)
        if response.status_code != 200:
            print("Error:", response.text)
        try:
            # Retrieve the generated images list
            images = response.json().get('images', [])
            if len(images) == 0:
                print("No generated images found in the response.")
                print("Response content:", response.content.decode())
            image = images[0]
            # Retrieve the generated image data
            image_data = image.get('image', {}).get('data')
            if not image_data:
                print("Generated image data not found for an image.")
                # Decode the base64 image data
            image_bytes = base64.b64decode(image_data)
            filename , file_path = service.gen_filename()
            with open(file_path, 'wb') as file:
                file.write(image_bytes)
            print(f"Image saved successfully as {file_path}.")
            # Specify the file path and name     
        except ValueError as e:
            print("Error parsing the response JSON:", str(e))
            
    else:
        rgb_im = service.product_image(prompt, STABILITY_KEY)
        filename , file_path = service.gen_filename()
        rgb_im.save(file_path)

    return {'filename': filename, 'title': title}
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', use_reloader=False)
