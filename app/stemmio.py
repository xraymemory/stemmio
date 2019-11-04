''' 

    STEMMIO - THE AUTOMAGIC STEM CREATOR
    
    Straight-forward Flask app that wraps the Spleeter NN 
    for easy stemming and music making 

'''

import os
import zipfile
import uuid

from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from spleeter.separator import Separator

UPLOAD_FOLDER = './uploads/'
OUTPUT_FOLDER = './output/'
ZIP_FOLDER = './zip/'
ALLOWED_EXTENSIONS = ['mp3', 'm4a', 'wav']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Limit uploads to 10MB
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024


def separate_stems(file_path, output_path):
    ''' Separate vocals and accompaniment into MP3s using Spleeter NN '''
    sep = Separator("spleeter:2stems")
    sep.separate_to_file(file_path, output_path, codec="mp3")

def zipdir(path, zip_handler):
    ''' Write split MP3s to bundled zip '''
    for root, dirs, files in os.walk(path):
        for file in files:
            zip_handler.write(os.path.join(root, file))

def allowed_file(filename):
    ''' Check if filename ends in allowed extension '''
    return filename.split('.')[-1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    ''' GET: Return index with upload form and info
        POST: Assign file unique ID, save, send for processing, zip ,return zip 
    '''

    if request.method == 'POST':

        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):

            file_id = uuid.uuid4().hex[:10] + "_" + file.filename
            file_path = UPLOAD_FOLDER + file_id
            output_path = OUTPUT_FOLDER + file_id
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_id))

            separate_stems(file_path, output_path)

            zip_path = ZIP_FOLDER + file_id
            zipf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
            zipdir(output_path, zipf)
            zipf.close()

            return send_from_directory(directory=ZIP_FOLDER, filename=file_id, as_attachment=True, attachment_filename=file.filename+"_stems.zip")

        else:
            print("Something's fucked")

    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug = True)
