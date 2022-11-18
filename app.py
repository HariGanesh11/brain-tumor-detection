import os
# Keras
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
# Flask utils
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import tensorflow_hub as hub
import  numpy as np

app = Flask(__name__)

model = load_model(('Brain_Tumor_Detection .h5'),custom_objects={'KerasLayer': hub.KerasLayer})

def model_predict(img_path, model):
    test_image = image.load_img(img_path, target_size = (224,224))
    test_image = image.img_to_array(test_image)
    test_image = test_image / 255
    test_image = np.expand_dims(test_image, axis=0)
    result = model.predict(test_image)
    result
    val=result

    if result < 0.5:
        result = "The Person has no Brain Tumor with the predicted value" + str(val)
    else:
        result = "The Person has Brain Tumor with the predicted value" + str(val)

    return result

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('reg.html')

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        result = preds
        return result
    return None
if __name__ == '__main__':
    app.run(debug=True)