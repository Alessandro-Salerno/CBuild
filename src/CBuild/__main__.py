import json
import sys


class CBuildConfiguration:
    def __init__(self, config: dict):
        self._config       = config
        self._dir_config   = config["directories"]
        self._build_config = config["build"]

        self.source_dirs   = self._dir_config["source"]
        self.include_dirs  = self._dir_config["include"]
        self.out_dir       = self._dir_config["output"]

        self.project_name  = self._build_config["name"]
        self.release_mode  = self._build_config["release"]
        self.output_format = self._build_config["format"]


class CBuildConfigurationException(Exception):
    pass


def read_config() -> CBuildConfiguration:
    try:
        with open("./CBuild.json", "r") as config_file:
            json_content = config_file.read()
            parsed_json  = json.loads(json_content)

            return CBuildConfiguration(parsed_json)
    except FileNotFoundError as e:
        raise CBuildConfigurationException("CBuild Configuration file not found.")
    except Exception as e:
        raise e


def main(argv: list) -> int:
    # Build
    if len(argv) == 1:
        config = read_config()
        return 0
    
    return 0


if __name__ == "__main__":
    exit(main(list(sys.argv)))
