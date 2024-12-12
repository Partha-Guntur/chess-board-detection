import tensorflow as tf
from tensorflow.keras.preprocessing import image # type: ignore
import numpy as np

import os

files = os.listdir('e:/New Folder/roboflow/')
print("Files in directory:", files)

model = tf.keras.models.load_model('/New Folder/roboflow/chessboard_detector.h5')
img_path = "/New Folder/roboflow/train/images/lichess3595__1KPNkbnp-pP1kNKn1-RqkpqQkb-kKBBkrpR-rNQkQ1kr-1QPKRNQR-pNbBPnnr-nBbbQpRQ_png_jpg.rf.f5caccf9cae142eb24d6039331349977.jpg"

img = image.load_img(img_path, target_size=(224, 224))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array /= 255.0

predictions = model.predict(img_array)

predicted_class = np.argmax(predictions, axis=1)
class_labels = {0: 'Not a Chessboard', 1: 'It is a Chessboard'}

print("Predicted class:", class_labels[predicted_class[0]])
