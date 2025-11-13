from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Folder to store uploads
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('gallery'))
    return 'Invalid file type'

@app.route('/gallery')
def gallery():
    image_names = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('gallery.html', image_names=image_names)

if __name__ == '__main__':
    app.run(debug=True)
