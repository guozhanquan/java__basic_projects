
import os
from pprint import pprint

from flask import Flask, render_template, url_for, send_from_directory, flash, redirect, request, jsonify
from werkzeug.utils import secure_filename

from .utils.upload import file_check
from .utils.YOLOV3.object_detection import detection_single_image
from .settings import Settings


app = Flask(__name__)
app.config.from_object(Settings)

@app.route('/uploader', methods=['GET', 'POST'])
def home1():
    files = request.files.getlist("file")
    for file1 in files:
        if file_check(file1.filename):
            filename = secure_filename(file1.filename)
            file1.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            file_url = url_for('upload_file', filename=filename)
            result = detection_single_image(os.path.join(app.config['UPLOAD_PATH'], filename))
            print("result=====",result,type(result))
            label= list(result.keys())[0]
            if label == "Scratches":
                result_url = url_for('scratches_file', filename=filename.split('.')[0] + '.jpg')
            elif label =="Bubbles":
                result_url = url_for('bubbles_file', filename=filename.split('.')[0] + '.jpg')
            else:
                result_url = url_for('download_file', filename=filename.split('.')[0]  + '.jpg')
            print("处理完一张了",file1)
    return "全部图片已经检测完成"


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST' and request.files.get('file'):
        file = request.files['file']
        if file_check(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            file_url = url_for('upload_file', filename=filename)
            result = detection_single_image(os.path.join(app.config['UPLOAD_PATH'], filename))
            print("res===",result)
            if len(result.keys()) >0:
                label = list(result.keys())[0]
                if label == "Scratches":
                    result_url = url_for('scratches_file', filename=filename.split('.')[0] + '.jpg')
                else:
                    result_url = url_for('bubbles_file', filename=filename.split('.')[0] + '.jpg')
            else:
                result_url = url_for('download_file', filename=filename.split('.')[0] + '.jpg')
            print(result_url)
            return render_template('home.html', result=result, result_url=result_url)
        else:
            flash('只允许jpg, png, jpeg格式的图片文件!', 'danger')
            return redirect(url_for('home'))
            
    return render_template('home.html')



@app.route('/upload/<filename>', methods=['GET', 'POST'])
def upload_file(filename):

    return send_from_directory(app.config['UPLOAD_PATH'], filename=filename)


@app.route('/download/<filename>', methods=['GET', 'POST'])
def download_file(filename):
    return send_from_directory(app.config['DOWNLOAD_PATH'], filename=filename)


@app.route('/scratch/<filename>', methods=['GET', 'POST'])
def scratches_file(filename):
    return send_from_directory(app.config['DOWNLOAD_PATH_SCRATCH'], filename=filename)

@app.route('/bubble/<filename>', methods=['GET', 'POST'])
def bubbles_file(filename):
    return send_from_directory(app.config['DOWNLOAD_PATH_BUBBLE'], filename=filename)

