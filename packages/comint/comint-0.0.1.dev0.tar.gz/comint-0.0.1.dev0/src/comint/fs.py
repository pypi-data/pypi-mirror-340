# -*- coding: utf-8 -*-
from typing import Dict
from pathlib import Path
from tempfile import NamedTemporaryFile
import shutil


# [CALL] generateFileTemp
def generateFileTemp(dir: str, suffix: str, data: str) -> Dict[str, str]:
    mkdirTree(dir)
    # data = readFileSync(file.name)
    with NamedTemporaryFile(
        mode="w+t",
        encoding="utf-8",
        newline="\n",
        suffix=suffix,
        prefix="_GCtemp@",
        dir=dir,
    ) as data_temp:
        data_temp.write(data)
        data_temp.seek(0)
        return {"name": data_temp.name, "data": data_temp.read()}


# [CALL] writeFileSync
def writeFileSync(path: str, data: str) -> str:
    with open(path, "w") as file:
        file.write(data)
        file.close()

    return path


# [CALL] readFileSync
def readFileSync(path: str) -> str:
    file = open(path).read()
    return file


# [CALL] removeTree
def rmTree(path: str) -> int:
    shutil.rmtree(path)
    return 1


# [CALL] mkdirTree
def mkdirTree(path: str) -> int:
    Path(path).mkdir(parents=True, exist_ok=True)
    return 1
