import io
import os
import pickle
from flask import Flask, render_template, request
from PIL import Image
from keras.applications.resnet import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model, Model
import numpy as np
import pyttsx3

model=load_model('model_19.h5')
model1 = ResNet50(weights = "imagenet",input_shape=(224,224,3))
model_new = Model(model1.input,model1.layers[-2].output)
max_len=35
word_to_idx = pickle.load(open("word_to_idx.pkl","rb"))
idx_to_word = pickle.load(open("idx_to_word.pkl","rb"))

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/explore',methods=['POST'])
def explore():
    return render_template('secondpage.html',caption="")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/generate_caption', methods=['POST'])
def upload():
    def preprocess_image(img):
        img = image.load_img(img,target_size=(224,224))
        img = image.img_to_array(img)
        img = np.expand_dims(img,axis=0)
        img = preprocess_input(img)
        return img

    def encode_image(img):
        img = preprocess_image(img)
        feature_vector = model_new.predict(img)
        feature_vector = feature_vector.reshape(feature_vector.shape[1],)
        return feature_vector

    def predict_caption(photo):
        in_text="startseq"
        for i in range(max_len):
            sequence = [word_to_idx[w] for w in in_text.split() if w in word_to_idx]
            sequence = pad_sequences([sequence], maxlen=max_len, padding='post')

            ypred = model.predict([photo,sequence])
            ypred = ypred.argmax()
            word = idx_to_word[ypred]
            in_text+= ' '+word

            if word =='endseq':
                break
        final_caption = in_text.split()
        final_caption = final_caption[1:-1]
        final_caption = ' '.join(final_caption)

        return final_caption
    if request.method == 'POST':
        f = request.files['userfile']
        path = "./static/{}".format(f.filename)
        f.save(path)
        photo = encode_image(path).reshape((1,2048))
        caption = predict_caption(photo)
        result_dic = {
            'image' : path,
            'caption':caption
        }
        
        engine = pyttsx3.init()
        engine.setProperty('voice','english')
        engine.setProperty('rate',150)
        engine.say(caption)
        engine.runAndWait()
        return render_template('secondpage.html',caption = caption,your_result = result_dic)
    


if __name__ == '__main__':
    app.run(debug=True)


