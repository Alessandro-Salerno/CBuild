import json
import sys
import os


class CBuildConfigurationException(Exception):
    pass


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


    def check_folders(self):
        for incdir in self.include_dirs:
            if not os.path.exists(incdir):
                raise CBuildConfigurationException(f"No such directory '{incdir}'. Required as include path.")

        for srcdir in self.source_dirs:
            if not os.path.exists(srcdir):
                raise CBuildConfigurationException(f"No such directory '{srcdir}'. Required as source directory.")

        if not os.path.exists(self.out_dir):
            os.mkdir(self.out_dir)

    
    def build_command(self) -> str:
        command = f"{self.compiler_path} -Wall -Wextra -I. {'-O3 ' if self.release_mode else '-g '}"

        for incdir in self.include_dirs:
            command += f"-I {incdir} "

        for srcdir in self.source_dirs:
            files    = [os.path.join(dp, f) for dp, dn, filenames in os.walk(srcdir) for f in filenames if os.path.splitext(f)[1] == self.file_extension]
            command += ' '.join(files)

        command += f" -o {self.out_dir}/{self.project_name}"
        return command


class CBuildCommandlineTools:
    @staticmethod
    def setup():
        os.mkdir("src")
        os.mkdir("include")
        
        with open("./CBuild.json", "w") as file:
            file.write("""{
    "directories": {
        "source":  [ "src" ],
        "include": [ "include" ],
        "output":  "dist"
    },

    "build": {
        "compiler":       "gcc",
        "file extension": ".c",
        "name":           "Example",
        "release":        true,
        "format":         "exec"
    }
}
""")

        with open("./src/main.c", "w") as file:
            file.write("""#include <stdio.h>


int main() {
    printf("Hello, world!\\n");
    return 0;
}
""")


    @staticmethod
    def help():
        print(
            f"""{'py' if os.name == 'nt' else 'python3'} -m cbuild [ options ]

OPTIONS:
    --help  | Shows this menu
    --setup | Creates a basic CBuild project in the working directory
""")


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
        config.check_folders()
        os.system(config.build_command())
        return 0

    # Simple command
    if len(argv) >= 2 and hasattr(CBuildCommandlineTools, str(argv[1]).replace("--", "")):
        getattr(CBuildCommandlineTools, str(argv[1]).replace("--", ""))(*argv[2:])
        return 0

    print(f"ERROR: Unrecognized options {' '.join(argv[1:])}")
    return -1


if __name__ == "__main__":
    exit(main(list(sys.argv)))
