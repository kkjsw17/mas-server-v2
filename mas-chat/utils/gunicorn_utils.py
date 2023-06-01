import multiprocessing

import tomllib
from fastapi import FastAPI
from gunicorn.app.base import BaseApplication


def number_of_workers() -> int:
    return (multiprocessing.cpu_count() * 2) + 1


class MASMultiProcessingServer(BaseApplication):
    def __init__(self, app: FastAPI, config_file_path: str):
        self.application = app
        with open(config_file_path, "rb") as f:
            self.options = tomllib.load(f)

        if "workers" not in self.options:
            self.options["workers"] = number_of_workers()

        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }

        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application
