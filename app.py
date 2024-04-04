from flask import Flask, request, flash
from werkzeug.utils import secure_filename



app = Flask(__name__)

@app.route('/upload', methods = ['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return {}
        file = request.files['file']
        content = file.read()
        f = open(file.filename, 'wb')
        f.write(content)
        f.close()
        print(content)
        return {"saved": "Ok"}
app.run()