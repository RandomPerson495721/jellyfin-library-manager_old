import configparser
import os
import traceback
from flask import Flask , jsonify , request , make_response


class jobHandler:
    chunksize: int
    filename: str
    filesize: int
    file: request.stream

    # TODO: Implement metadata
    def __init__(self , filename: str , filesize: int , file: request.stream,  chunksize: int = 4096):
        self.filename = filename
        self.chunksize = chunksize
        self.filesize = filesize
        self.file = file

    def start_upload(self):



