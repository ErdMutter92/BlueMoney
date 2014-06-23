"""
    Author: Alexis M. Bleau <alexis@bleauweb.net>
    Title: Blue Money Comma Seperated Data Values ("csdv")
    
    Copyright 2014 by Alexis M. Bleau, All Rights Reserved!
    
    Discription: All the tools needed to deal with the
    csdv file type, and the data heald within.
    
"""
import os, csv

class csdv:

    dbList = []
    
    def __init__(self, fileName):
        self.read(fileName)
    
    def getHeaders(self):
        """
            Writes a list to a csdv file
        """
        return self.dbList[0]
    
    def write(self, fileName, dataList):
        """
            Writes a list to a csdv file
            """
        fileName = './data/'+fileName+'.csdv'
        fileExists = os.path.exists(fileName)
        ## Checks to make sure the dataList provided is of the list type.
        if isinstance(dataList, list):
            ## checks to make sure the file exists before continuing.
            if fileExists:
                ## reading the file to get the headers.
                with open(fileName) as csvfile:
                    filereader = csv.reader(csvfile, delimiter='\t', quotechar='|')
                    fileheader = []
                    for row in filereader:
                        fileheader.append(row)
                        #breaks after first loop, only need headers from first line.
                        break
                
                ## opening the file in append mode to make additions.
                with open(fileName, 'a') as csvfile:
                    filewriter = csv.writer(csvfile, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    if len(fileheader[0]) == len(dataList):
                            filewriter.writerow(dataList)
                    else:
                        print('Inacurate user input, please try using a list structured like: '+str(fileheader[0]))
            else:
                return False
        else:
            return False

    def saveOver(self, fileName, dataList):
        """
            Writes a list to a csdv file
        """
        fileName = './data/'+fileName+'.csdv'
        fileExists = os.path.exists(fileName)
        ## Checks to make sure the dataList provided is of the list type.
        if isinstance(dataList, list):
            ## checks to make sure the file exists before continuing.
            if fileExists:
                ## reading the file to get the headers.
                with open(fileName) as csvfile:
                    filereader = csv.reader(csvfile, delimiter='\t', quotechar='|')
                    fileheader = []
                    for row in filereader:
                        fileheader.append(row)
                        #breaks after first loop, only need headers from first line.
                        break
            
                ## opening the file in append mode to make additions.
                with open(fileName, 'w') as csvfile:
                    filewriter = csv.writer(csvfile, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    if len(fileheader[0]) == len(dataList[-1]):
                        for data in dataList:
                            filewriter.writerow(data)
                    else:
                        print('Inacurate user input, please try using a list structured like: '+str(fileheader[0]))
            else:
                return False
        else:
            return False


    def remove(self, index):
        """
            used to remove entires from the cached database file
        """
        ## checks to see if index is of the int type, if so use pop
        if isinstance(index, int):
            self.dbList.pop(index)
        ## checks to see if index is of the int type, if so use remove
        elif isinstance(index, str):
            self.dbList.remove(index)
        ## when not sure what the $^@% the user typed, return false.
        else:
            return False

    def read(self, fileName = '', verbose = True):
        """
            this opearation is overloaded. If fileNmae is not send to blank
            then it will read in the database file and convert it to a list.
            Otherwise it will print out the database file to console as well
            as retrun it. Esentally doing the same thing as the get function.
        """
        if fileName != '':
            fileName = './data/'+fileName+'.csdv'
            returnList = []
            if os.path.exists(fileName):
                with open(fileName) as csvfile:
                    filereader = csv.reader(csvfile, delimiter='\t', quotechar='|')
                    for row in filereader:
                        returnList.append('\t '.join(row).split('\t '))
                    self.dbList = returnList
            return returnList
        else:
            for item in self.get():
                if verbose: print('\t '.join(item));
            return self.dbList

    def get(self):
        return self.dbList

    def set(self, database):
        self.dbList = database

    def add(self, values):
        self.dbList.append(values)

