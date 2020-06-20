import os
import yamlreader


def get(paths: list) -> dict:
    for path in paths:
        if not os.path.isfile(path):
            raise ValueError(f"The path {path} did not refer to any existing file")

    config: dict = yamlreader.yaml_load(paths)

    config["display"]["colours"]["background"] = tuple(config["display"]["colours"]["background"])

    return config
