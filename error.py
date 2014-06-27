"""
    Upon unexpected failure generates a bug report for client 
    to submit online
"""
from urllib import *
import os, base64, time

class report():
    
    clientFiles = []
    fileBlobs = []

    def __init__(self, capturedException, e):
        self.genReport(capturedException, e)
        print('Error Report Generated')
    
    def genReport(self, capturedException, e):
        self.fileBlobs = self.encode(self.walkClient())
        self.log(self.genFileBlobPair(self.clientFiles, self.fileBlobs), capturedException, e)

    def walkClient(self, startDir = '.'):
        for file in os.listdir(startDir):
            if file[-2:] == 'py':
                self.clientFiles.append(file)
        return self.clientFiles

    def encode(self, fileList):
        tmpBlob = []
        for file in fileList:
            myfile = open(file, 'rb').read()
            myfile = base64.b64encode(myfile)
            tmpBlob.append(myfile)
        return tmpBlob

    def genFileBlobPair(self, clientFiles, fileBlobs):
        report = []
        for i in range(0, len(self.clientFiles)):
            report.append([clientFiles[i], fileBlobs[i]])
        return report

    def log(self, generatedBlobsPair, capturedException, e):
        id = time.time()
        if not os.path.exists('./data/crash/'):
            os.mkdir('./data/crash/')
        logfile = open('./data/crash/'+str(id)+'_crash_data.bmcr', 'a')
        logfile.write(capturedException+'\t'+str(e)+'\n')
        for group in generatedBlobsPair:
            logfile.write(group[0]+'\t'+group[1]+'\n')
