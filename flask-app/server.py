import PIL
from flask import Flask, request
import tensorflow as tf
import numpy as np
from keras.preprocessing import image

app = Flask(__name__)


@app.route('/disease-analyzer', methods=['POST'])
def diseaseanalyzer():
    try:
        img_path = request.json['img']

        img_arr = image.img_to_array(
            image.load_img(img_path, color_mode='rgb'))

        img_arr = tf.expand_dims(img_arr, axis=0)

        model = tf.saved_model.load('model/')
        f = model.signatures["serving_default"]

        outputs = f(tf.constant(img_arr, tf.float32))

        prediction = tf.math.argmax(outputs["dense_1"], 1)

        disease = np.array_str(prediction.numpy())

        disease_class = "N/A"

        if disease == '[0]':
            disease_class = '0'
        elif disease == '[1]':
            disease_class = '1'
        elif disease == '[2]':
            disease_class = '2'
        elif disease == '[3]':
            disease_class = '3'

        return disease_class

    except Exception as e:
        return "Prediction Error"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=4040)
