# -*- coding: utf-8 -*-
import os
import shutil
from pathlib import Path

from comint.__types import Unknown

# [CALL] writeFile
def writeFile(path: str, *, data: Unknown = ...,
to_file: Unknown = ...) -> Unknown:
    if os.name != 'nt':
        # tempfile for Posix [Linux or Mac]
        TEMP: str = f'.temp/{to_file}/'
    else:
        # tempfile for Windows
        TEMP: str = f'.temp\\{to_file}\\'
        
    Path(TEMP).mkdir(parents=True, exist_ok=True)
    _files: Path = Path(path)
    new_path: str = f'{TEMP}Main{_files.suffix}'
    new_data: bytes = bytes(data, 'utf-8')
    with open(new_path, 'wb') as file:
        file.write(new_data)
        file.close()
        
    return new_path
        
# [CALL] readFile
def readFile(path: str) -> Unknown:
    with open(path, 'rb') as file:
        _reader: str = file.read().decode()

    return _reader

# [CALL] rewriteFile
def rewriteFile(path: Unknown = ..., ext_file: Unknown = ...) -> Unknown:
    thisFile: tuple[str, str] = os.path.splitext(path)
    if path and ext_file != Ellipsis:
        if os.path.isfile(path):
            _xData: str = readFile(path)
            file_path = writeFile(path, data=_xData,
            to_file=ext_file)
            
            return file_path
