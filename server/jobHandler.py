import configparser
import os
import traceback
import threading
from types import LambdaType

from flask import Flask, jsonify, request, make_response, stream_with_context
import subprocess


class jobHandler:
    chunksize: int
    filename: str
    filesize: int
    ffmpeg_path: str
    processing_thread: threading.Thread
    # The tuple is (is_finished, is_error)
    processing_checklist: dict[str, tuple] = {"uploading": tuple[False, False],
                                              "transcoding": tuple[False, False],
                                              "finished": tuple[False, False]}

    # TODO: Implement metadata
    def __init__(self, filesize: int, filename: str, config: configparser.ConfigParser, chunksize: int = 4096):
        self.lock = threading.Lock()
        self.filename = ''.join([config.get('REQUIRED', 'temp_file_path'), filename])
        self.chunksize = chunksize
        self.filesize = filesize
        self.ffmpeg_path = config.get('REQUIRED', 'ffmpeg_path')
        #self.file = file

    def start_upload(self, file):
        def _start_upload(_self, _file):
            try:
                with open(_self.filename, "wb") as output:
                    self.processing_checklist["uploading"] = True, False
                    while True:
                        buffer = _file.read(_self.chunksize)
                        print(buffer)
                        if len(buffer) > 0:
                            output.write(buffer)
                        else:
                            break
                # return make_response("Upload Successful", 200)
            except IOError:
                # return make_response("Error occurred when writing file", 500)
                self.processing_checklist["uploading"] = False, True
                pass
            except Exception:
                # return make_response("Unknown server error occurred", 500)
                self.processing_checklist["uploading"] = False, True
                pass
            finally:
                self.processing_checklist["uploading"] = False, False

        self.processing_thread = threading.Thread(target=_start_upload, args=(self, file))
        self.processing_thread.start()

    def get_progress(self):
        filesize: int
        status_code: int
        try:
            filesize = os.path.getsize(self.filename)
            status_code = 200
        except Exception:
            filesize = -1
            status_code = 500

        return self.processing_checklist, filesize, status_code

    def start_transcode(self):
        # TODO: Implement transcoding
        # TODO: Implement error handling for ffmpeg
        initial_status_code: int = 500

        def _start_transcode(_self):
            try:
                self.processing_checklist["transcoding"] = True, False
                _self.initial_status_code = 200
            except Exception:
                self.processing_checklist["transcoding"] = False, True
                _self.initial_status_code = 500
                pass
            finally:
                self.processing_checklist["transcoding"] = False, False

        self.processing_thread = threading.Thread(target=_start_transcode, args=(self,))
        self.processing_thread.start()
        # Initial status code is 500, if transcoding fails, it will be set to 500, this will not notify the client
        # if transcoding fails after the lifecycle of this function. To track the status of transcoding, use the
        # get_progress() function.
        return initial_status_code

    def is_alive(self):
        return self.processing_thread.is_alive()
