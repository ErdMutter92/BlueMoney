'''
    Title: Blue Money Repair Tool
    Author: Alexis Matthew Bleau <alexis@bleauweb.net>
    
    Copyright 2014 Alexis Bleau. All rights reserved.
    
    Discription: A self contained script that only relies on default
    python modules to carry out it's task of repairing the client back
    to fresh ("factory settings") install status. If during the repair 
    an error is detected this script automaticly generates a bug report 
    and attempts to submit it to the website. The report is cached in a 
    file on the client computer for later sending if no respownse if 
    heared from the server. Downloads and installs a fresh copy of the 
    client side program. Wipes all data, and is not ment to be used as 
    an updater.
'''
from urllib2 import *
import os, base64, hashlib, sys, textwrap

class repair:
    
    ## List containing all repair tool's main strings. Later to be managed by
    ## multi-language tools.
    clientStrings = ['Blue Money Bugdet Repair Tool', '0.0.4', './data/backup']
    ## List containing all essental directories, filetypes, and file names
    index = [['', 'py', 'BlueMoney', 'main', 'database', 'repair', 'notify', 'update', 'error'],['data/', 'csdv', 'bills', 'registry', 'items', 'recipies', 'budget'],['data/resources/']]

    ## class data storage variables
    _fileName = ''
    _fileBlob = ''
    _fileData = []
    
    def repair(self, ui = None):
        ## Client Side Warning
        print self.clientStrings[0]+' '+self.clientStrings[1]+'\n'
        for lines in textwrap.wrap('WARNING: Use this tool as a last resort, because by running this script you are going to wipe out all the settings and data assosated with this program, and return them to the last backed up copy, normally the only backup file generated is the one on first run. This process is not reversible, and any new DATA WILL BE LOST. If you are experiencing a bug, please consider filing a bug report. Additionally if you are looking for a feature, consider submitting a feature request or some feedback. '):
            print(lines)
        
        ## Checks to make sure user wants to go through with repair
        if ui != True:
            ui = raw_input('\nDo you wish to continue? [yes/no]: ')
            ui = ui.lower()
            if ui == 'yes':
                ui = True
                print '' ## non-arbritrary blank line after user respawnse
            else:
                print('\nAborting Repair, invalid user input.')
                ui = False
        else:
            print ''  ## non-arbritrary blank line after warning message

        if ui == True:
            files = []
            ## generates a list of all important file paths
            for data in self.index:
                numOfFiles = len(data)
                for number in range(2, numOfFiles):
                    files.append('/'+data[0]+''+data[number]+'.'+data[1])

            ## Creat a work directly to do some work in.
            if not os.path.exists('./work'):
                os.mkdir('./work')

            ## Checks to see if fies are there, if not create file from backup
            for file in files:
                ## always removes and restores database files.
                if file.split('.')[-1] == 'csdv':
                    if os.path.exists('.'+file):
                        os.remove('.'+file)

                if not os.path.exists('.'+file):
                    print('Restoring '+file+' from backup...')
                    self.genFile(['.'+file, open(self.clientStrings[2]+file+'.backup', 'r').read()])


            ## Remove the work directory as it should no longer be needed.
            if os.path.exists('./work'):
                os.rmdir('./work')
    
    def backup(self):
        files = []
        ## Construct list containing all important file paths
        for data in self.index:
            numOfFiles = len(data)
            for number in range(2, numOfFiles):
                files.append('/'+data[0]+''+data[number]+'.'+data[1])
    
        print('Creating Application Backup')
        for file in files:
            ## Removes all old backup files is there are any.
            if os.path.exists(self.clientStrings[2]+file+'.backup'):
                os.remove(self.clientStrings[2]+file+'.backup')
            
            ## set up enviroment to create backup files
            if self.setBlob(file):
                sys.stdout.write('Creating backup of '+file+' ')
                if self.saveBlob(file):
                    print('... done!')
                else:
                    print('... failed!')
            else:
                print('backup failed')


    def __init__(self, function = None, ui = None):
        if function == None:
            self.repair(ui)
        elif function.lower() == 'backup':
            self.backup()
        elif function.lower() == 'repair':
            self.repair(ui)
        elif function.lower() == 'blank':
            print('Repair functionality is now at your fingertips...')
        else:
            print('ERROR: Unknown User Input, '+function+'.')

    def getBlob(self):
        return self._fileBlob

    def genFile(self, fileData):
        with open(fileData[0], 'wb') as file:
            file.write(base64.b64decode(fileData[1]))

    def getData(self):
        return self._fileData

    def saveBlob(self, fileName):
        file = open(self.clientStrings[2]+'/'+self._fileName+'.backup', 'w')
        file.write(self._fileBlob)
        return True
    
    def _openBlob(self):
        self._fileBlob = open(self.clientStrings[2]+'/'+self._fileName+'.backup', 'r').read()
        return True

    def setBlob(self, fileName):
        self._fileName = '.'+fileName
        file = open(self._fileName+'', 'rb').read()
        self._fileBlob = base64.b64encode(file)
        return True


