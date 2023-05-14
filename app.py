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
    file = request.files['file'].read()
    thought = request.form.get('thought')
    flag = request.form.get('flag')
    string = "IDEA:只要生成英文的"+thought+"，prompt細節越多越好，並將這些從最重要到不重要排列，請直接給我完整的prompt，不要生成其他東西，請不要加入不相關的prompt，只要生成一個英文prompt"
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "You are a helpful assistant which gernarate prompt."},
            {"role": "user", "content": '''Stable Diffusion is an AI art generation model similar to DALLE-2.
    Here are some prompts for generating art with Stable Diffusion. 

    Example:

    - portait of a homer simpson archer shooting arrow at forest monster, front game card, drark, marvel comics, dark, intricate, highly detailed, smooth, artstation, digital illustration
    - pirate, concept art, deep focus, fantasy, intricate, highly detailed, digital painting, artstation, matte, sharp focus, illustration
    - ghost inside a hunted room, art by lois van baarle and loish and ross tran and rossdraws and sam yang and samdoesarts and artgerm, digital art, highly detailed, intricate, sharp focus, Trending on Artstation HQ, deviantart, unreal engine 5, 4K UHD image
    - red dead redemption 2, cinematic view, epic sky, detailed, concept art, low angle, high detail, warm lighting, volumetric, godrays, vivid, beautiful, trending on artstation
    - a fantasy style portrait painting of rachel lane / alison brie hybrid in the style of francois boucher oil painting unreal 5 daz. rpg portrait, extremely detailed artgerm
    - athena, greek goddess, claudia black, art by artgerm and greg rutkowski and magali villeneuve, bronze greek armor, owl crown, d & d, fantasy, intricate, portrait, highly detailed, headshot, digital painting, trending on artstation, concept art, sharp focus, illustration
    - closeup portrait shot of a large strong female biomechanic woman in a scenic scifi environment, intricate, elegant, highly detailed, centered, digital painting, artstation, concept art, smooth, sharp focus, warframe, illustration
    - ultra realistic illustration of steve urkle as the hulk, intricate, elegant, highly detailed, digital painting, artstation, concept art, smooth, sharp focus, illustration
    - portrait of beautiful happy young ana de armas, ethereal, realistic anime, trending on pixiv, detailed, clean lines, sharp lines, crisp lines, award winning illustration, masterpiece, 4k, eugene de blaas and ross tran, vibrant color scheme, intricately detailed
    - A highly detailed and hyper realistic portrait of a gorgeous young ana de armas, lisa frank, trending on artstation, butterflies, floral, sharp focus, studio photo, intricate details, highly detailed, alberto seveso and geo2099 style

    Prompts should be written in English, excluding the artist name, and include the following rule:

    - Follow the structure of the example prompts. This means Write a description of the scene, followed by modifiers divided by commas to alter the mood, style, lighting, and more, excluding the artist name, separated by commas. place a extra commas. and place the extra Chinese translation for prompt at the end of each prompt.

    I want you to write me a list of detailed prompts exactly about the IDEA follow the rule at most 1  every time and don't generate other sentense only prompt. tell me ok if you get my point'''},
            {"role": "system", "content": "Sure, I got your point."},
            {"role": "user", "content":string},
        ]
    )
    thought = response['choices'][0]['message']['content']
    if ':' in thought:
        thought = thought[thought.index(':'):]
    paragraphs = thought.split('-')
    # Find the longest paragraph
    longest_paragraph = max(paragraphs, key=len)
    text = re.sub(r'\([^)]*\)', '', longest_paragraph)
    print(text)
    if flag == '0':
        url = "https://api.mokker.ai/v1/replace-background"
        files = {
            "image": file
        }
        payload = {
            "pos_prompt": text,
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
        image = Image.open(io.BytesIO(file))
        answers = stability_api.generate(
            prompt = text,
            init_image=image.resize((512,512)),
            seed = 0,
            steps=50, # defaults to 30 if not specified
            start_schedule=0.5,
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
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', use_reloader=False)
