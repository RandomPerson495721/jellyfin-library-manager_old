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
    processing_thread: threading.Thread

    # TODO: Implement metadata
    def __init__(self, filename: str, filesize: int, file: request.stream, chunksize: int = 4096):
        self.lock = threading.Lock()
        self.filename = filename
        self.chunksize = chunksize
        self.filesize = filesize
        self.file = file

    def start_upload(self):
        def _start_upload(_self):
            try:
                with open(_self.filename, "wb") as output:
                    while True:
                        buffer = _self.file.read(_self.chunksize)
                        if len(buffer) > 0:
                            output.write(buffer)
                        else:
                            break
                # return make_response("Upload Successful", 200)
            except IOError:
                # return make_response("Error occurred when writing file", 500)
                pass
            except Exception:
                # return make_response("Unknown server error occurred", 500)
                # TODO: Implement error tracking in the state of the class (If this works) ^
                pass

        self.processing_thread = threading.Thread(target=_start_upload, args=(self,))
        return self.processing_thread.start()

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

    def is_alive(self):
        return self.processing_thread.is_alive()
