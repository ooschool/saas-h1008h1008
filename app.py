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
<<<<<<< Updated upstream
=======
import openai
import re
import requests
import base64
import json
import service
>>>>>>> Stashed changes
load_dotenv()
# NB: host url is not prepended with \"https\" nor does it have a trailing slash.
STABILITY_HOST = os.getenv('ALLOWED_EXTENSIONS')
# To get your API key, visit https://beta.dreamstudio.ai/membership
STABILITY_KEY = os.getenv('STABILITY_KEY')
print(STABILITY_KEY)
stability_api = client.StabilityInference(
    key=STABILITY_KEY, 
    verbose=True,
)


def gen_filename():
    script_path = os.path.abspath( __file__ )
    localtime = time.localtime()
    result = time.strftime("%Y%m%d%I%M%S%p", localtime)
    filename = "/static/images/" + str(result) + ".jpg"
    file_path = os.path.dirname(script_path)  + filename
    # Save the image as a JPG file
    return filename , file_path

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
<<<<<<< Updated upstream
    print(request)
    file = request.files['file'].read()
    thought = request.form.get('thought')
    image = Image.open(io.BytesIO(file))
    answers = stability_api.generate(
        prompt = thought,
        init_image=image.resize((256,256)),
        seed=12345, # if provided, specifying a random seed makes results deterministic
        steps=30, # defaults to 30 if not specified
        start_schedule=0.25,
    )
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
    rgb_im = img.convert("RGB")
    localtime = time.localtime()
    result = time.strftime("%Y%m%d%I%M%S%p", localtime)
    script_path = os.path.abspath( __file__ )
    filename = "/static/images/" + str(result) + ".jpg"
    rgb_im.save(os.path.dirname(script_path)  + filename)
    return filename
=======
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
            filename , file_path = gen_filename()
            with open(file_path, 'wb') as file:
                file.write(image_bytes)
            print(f"Image saved successfully as {file_path}.")
            # Specify the file path and name     
        except ValueError as e:
            print("Error parsing the response JSON:", str(e))
            
    else:
        rgb_im = service.product_image(prompt, STABILITY_KEY)
        filename , file_path = gen_filename()
        rgb_im.save(file_path)

    return {'filename': filename, 'title': title}
>>>>>>> Stashed changes
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', use_reloader=False)
