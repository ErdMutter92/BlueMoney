'''
    Title: Blue Money Updater
    Author: Alexis Matthew Bleau <alexis@bleauweb.net>
    
    Copyright 2014 Alexis Bleau. All rights reserved.
    
    Discription: Checks client files agenst files on the server,
    before updating it makes sure that that scripts are runable
    and match the files on the server.
    '''
from urllib import *
import hashlib, subprocess, sys, os, main

class updater:
    
    firstMD5 = ''
    
    main = main.loopback()
    
    updateConfig = ['Blue Money Updater', main.clientConfig[1], 'http://localhost/update/']
    
    def buildid(self):
        """
            Takes the contents of all critical files and returns a master md5sum
            """
        fileMD5 = hashlib.md5('')
        ## Passes the url argument to be opened by urlib
        serverIndex = open('./data/resources/repair.index.html', 'r+')
        ## reads the opened urllib object, strips out any new line characitors
        ## and decodes it back into readable text (default: utf-8)
        serverIndex = serverIndex.read().rstrip().decode('utf-8').split('<br />')
        serverIndex.pop(-1)
        for file in serverIndex:
            contents = open(file, 'r+')
            for line in contents:
                fileMD5.update(line.encode())
        return fileMD5.hexdigest()
    
    def client(self, decode = 'utf-8'):
        '''
            Downloads the index of what files should be present on the
            client side, and then checks to make sure each file in the
            index are up to date. If they are not up to date, download
            the updated file and check to make sure it runs.
            '''
        ## Passes the url argument to be opened by urlib
        serverIndex = urlopen(self.updateConfig[2]+'index.php?update')
        ## reads the opened urllib object, strips out any new line characitors
        ## and decodes it back into readable text (default: utf-8)
        serverIndex = serverIndex.read().rstrip().decode(decode).split('<br />')
        ## BUGWORKAROUND: Removes last entry on list, as it is currently is blank.
        serverIndex.pop(-1)
        returnList = []
        returnList.append(serverIndex)
        print u'Running client side update...'
        for file in serverIndex:
            print 'Attempting to update '+file+' ... ',; sys.stdout.write('')
            if self.file(file):
                print 'sucsess!'
                returnList.append('sucess')
            else:
                ## checks to see if the md5s match before continuing...
                if self.check(file):
                    print 'no need!'
                    returnList.append('sucess')
                else:
                    print 'failed!'
                    returnStr = 'failed'
                    returnList.append('failed')
        print('Client side updater has finished...')
        return returnList
    
    def runCheck(self, fileName):
        '''
            Temp workaround until runCheck can be rewritten
            '''
        return True
    
    def file(self, fileName):
        '''
            Checks local file's md5 agenst server file's md5 to make sure they
            match before downloading the updated file. Before installing that
            file it passes it through runCheck to make sure it's executable.
            '''
        ## checks to see if the md5s match before continuing...
        if self.check(fileName):
            return False
        else:
            ## Downloads the file to update as a temp file.
            urlretrieve(self.updateConfig[2]+'/clientfiles/'+fileName, 'tmp.'+fileName)
            if (self.runCheck('tmp.'+fileName)):
                ## if downloaded file is capible of running without reutrning an error
                ## remove the old file and replace it with the new updated version.
                os.remove(fileName)
                os.rename('tmp.'+fileName, fileName)
                return True
            else:
                ## if run check fails, remove the failed updated file.
                os.remove('tmp.'+fileName)
                return False
    
    def md5sum(self, contents):
        '''
            Takes the contents and feeds it through hashlib to generate
            a md5. Returns a md5 hash.
            '''
        self.fileMD5 = hashlib.md5('')
        
        ## reads through the content one line at a time encoding it
        ## and feeding it into the md5 object.
        for line in open(contents, 'r+'):
            self.fileMD5.update(line.encode())
        return self.fileMD5.hexdigest()
    
    def check(self, fileName):
        """
            checks to see if the MD5 provided is the same of that found
            on the server.
            """
        ## Passes the url argument to be opened by urlib
        serverFile = urlopen(self.updateConfig[2]+'md5.php?file='+fileName)
        self.firstMD5 = self.md5sum('./'+fileName)
        ## reads the opened urllib object, strips out any new line characitors
        ## and decodes it back into readable text (default: utf-8)
        webMD5 = serverFile.read().rstrip().decode('utf-8')
        return self.checksums(self.firstMD5, webMD5)
    
    def checksums(self, firstMD5, secondMD5):
        '''
            Does a simple check to make sure the md5s provided are qaulified,
            and then matches them togeather. If matches return true. If not
            matching or if not qualitified return false.
            '''
        ## checks to make sure the two md5sums are the same length
        if len(firstMD5) == len(secondMD5):
            ## checks to make sure the md5sums are the same.
            if firstMD5 == secondMD5:
                return True
            else:
                return False
        else:
            return False

#if __name__ == '__main__':
#    update = updater()
#    update.client()