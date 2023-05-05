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
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', use_reloader=False)
