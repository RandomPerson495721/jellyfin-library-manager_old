import configparser
import os
import base64
import subprocess
import traceback
from time import sleep

from jobHandler import jobHandler
from jobsManager import jobsManager
from flask import Flask, jsonify, request, make_response

config = configparser.ConfigParser()

app = Flask(__name__, instance_relative_config=True)

ConfigFile = '/'.join([app.instance_path, 'configuration.ini'])

IsNewConfig = False
UploadJobs = []

if os.path.exists(ConfigFile):
    config.read(ConfigFile)
else:
    print("File does not exist, creating...")
    IsNewConfig = True
    open(ConfigFile, 'a').close()
    print("File successfully created!")


def write_configs(file: str):
    with open(file, 'w') as conf:
        config.write(conf)


def set_default_configs():
    config.add_section('REQUIRED')
    config.set('REQUIRED', 'temp_file_path', '/'.join([app.instance_path, 'tmp/']))
    config.set('REQUIRED', 'ffmpeg_path',
               subprocess.check_output("which ffmpeg", shell=True).decode("utf-8").strip("\n"))
    config.set('REQUIRED', 'jellyfin_url', 'http://localhost:8096')
    config.set('REQUIRED', 'jellyfin_api_key', 'API_KEY_HERE')

    config.add_section('UPLOAD')
    config.set('UPLOAD', 'UnfinishedUploadJobs', ','.join(UploadJobs))
    config.set('UPLOAD', 'chunk_size', '4096')

    write_configs(ConfigFile)


if IsNewConfig:
    set_default_configs()


@app.route('/api/set-temp-file-destination', methods=['POST'])
def handle_filepath():
    filepath = str(request.form.get('path'))

    if filepath.lower().startswith('users') and not filepath.lower().startswith('/users'):
        filepath = '/' + filepath

    if request.method == 'POST' and 'path' in request.form and os.path.exists(filepath):
        config.set('REQUIRED', 'temp_file_path', filepath)
        write_configs(ConfigFile)
        return make_response('Success', 200)
    elif request.method == 'POST' and 'path' in request.form and not os.path.exists(filepath):
        os.makedirs(filepath)
        config.set('REQUIRED', 'temp_file_path', filepath)
        write_configs(ConfigFile)
        return make_response('Directory created and setting updated', 200)
    else:
        return make_response('Invalid request received', 400)


@app.route('/api/set-jellyfin-credentials', methods=['POST'])
def set_jellyfin_credentials():
    jellyfin_url = str(request.form.get('jellyfin_url'))
    jellyfin_api_key = str(request.form.get('jellyfin_api_key'))

    if request.method == 'POST' and 'jellyfin_url' in request.form and 'jellyfin_api_key' in request.form:
        config.set('REQUIRED', 'jellyfin_url', jellyfin_url)
        config.set('REQUIRED', 'jellyfin_api_key', jellyfin_api_key)
        write_configs(ConfigFile)
        return make_response('Success', 200)
    else:
        return make_response('Invalid request received', 400)


@app.route('/api/set-ffmpeg-path', methods=['POST'])
def set_ffmpeg_path():
    ffmpeg_path = str(request.form.get('ffmpeg_path'))

    if request.method == 'POST' and 'ffmpeg_path' in request.form and os.path.exists(ffmpeg_path):
        config.set('REQUIRED', 'ffmpeg_path', ffmpeg_path)
        write_configs(ConfigFile)
        return make_response('Success', 200)
    elif request.method == 'POST' and 'ffmpeg_path' in request.form and not os.path.exists(ffmpeg_path):
        return make_response('Invalid request received', 400)
    else:
        return make_response('Invalid request received', 400)


@app.route('/api/upload', methods=['POST'])
def handle_upload():
    file: request.stream = request.files['file']
    filename = file.filename
    filesize: int = int(request.form.get('filesize')) if 'filesize' in request.form else 0
    chunk_size: int = int(request.form.get('chunk_size')) if 'chunk_size' in request.form else 4096
    job = jobHandler(filesize, filename, config, chunk_size)
    UploadJobs.append(job)
    return make_response('Not implemented yet', 501)


@app.after_request
def after_request(response):
    job: jobHandler = UploadJobs[0]
    job.start_upload(request.files['file'].stream)
    sleep(122)
    return response


if __name__ == '__main__':
    app.run(debug=True)
