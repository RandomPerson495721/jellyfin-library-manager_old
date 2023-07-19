import configparser
import os
import subprocess

from flask import Flask , jsonify , request , Response , redirect
from configparser import ConfigParser

config: ConfigParser = ConfigParser()

app: Flask = Flask(__name__ , instance_relative_config=True)

ConfigFile: str = '/'.join([app.instance_path , 'configuration.ini'])

IsNewConfig: bool = False

while True:
    if os.path.exists('/'.join([app.instance_path , 'configuration.ini'])):
        # TODO: Replace printouts with a proper logging solution
        config.read('configuration.ini', '')
        break

    else:
        print("File does not exist, creating...")
        with open('/'.join([app.instance_path , 'configuration.ini']) , 'x'):
            pass
        IsNewConfig = True
        print("File successfully created!")


def write_configs(file: str):
    with open(file, 'w') as conf:
        config.write(conf)


def set_default_configs():
    # Add default configs
    config['REQUIRED'] = dict(TempFilePath='/'.join([app.instance_path, 'tmp/']))
    write_configs(ConfigFile)


if IsNewConfig:
    set_default_configs()


@app.route('/api/set-temp-file-destination' , methods=['POST'])
def handle_filepath():
    filepath = str(request.form['path'])

    if filepath.lower().startswith('users') and not filepath.lower().startswith('/users'):
        filepath = '/' + filepath

    while True:
        if request.method == 'POST' and 'path' in request.form and os.path.exists(filepath):
            config['REQUIRED'] = dict(TempFilePath=filepath)
            write_configs(ConfigFile)
            return Response(status=200)
        elif request.method == 'POST' and 'path' in request.form and not os.path.exists(filepath):
            os.makedirs(filepath)
        else:
            print("Invalid request recieved")
            return Response(status=400)


@app.route('/api/upload' , methods=['POST'])
def handle_upload():
    # TODO: Implement file upload logic

    return jsonify({'message': 'Upload endpoint'})


if __name__ == '__main__':
    app.run(debug=True)
