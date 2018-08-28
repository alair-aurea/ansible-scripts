from __future__ import unicode_literals
from prompt_toolkit import prompt
from os import walk
import inquirer

class FileSelector():
    def __init__( self, filesDir, extensions, message  ):
        self.filesDir = filesDir
        self.message = message
        self.extensions = extensions
            
    def getFilenames( self ):
        filenames = []
        for ( dirpath, dirnames, filenames ) in walk(self.filesDir):
            filenames = [ fi for fi in filenames if fi.endswith( self.extensions ) ]
            break
        return filenames

    def select( self ):
        filenames = self.getFilenames()
        
        if filenames:
            questions = [
                inquirer.List('files',
                      message=self.message,
                      choices=self.getFilenames(),
                  ),
            ]
            return inquirer.prompt(questions)['files']
            
        else:
            return None
