import configparser
import os
import base64
import traceback
from flask import Flask , jsonify , request , make_response


config = configparser.ConfigParser()

app = Flask(__name__ , instance_relative_config=True)


ConfigFile = '/'.join([app.instance_path , 'configuration.ini'])

IsNewConfig = False
UploadJobs = []

if os.path.exists(ConfigFile):
    config.read(ConfigFile)
else:
    print("File does not exist, creating...")
    IsNewConfig = True
    open(ConfigFile , 'a').close()
    print("File successfully created!")


def write_configs(file: str):
    with open(file , 'w') as conf:
        config.write(conf)


def set_default_configs():
    config.add_section('REQUIRED')
    config.set('REQUIRED' , 'TempFilePath' , '/'.join([app.instance_path , 'tmp/']))

    config.add_section('UPLOAD')
    config.set('UPLOAD' , 'UnfinishedUploadJobs' , ','.join(UploadJobs))
    config.set('UPLOAD' , 'ChunkSize' , '4096')

    write_configs(ConfigFile)


if IsNewConfig:
    set_default_configs()


@app.route('/api/set-temp-file-destination' , methods=['POST'])
def handle_filepath():
    filepath = str(request.form.get('path'))

    if filepath.lower().startswith('users') and not filepath.lower().startswith('/users'):
        filepath = '/' + filepath

    if request.method == 'POST' and 'path' in request.form and os.path.exists(filepath):
        config.set('REQUIRED' , 'TempFilePath' , filepath)
        write_configs(ConfigFile)
        return make_response('Success' , 200)
    elif request.method == 'POST' and 'path' in request.form and not os.path.exists(filepath):
        os.makedirs(filepath)
        config.set('REQUIRED' , 'TempFilePath' , filepath)
        write_configs(ConfigFile)
        return make_response('Directory created and setting updated' , 200)
    else:
        return make_response('Invalid request received' , 400)

@app.route('/api/upload' , methods=['POST'])
def handle_upload():
    chunksize = 4096
    filename = request.args.get('filename')
    filesize = int(request.args.get('filesize_bytes'))

    chunk = base64.b64decode(request.data)
    #print(chunk)
    try:
        chunksize = int(request.args.get('chunksize'))
    except:
        pass

    if len(chunk) > chunksize:
        return make_response('Chunk exceeds chunk size of 4096 bytes and your chunk was %s bytes' % len(chunk) , 400)

    filename = ''.join([config.get('REQUIRED' , 'TempFilePath') , filename])

    if filename not in UploadJobs:
        UploadJobs.append(filename)
        #print(UploadJobs)



    if filename not in config.get('UPLOAD' , 'UnfinishedUploadJobs') and os.path.getsize(filename) < filesize:
        config.set('UPLOAD' , 'UnfinishedUploadJobs' , ','.join(UploadJobs))
        write_configs(ConfigFile)
    elif os.path.getsize(filename) == filesize:
        config.set('UPLOAD' , 'UnfinishedUploadJobs' , ','.join(UploadJobs))
        write_configs(ConfigFile)

    return make_response('Good!', 200)


if __name__ == '__main__':
    app.run(debug=True)
