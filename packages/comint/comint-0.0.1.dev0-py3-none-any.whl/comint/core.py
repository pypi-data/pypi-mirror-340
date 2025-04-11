# -*- coding: utf-8 -*-
from typing import Dict, Any
from pathlib import Path
import subprocess
import json
import os

# from configparser import ConfigParser
from gears.fs import writeFileSync, readFileSync, rmTree, generateFileTemp
import gears


# [CLASS] GearsCore
class GearsCore:

    str2: Dict[str, str] = {
        "unknown": ".txt",
        "cpp": ".cpp",
        "dart": ".dart",
        "rust": ".rs",
        "rs": ".rs",
        "ruby": ".rb",
        "rb": ".rb",
        "go": ".go",
        "js": ".js",
        "javascript": ".js",
        "python": ".py",
        "py": ".py",
        "php": ".php",
        "lua": ".lua",
        "shell": ".sh",
        "sh": ".sh",
        "perl": ".perl",
        "exs": ".exs",
        "elixir": ".exs",
    }
    ext2: Dict[str, str] = {
        ".txt": "text",
        ".cpp": "cpp",
        ".dart": "dart",
        ".rs": "rust",
        ".go": "go",
        ".js": "node",
        ".py": "python",
        ".php": "php",
        ".lua": "lua",
        ".sh": "sh",
        ".perl": "perl",
        ".rb": "ruby",
        ".exs": "elixir",
    }

    # [CALL] initialize
    def __init__(
        self, source4compiling: str = "",
        language: str = "unknown",
        temp: bool = False
    ) -> None:
        """Gears act as translators, converting code written by programmers
        (which is easy for humans to understand) into instructions
        that can be directly executed by the computer.

        Argument:
          - source4compiling:
         processing compilation from Bytes or String sources
          - language: available only for String typeResource
          - temp: there is an optional choice, whether to use a
          temporary file or not by default false

        Return:
          The value returned by the Compiler is a Json object.
        """
        self._resource = source4compiling
        self._language = language
        self._temp = temp

        results: dict[str, str] = self.get_compilex()
        self.resource = results["resource"]
        self.type = results["typeResource"]
        self.output = results["output"]
        self.error = results["error"]

    def __str__(self) -> str:
        results: dict[str, str] = self.get_compilex()
        return f"GearsCore(typeResource='{results['typeResource']}',\
resource='{results['resource']}', output='{results['output']}',\
error='{results['error']}')"

    def __call__(self) -> str:
        return json.dumps(self.compilex())

    def __version__(self) -> str:
        return gears.__version__

    def compilex(self) -> Dict[str, Any]:
        """Compilex is the main role to filter which parts are of
        typeResource String or File.

        Function that will execute between Files or Strings,
        which have passed the filtering stage.

        Return:
            The value returned by the Compilex is a Json object.
        """
        file: Path = Path(self._resource)
        temp_dir_name: str = GearsCore.ext2[GearsCore.str2[self._language]]
        temp_dir: str = f".tmp/{temp_dir_name}"

        # [CHECK] File or String or NoneType
        if file.is_file():
            tempD: str = f".tmp/{GearsCore.ext2[file.suffix]}"
            data = generateFileTemp(
                tempD, suffix=file.suffix, data=readFileSync(self._resource)
            )
            file_temp = writeFileSync(data["name"], data["data"])

            match GearsCore.ext2[file.suffix]:
                case "dart" | "go":
                    data_result = subprocess.run(
                        [GearsCore.ext2[file.suffix], "run", file_temp],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                case "rust":
                    os.system(f"rustc {file_temp} -o Main")
                    data_result = subprocess.run(
                        "./Main",
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                case "cpp":
                    os.system(f"g++ {file_temp} -o Main")
                    data_result = subprocess.run(
                        "./Main", stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                case "unknown":
                    data_result = subprocess.run(
                        ["cat", file_temp], stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                case _:
                    data_result = subprocess.run(
                        [GearsCore.ext2[file.suffix], file_temp],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )

            output = data_result.stdout.decode()
            error = data_result.stderr.decode()

            # [CHECK] true or false to use tempfile
            if self._temp:
                pass
            else:
                rmTree(".tmp")

            if os.path.isfile(self._resource):
                typeFile: str = 'File'
            else:
                typeFile: str = "String"

            return {
                "resource": self._resource,
                "typeResource": typeFile,
                "temporary": file_temp,
                "output": output,
                "error": error,
            }
        else:
            data = generateFileTemp(
                temp_dir,
                suffix=GearsCore.str2[self._language],
                data=self._resource,
            )
            f_temp = writeFileSync(data["name"], data["data"])
            match self._language:
                case "unknown":
                    data_result = subprocess.run(
                        ["cat", f_temp],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                case _:
                    l: str = self._language
                    engineL: str = GearsCore.ext2[GearsCore.str2[l]]
                    data_result = subprocess.run(
                        [engineL, f_temp],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
            output = data_result.stdout.decode()
            error = data_result.stderr.decode()

            # [CHECK] true or false to use tempfile
            if self._temp:
                pass
            else:
                rmTree(".tmp")

            if os.path.isfile(self._resource):
                typeF: str = "File"
            else:
                typeF: str = "String"

            return {
                "resource": self._resource,
                "typeResource": typeF,
                "temporary": f_temp,
                "output": output,
                "error": error,
            }

    def get_compilex(self) -> Dict[str, str]:
        return self.compilex()
