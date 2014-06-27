from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtWebKit import *
import sys
import database
import main
import update

class Control:

    lastSearch = ''
    main = main.loopback()
    update = update.updater()
    
    def __init__(self, ref):
        self.view = ref
        
    def aboutUs(self):
        msgBox = QMessageBox.about(self.view, 'About Us', '<h1>'+self.main.clientConfig[0]+' '+self.main.clientConfig[1]+'</h1>A tool developed to help households manage their buget wisely and easly.<br><center>Build ID: <i>'+self.update.buildid()+'</i><br><br><small>Copyright 2014 bleauweb.net, all rights reserved!</small></center>')
        
    def exit(self):

        """
            Makes sure the user does not acidently close the application without saving.
        """
            
        tableTitle = self.view.tabWidget.tabText(self.view.tabWidget.currentIndex())
        database1 = database.csdv(tableTitle)
        
        if self.updateDB(self.view.tabWidget.currentIndex()) == database1.get() or not isinstance(self.view.tabWidget.currentWidget(), QTableWidget):
            sys.exit()
     
        msgBox = QMessageBox()
        msgBox.setText("The document has been modified.")
        msgBox.setInformativeText("Do you want to save your changes?")
        msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Save)
        ret = msgBox.exec_()
        if ret == QMessageBox.Save:
            sys.exit()
        elif ret == QMessageBox.Cancel:
            print('aborting close...')
        elif ret == QMessageBox.Discard:
            sys.exit()
        else:
            sys.exit()
        
    def save(self):
        self.controls()
        if isinstance(self.view.tabWidget.currentWidget(), QTableWidget):
            tableTitle = self.view.tabWidget.tabText(self.view.tabWidget.currentIndex())
            database1 = database.csdv(tableTitle)
            db = database1.get()
            database1.saveOver(tableTitle, self.updateDB(self.view.tabWidget.currentIndex()))
            self.generate()
    
    def search(self):
        '''
            Need to find a way for the search function to move items in the row
            to the next. without bugging out of course. :'(
            
            currently the search box works if the rows are
        '''
        ## List containing all items pertaining to the search in a [x,y] format.
        foundList = []
        
        ## Text entered into search box.
        searchBoxInput = self.view.searchBox.displayText()
        
        ## returns pointer to currently displayed widget.
        table = self.view.tabWidget.currentWidget()
        
        for itemFound in table.findItems(searchBoxInput, Qt.MatchContains):
            tmpList = []
        
            tmpList.append(itemFound.row())
            tmpList.append(itemFound.column())
            if itemFound.text() == self.lastSearch:
                ## this seems to be where I am having issues when it comes
                ## to going to the next item in the table. I'm trying to get
                ## it to go to the next column before going to the next row
                ## starting from the column 1 row 1, and working it's way
                ## through the currently displayed table.
                if (int(itemFound.row()) >= int(table.currentRow()) or (int(itemFound.column()) == int(table.currentColumn()) and int(itemFound.row()) <= int(table.currentRow()) )):
                    ## true if the item currently select is not the one found.
                    if tmpList != [table.currentRow(), table.currentColumn()]:
                        foundList.append(tmpList)
    
            else:
                self.lastSearch = searchBoxInput
                foundList.append(tmpList)
    
        if len(foundList) > 0:
            table.setCurrentCell(foundList[0][0], foundList[0][1])
        else:
            ## popup error if no items found.
            msgBox = QMessageBox.information(self.view, 'No Items Found', 'We were unable to find any items on this page with "'+searchBoxInput+'" in them.')
    
        return foundList
    
    def add(self):
        rowCount = self.view.tabWidget.currentWidget().rowCount()
        self.view.tabWidget.currentWidget().insertRow(rowCount)
        self.save()
        self.generate()
    
    def addTop(self):
        self.view.tabWidget.currentWidget().insertRow(0)
        self.save()
        self.generate()
    
    def remove(self):
        ok = QMessageBox.question(self.view, 'Remove Dialog', 'You sure you want to delete this row? It can\'t be undone!', QMessageBox.Yes, QMessageBox.Abort)
        if ok == QMessageBox.Yes:
            currentRow = self.view.tabWidget.currentWidget().currentRow()
            if int(currentRow) != int(-1):
                self.view.tabWidget.currentWidget().removeRow(currentRow)
        self.save()
        self.generate()
        
    def controls(self):
        """
        Used to control element settings
        """
        tableID = self.view.tabWidget.tabText(self.view.tabWidget.currentIndex())
        if isinstance(self.view.tabWidget.currentWidget(), QTableWidget):
            self.view.addAction.setEnabled(True)
            if self.view.tabWidget.currentWidget().rowCount() == 0:
                self.view.removeAction.setEnabled(False)
            else:
                self.view.removeAction.setEnabled(True)
        else:
            self.view.removeAction.setEnabled(False)
            self.view.addAction.setEnabled(False)
            
    def updateDB(self, tableID):
        ## return falsse if there is not widget at that id.
        if not self.view.tabWidget.widget(tableID) or not isinstance(self.view.tabWidget.currentWidget(), QTableWidget):
            return False
        
        tableTitle = self.view.tabWidget.tabText(tableID)
        database1 = database.csdv(tableTitle)
        db = database1.get()

        colCount = self.view.tabWidget.widget(tableID).columnCount()
        rowCount = self.view.tabWidget.widget(tableID).rowCount()
        constructList = []

        dbHeaders = db[0]
        for x in range(0, rowCount):
            constructInner = []
            for y in range(0, colCount):
                if isinstance(self.view.tabWidget.widget(tableID).item(x,y), type(None)):
                    constructInner.append('')
                else:
                    constructInner.append(self.view.tabWidget.widget(tableID).item(x,y).text())
            constructList.append(constructInner)
        constructList.insert(0, dbHeaders)
        return constructList

    def generate(self):
        tableName = self.view.tabWidget.tabText(self.view.tabWidget.currentIndex())
        tableID = self.view.tabWidget.currentIndex()
        if tableName == 'Registry':
            ## return falsse if there is not widget at that id.
            if not self.view.tabWidget.widget(tableID):
                return False
            
            tableTitle = self.view.tabWidget.tabText(tableID)
            database1 = database.csdv(tableTitle)
            db = database1.get()
            
            self.view.tabWidget.widget(tableID).setColumnCount(int(len(db[0])))
            self.view.tabWidget.widget(tableID).setRowCount(int(len(db[1:])))
            
            colCount = 0
            lastBalance = '0'
            for item in db[1:]:
                rowCount = 0
                payment = '0'
                deposit = '0'
                for items in item:
                    itemsInput = QTableWidgetItem(str(items))
                    if rowCount == 3:
                        payment = str(items)
                        if payment == None or payment == '':
                            payment = str(0)
                    if rowCount == 4:
                        deposit = str(items)
                        if deposit == None or deposit == '':
                            deposit = str(0)
                    if rowCount == 5:
                        lastBalance = str(float(float(deposit)-abs(float(payment))+float(lastBalance)))
                        item = QTableWidgetItem(str(lastBalance))
                        ## Item is no longer editable by user.
                        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        self.view.tabWidget.widget(tableID).setItem(colCount, rowCount, item)
                    else:
                        self.view.tabWidget.widget(tableID).setItem(colCount, rowCount, itemsInput)
                    rowCount = rowCount+1
                colCount = colCount+1
            
            self.view.tabWidget.widget(tableID).setHorizontalHeaderLabels(db[0])
            self.controls()
        else:
            self.genCurrentTable()

    def genCurrentTable(self):
        tableTitle = self.view.tabWidget.tabText(self.view.tabWidget.currentIndex())
        database1 = database.csdv(tableTitle)
        db = database1.get()
    
        self.view.tabWidget.currentWidget().setColumnCount(int(len(db[0])))
        self.view.tabWidget.currentWidget().setRowCount(int(len(db[1:])))
    
        colCount = 0
        for item in db[1:]:
            rowCount = 0
            for items in item:
                itemsInput = QTableWidgetItem(str(items))
                self.view.tabWidget.currentWidget().setItem(colCount, rowCount, itemsInput)
                rowCount = rowCount+1
            colCount = colCount+1
    
        self.view.tabWidget.currentWidget().setHorizontalHeaderLabels(db[0])
    
    def calcRow(self, ref):
        return True
    
    def debug(self):
        print('debugging')
    
    def genTable(self, tableID):
        
        ## return falsse if there is not widget at that id.
        if not self.view.tabWidget.widget(tableID):
            return False
        
        tableTitle = self.view.tabWidget.tabText(tableID)
        database1 = database.csdv(tableTitle)
        db = database1.get()
    
        self.view.tabWidget.widget(tableID).setColumnCount(int(len(db[0])))
        self.view.tabWidget.widget(tableID).setRowCount(int(len(db[1:])))
    
        colCount = 0
        for item in db[1:]:
            rowCount = 0
            for items in item:
                itemsInput = QTableWidgetItem(str(items))
                self.view.tabWidget.widget(tableID).setItem(colCount, rowCount, itemsInput)
                rowCount = rowCount+1
            colCount = colCount+1
    
        self.view.tabWidget.widget(tableID).setHorizontalHeaderLabels(db[0])
        self.controls()