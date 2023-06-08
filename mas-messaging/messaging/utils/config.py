import tomllib


class Config:
    """
    Mas Configuration Class

    Note:
        To create a new configuration attribute, you should follow the following procedure.

        1. Create a new config in config/local.toml for all phase common configurations
            and in config/${phase}.toml for phase-specific configurations.
        2. Declares the new config as a class variable with None.
        3. Using it!

    Args:
        phase (str): running phase e.g. 'real', 'local', ...
    """

    database = None
    kafka = None

    def __init__(self, phase: str):
        with open("./config/local.toml", "rb") as f:
            config_dict = tomllib.load(f)

        for key, val in config_dict.items():
            setattr(self, key, val)

        with open(f"./config/{phase}.toml", "rb") as f:
            config_dict = tomllib.load(f)

        for key, val in config_dict.items():
            if (existing_val := getattr(self, key)) is None:
                setattr(self, key, val)
            else:
                for sub_key, sub_val in val.items():
                    if isinstance(sub_val, dict):
                        existing_val[sub_key].update(sub_val)
                    else:
                        existing_val[sub_key] = sub_val
