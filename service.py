from PIL import Image
import io
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import openai
import time
import requests
import  os
def gen_filename():
    script_path = os.path.abspath( __file__ )
    localtime = time.localtime()
    result = time.strftime("%Y%m%d%I%M%S%p", localtime)
    filename = "/static/images/" + str(result) + ".jpg"
    file_path = os.path.dirname(script_path)  + filename
    # Save the image as a JPG file
    return filename , file_path

def random_gen_prompts():
    openai.api_key = os.getenv("OPENAI_KEY")
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "You are a helpful assistant who generate random products prompt "},
            {"role": "user", "content": "random products"},
            {"role": "assistant", "content": '''1. A luxury lotion bottle2. The toy  robot 3. Delicious salmon4.modern TV'''},
            {"role": "user", "content": "random products"},
            {"role": "assistant", "content": '''1. A smart watch with fitness tracking features2. A portable Bluetooth speaker3. A vegan leather handbag4. An automatic milk frother for coffee and lattes'''},
            {"role": "user", "content": "random products"},
        ]
    )
    return response['choices'][0]['message']['content']
def extend_prompts(string):
    openai.api_key = os.getenv("OPENAI_KEY")
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
    return response['choices'][0]['message']['content']
def poster_image(file , prompt , MOKKER_KEY):
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
    return response
def product_image(prompt , STABILITY_KEY):
    stability_api = client.StabilityInference(
    key=STABILITY_KEY, 
    verbose=True,
    )
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
    return rgb_im