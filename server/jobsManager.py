import configparser
import os
import traceback
import threading
from flask import Flask, jsonify, request, make_response
import jobHandler


class jobsManager:
    jobs: dict[int, jobHandler.jobHandler]
    max_concurrent_transcodes: int

    def __init__(self, max_concurrent_transcodes: int = 4):
        self.lock = threading.Lock()
        self.jobs = {}
        self.max_concurrent_transcodes = max_concurrent_transcodes

    def add_job(self, job: jobHandler.jobHandler):
        self.lock.acquire()
        index = self.jobs
        self.jobs[index] = job
        self.lock.release()
        return index

    def remove_job(self, job: int):
        self.lock.acquire()
        self.jobs.pop(job)
        self.lock.release()

    def get_job(self, job: int):
        self.lock.acquire()
        job = self.jobs[job]
        self.lock.release()
        return job

    def start(self):
        def _start():
            while True:
                if len(self.jobs) > 0:
                    for job in self.jobs:
                        if self.jobs[job].is_alive():
                            pass
                        else:
                            self.remove_job(job)


        return threading.Thread(target=_start).start()
