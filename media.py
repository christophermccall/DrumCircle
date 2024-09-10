import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
from flask import render_template, request, flash, redirect, url_for, Blueprint
#from forum.app import app
from circle.models import Post, Message, Audio, db
import boto3
from botocore.exceptions import ClientError
s3 = boto3.client('s3')
bucket_name = 'drum-circle-app-bucket'
media = Blueprint('media', __name__, template_folder='templates')


# Upload an object to bucket
filename = ''
object_name = 'data/exercise{}.pdf'
s3.upload_file(filename, bucket_name, object_name)



# Generate pre-signed URL to share an object
url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket_name, 'Key': object_name},
        ExpiresIn=3608)
print(url)




UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['xhr2upload']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return