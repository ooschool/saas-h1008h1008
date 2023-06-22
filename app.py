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
load_dotenv()
# NB: host url is not prepended with \"https\" nor does it have a trailing slash.
STABILITY_HOST = os.getenv('ALLOWED_EXTENSIONS')
openai.api_key = os.getenv('OPENAI_KEY')
MOKKER_KEY = os.getenv('MOKKER_KEY')
# To get your API key, visit https://beta.dreamstudio.ai/membership
STABILITY_KEY = os.getenv('STABILITY_KEY')
print(STABILITY_KEY)
stability_api = client.StabilityInference(
    key=STABILITY_KEY, 
    verbose=True,
)



ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS')
app = Flask(__name__,template_folder='templates')
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')
MAX_CONTENT_LENGTH = os.getenv('MAX_CONTENT_LENGTH')
app.config['MAX_CONTENT_LENGTH'] = int(MAX_CONTENT_LENGTH)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def upload_file():
    return render_template('index.html' , filename1 = None)

@app.route('/', methods=['POST'])
def uploading_file():
    flag = request.form.get('flag')
    if flag == '2':
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a helpful assistant who generate random products prompt "},
                {"role": "user", "content": "random products"},
                {"role": "assistant", "content": '''1. A luxury lotion bottle<br>2. The toy  robot <br>3. Delicious salmon<br>4.modern TV<br>'''},
                {"role": "user", "content": "random products"},
                {"role": "assistant", "content": '''1. A smart watch with fitness tracking features<br>2. A portable Bluetooth speaker<br>3. A vegan leather handbag<br>4. An automatic milk frother for coffee and lattes<br>'''},
                {"role": "user", "content": "random products"},
            ]
        )
        filename = response['choices'][0]['message']['content']
        print(filename)
        title = 'Your Poster'
    else:
        thought = request.form.get('thought')
        string = thought
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a helpful assistant which gernarate prompt in json format."},
                {"role": "user", "content": "homer simpson archer"},
                {"role": "assistant", "content": '''{"title":"shooting archer",
    "prompt":"portait of a homer simpson archer shooting arrow at forest monster, front game card, drark, marvel comics, dark, intricate, highly detailed, smooth, artstation, digital illustration"}'''},
                {"role": "user", "content": "pirate"},
                {"role": "assistant", "content": '''{"title":"horrible pirate",
    "prompt":"pirate, concept art, deep focus, fantasy, intricate, highly detailed, digital painting, artstation, matte, sharp focus, illustration"}'''},
                {"role": "user", "content":string},
            ]
        )
        json_string = response['choices'][0]['message']['content']
        data = json.loads(json_string)
        title = data["title"]
        prompt = data["prompt"]
        if flag == '0':
            file = request.files['file'].read()
            url = "https://api.mokker.ai/v1/replace-background"
            files = {
                "image": file
            }
            payload = {
                "pos_prompt": prompt,
                "number_of_images": "1"
            }
            headers = {
                "Authorization": "Bearer " + MOKKER_KEY,
                "accept": "application/json"
            }
            response = requests.post(
            url = url,
            headers = headers,
            data = payload,
            files = files
            )
            if response.status_code == 200:
                # Retrieve the generated image data
                try:
                    # Retrieve the generated images list
                    images = response.json().get('images', [])

                    if images:
                        for image in images:
                            # Retrieve the generated image data
                            image_data = image.get('image', {}).get('data')

                            if image_data:
                                # Decode the base64 image data
                                image_bytes = base64.b64decode(image_data)

                                # Specify the file path and name
                                script_path = os.path.abspath( __file__ )
                                localtime = time.localtime()
                                result = time.strftime("%Y%m%d%I%M%S%p", localtime)
                                filename = "/static/images/" + str(result) + ".jpg"
                                file_path = os.path.dirname(script_path)  + filename

                                # Save the image as a JPG file
                                with open(file_path, 'wb') as file:
                                    file.write(image_bytes)

                                print(f"Image saved successfully as {file_path}.")
                            else:
                                print("Generated image data not found for an image.")
                    else:
                        print("No generated images found in the response.")
                        print("Response content:", response.content.decode())
                except ValueError as e:
                    print("Error parsing the response JSON:", str(e))
            else:
                print("Error:", response.text)
        else:
            answers = stability_api.generate(
                prompt = prompt,
                steps=50, # defaults to 30 if not specified
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

    return {'filename': filename, 'title': title}
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', use_reloader=False)
