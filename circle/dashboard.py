from flask import Flask, request, redirect, render_template, Blueprint, url_for
from flask_login import LoginManager, current_user, login_required
from circle.models import User, Score, Exercise, Audio, db
import boto3
from circle.models import Exercise, db
dashboard = Blueprint('dashboard', __name__, template_folder='templates')
s3 = boto3.client('s3')
bucket_name = 'drum-circle-app-bucket-2'
location = {'LocationConstraint': 'us-east-2'}
response = s3.list_objects(Bucket=bucket_name)
for object in response['Contents']:
    print(object['Key'])


@dashboard.route('/dashboard')
@login_required
def dash():
    urls = []
    audio_urls = []

    exercises = Exercise.query.filter_by(user_id=current_user.id)

    # exercise = Exercise.query.filter_by(user_id=current_user.id).first()
    for exercise in exercises:
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': bucket_name,
                    'Key': exercise.fileName,
                    'ResponseContentType': 'application/pdf',
                    'ResponseContentDisposition': 'inline; filename="{}"'.format(exercise.fileName)},
            ExpiresIn=3608)
        audio = Audio.query.filter_by(exercise_id=exercise.exerciseID)
        audio_url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': bucket_name,
                    'Key': audio.fileName,
                    'ResponseContentType': 'audio/mpeg'},
            ExpiresIn=3608)
        audio_urls.append(audio_url)
        urls.append(url)
    return render_template('dashboard.html', urls=urls, audio_urls=audio_urls)

# url = s3.generate_presigned_url(
#     ClientMethod='get_object',
#     Params={'Bucket': bucket_name, 'Key': object_name},
#     ExpiresIn=3608)
# print(url)
