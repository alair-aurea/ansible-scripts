from __future__ import unicode_literals
from os import walk
import inquirer
import constants

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
            while(True):
                filename = inquirer.prompt([
                        inquirer.List('files',
                            message=self.message,
                            choices=self.getFilenames(),
                        ),
                    ])['files']
              
                correct = inquirer.prompt([
                        inquirer.Confirm('confirmation',
                            message=constants.CONFIRM_FILE_SELECTION_TEXT + " '" + filename + "'",
                            default=True,
                        ),
                    ])['confirmation']
                if ( correct ):
                    return filename
                else:
                    print
            
        else:
            return None
