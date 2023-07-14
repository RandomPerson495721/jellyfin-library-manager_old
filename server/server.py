import configparser
import subprocess
from flask import Flask, jsonify, request, Response
from configparser import ConfigParser
config = ConfigParser()


app = Flask(__name__, instance_relative_config = True)

while True:
    try:
        #TODO: Replace printouts with a proper logging solution
        app.config.from_pyfile('configuration.ini')
        break

    except FileNotFoundError:
        print("File does not exist, creating...")
        with open('/'.join([app.instance_path, 'configuration.ini']), 'x'):
            pass
        print("File successfully created!")


@app.route('/api/set-temp-file-destination', methods=['POST'])
def handle_filepath():
    if request.method == 'POST' and 'path' in request.form:
        filepath = str(request.form['path'])
        value = app.config.get('CONFIG_KEY')
        return Response(status= 200)
    else:
        print("Invalid request recieved")
        return Response(status= 400)
    
    

    

@app.route('/api/upload', methods=['POST'])
def handle_upload():

    # Implement file upload logic here
    return jsonify({'message': 'Upload endpoint'})


if __name__ == '__main__':
    app.run(debug=True)

