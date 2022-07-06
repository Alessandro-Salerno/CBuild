import json
import sys
import os


class CBuildConfiguration:
    def __init__(self, config: dict):
        self._config        = config
        self._dir_config    = config["directories"]
        self._build_config  = config["build"]

        self.source_dirs    = self._dir_config["source"]
        self.include_dirs   = self._dir_config["include"]
        self.out_dir        = self._dir_config["output"]

        self.compiler_path  = self._build_config["compiler"]
        self.file_extension = self._build_config["file extension"]
        self.project_name   = self._build_config["name"]
        self.release_mode   = self._build_config["release"]
        self.output_format  = self._build_config["format"]


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


def build_command(config: CBuildConfiguration) -> str:
    command = f"{config.compiler_path} -Wall -Wextra -I. {'-O3' if config.release_mode else '-g '}"

    for incdir in config.include_dirs:
        command += f"-I {incdir}"

    for srcdir in config.source_dirs:
        files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(srcdir) for f in filenames if os.path.splitext(f)[1] == config.file_extension]
        for file in files:
            command += f"{file} "

    command += f"-o {config.out_dir}/{config.project_name}"
    return command


def main(argv: list) -> int:
    # Build
    if len(argv) == 1:
        config = read_config()
        os.system(build_command(config))
        return 0
    
    return -1


if __name__ == "__main__":
    exit(main(list(sys.argv)))
