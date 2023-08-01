import configparser
import os
import traceback
import threading
from flask import Flask, jsonify, request, make_response


class jobHandler:
    chunksize: int
    filename: str
    filesize: int
    file: request.stream

    # TODO: Implement metadata
    def __init__(self, filename: str, filesize: int, file: request.stream, chunksize: int = 4096):
        self.lock = threading.Lock()
        self.filename = filename
        self.chunksize = chunksize
        self.filesize = filesize
        self.file = file

    def start_upload(self):
        def __start_upload__(__self__):
            try:
                with open(__self__.filename, "wb") as output:
                    while True:
                        buffer = __self__.file.read(__self__.chunksize)
                        if len(buffer) > 0:
                            output.write(buffer)
                        else:
                            break
                #return make_response("Upload Successful", 200)
            except IOError:
                #return make_response("Error occurred when writing file", 500)
                pass
            except Exception:
                #return make_response("Unknown server error occurred", 500)
                #TODO: Implement error tracking in the state of the class (If this works) ^
                pass

        return threading.Thread(target=__start_upload__(self))


    def get_progress(self):
        filesize: int
        status_code: int
        try:
            filesize = os.path.getsize(self.filename)
            status_code = 200
        except Exception:
            filesize = -1
            status_code = 500

        return make_response(jsonify({
            'uploaded_file_size': filesize,
            'other_progress_indicators': 'need_to_be_implemented'}),
            status_code)
