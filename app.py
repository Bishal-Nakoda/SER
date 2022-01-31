from distutils.command.config import config
from distutils.log import debug
from flask import Flask, render_template,request
import pickle, librosa,soundfile
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# import warnings,sys
# if not sys.warnoptions:
#     warnings.simplefilter("ignore")
# warnings.filterwarnings("ignore", category=DeprecationWarning) 

app = Flask(__name__)
UPLOAD_FOLDER = '/session_files/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# with open("model_pkl", 'rb') as f:
#     model = pickle.load(f)

scaler = StandardScaler()
encoder = OneHotEncoder()

Y = encoder.fit_transform(np.array(['angry','calm','happy','sad','surprise']).reshape(-1,1)).toarray()

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/')  
def upload():  
    return render_template("file_upload_form.html")  
 
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(f.filename)  
        # data, sample_rate = librosa.load(path, duration=2.5, offset=0.6)
        # # res1 = extract_features(data,sample_rate)
        # # result = np.array(res1)

        # # x = np.expand_dims(scaler.fit_transform(result, axis=2))
        # # # pred = model.predict(x)
        # # # y = encoder.inverse_transform(pred)

        return render_template("success.html", name = f.filename)  

def extract_features(data,sample_rate):
    # ZCR
    result = np.array([])
    zcr = np.mean(librosa.feature.zero_crossing_rate(y=data).T, axis=0)
    result=np.hstack((result, zcr)) # stacking horizontally

    # Chroma_stft
    stft = np.abs(librosa.stft(data))
    chroma_stft = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
    result = np.hstack((result, chroma_stft)) # stacking horizontally

    # MFCC
    mfcc = np.mean(librosa.feature.mfcc(y=data, sr=sample_rate).T, axis=0)
    result = np.hstack((result, mfcc)) # stacking horizontally

    # Root Mean Square Value
    rms = np.mean(librosa.feature.rms(y=data).T, axis=0)
    result = np.hstack((result, rms)) # stacking horizontally

    # MelSpectogram
    mel = np.mean(librosa.feature.melspectrogram(y=data, sr=sample_rate).T, axis=0)
    result = np.hstack((result, mel)) # stacking horizontally
    
    return result

def get_features(path):
    # duration and offset are used to take care of the no audio in start and the ending of each audio files as seen above.
    data, sample_rate = librosa.load(path, duration=2.5, offset=0.6)
    
    # without augmentation
    res1 = extract_features(data)
    result = np.array(res1)
     
    return result

if __name__=="__main__":
    app.run(debug=True)