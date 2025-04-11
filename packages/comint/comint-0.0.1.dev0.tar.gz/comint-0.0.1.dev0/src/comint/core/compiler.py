# -*- coding: utf-8 -*-
import os
import subprocess
import os.path as path

from comint.__types import Unknown
from comint.fs import writeFile
from comint.fs import rewriteFile

# Define
EXT2STR: dict[str, str] = {
    '.cpp':'cpp',
    '.c':'cpp',
    '.go':'go',
    '.rs':'rust',
    '.dart':'dart',
}
STR2EXT: dict[str, str] = {
    'cpp':'.cpp',
    'c':'.c',
    'go':'.go',
    'rust':'.rs',
    'dart':'.dart',
}


class Compiler:
    
    def __init__(self, resource: Unknown,
    lang: Unknown = None) -> Unknown:
        """
        
        :param resource: source of file or str
        :param lang: programming language to be used
        :return str:
        """
        self.__resouce: Unknown = resource
        self.__language: str = lang
        self.__file: tuple[str, str] = path.splitext(self.__resouce)
        
    def __repr__(self):
        _exec_repr: callable = self.filterize()
        lang_filtered: str = ''
        output: bytes = _exec_repr.stdout
        error: bytes = _exec_repr.stderr
        
        return f"ComintCompiler(Language=\
b'{lang_filtered}', \
Output={output})"
    
    def filterize(self) -> Unknown:
        global EXT2STR
            
        # Validated Files
        if path.isfile(self.__resouce):
            # Rewrite to tempfile
            file_path: str = rewriteFile(self.__resouce,
                ext_file=EXT2STR[self.__file[1]])
            # Execution File to Compile
            return self.compilex(file_path)
        else:
            code_string: str = self.__resouce
            try:
                new_file_string: str = writeFile(f'.temp/{self.__language}/Main{STR2EXT[self.__language]}',
                data=code_string,
                to_file=self.__language)
                return self.compilex(new_file_string)
            except KeyError:
                print(f'Comint: Sorry, lang="{self.__language}" is not included in the compilation category.')
    
    def compilex(self, resource: Unknown) -> str:
        """compilex, is the main function to perform compilation
        which will be processed either through string or file
        
        Args:
            :param resource: source of string or file
        
        Return:
            Output string comint processed
        """
        global STR2EXT
        new_exec: path = path.splitext(resource)
        if self.__language != None:
            match STR2EXT[self.__language]:
                case ".c":
                    os.system(f'gcc {resource} -o {new_exec[0]}')
                    _proc: callable = subprocess.run(f'./{new_exec[0]}',
                    stdout = subprocess.PIPE,
                    stderr = subprocess.PIPE)
                    return _proc
                case ".cpp":
                    os.system(f'g++ {resource} -o {new_exec[0]}')
                    _proc: callable = subprocess.run(f'./{new_exec[0]}',
                    stdout = subprocess.PIPE,
                    stderr = subprocess.PIPE)
                    return _proc
                    os.system(f'rm ./{new_exec[0]}')
                case ".go":
                    os.system(f'go build {resource}')
                    _proc: callable = subprocess.run(f'./Main',
                    stdout = subprocess.PIPE,
                    stderr = subprocess.PIPE)
                    return _proc
                    os.system(f'rm ./Main')
                case _:
                    print('Error')
        else:
            match new_exec[1]:
                case ".c":
                    os.system(f'gcc {resource} -o {new_exec[0]}')
                    _proc: callable = subprocess.run(f'./{new_exec[0]}',
                    stdout = subprocess.PIPE,
                    stderr = subprocess.PIPE)
                    return _proc
                case ".cpp":
                    os.system(f'g++ {resource} -o {new_exec[0]}')
                    _proc: callable = subprocess.run(f'./{new_exec[0]}',
                    stdout = subprocess.PIPE,
                    stderr = subprocess.PIPE)
                    return _proc
                    os.system(f'rm ./{new_exec[0]}')
                case ".go":
                    os.system(f'go build {resource}')
                    _proc: callable = subprocess.run(f'./Main',
                    stdout = subprocess.PIPE,
                    stderr = subprocess.PIPE)
                    os.system(f'rm ./Main')
                    return _proc
                case _:
                    print('Error')

if __name__ == '__main__':
    Xcode: str = """
package main

import "fmt"

func main() {
    fmt.Println("Hello Comint Indonesia!")
}

    """
    x = Compiler("example.go")
    x = Compiler(Xcode, lang='go')
    print(x)