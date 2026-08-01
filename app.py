import os
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
import pandas as pd
from bates_stamper import apply_bates_stamping

UPLOAD_FOLDER = 'uploads'
STAMPED_FOLDER = 'stamped_documents'
ALLOWED_EXTENSIONS = {'xlsx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STAMPED_FOLDER'] = STAMPED_FOLDER
app.secret_key = 'supersecretkey'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            # Create upload folder if it doesn't exist
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            
            manifest_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(manifest_path)
            
            try:
                # Create stamped documents folder if it doesn't exist
                if not os.path.exists(app.config['STAMPED_FOLDER']):
                    os.makedirs(app.config['STAMPED_FOLDER'])

                # Process the manifest
                processed_files, errors = apply_bates_stamping(manifest_path, app.config['STAMPED_FOLDER'])
                
                flash(f'Successfully stamped {len(processed_files)} files.')
                if errors:
                    for error in errors:
                        flash(f'Error: {error}', 'error')

            except Exception as e:
                flash(f'An error occurred during processing: {e}', 'error')
            
            return redirect(url_for('upload_file'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)