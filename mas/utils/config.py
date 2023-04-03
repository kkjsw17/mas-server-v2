import tomllib


class Config:
    database = None

    def __init__(self, phase: str):
        with open(f"./config/{phase}.toml", "rb") as f:
            config_dict = tomllib.load(f)

        for key, val in config_dict.items():
            setattr(self, key, val)
