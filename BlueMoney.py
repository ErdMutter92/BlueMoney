from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *
from notify import *
import sys, update, main, database, repair, firstrun

class run(QMainWindow):
    
    main = main.loopback()
    update = update.updater()
    debug = True

    appWidth = int('750')
    appHeight = int('350')
    lastSearch = ''
    searchIndex = 0
    lastSearchItem = ['']
    
    saved = Signal()
    
    def __init__(self):
        super(run, self).__init__()
        self.initUI()
        self.controls()

    def aboutUs(self):
        msgBox = QMessageBox.about(self, 'About Us', '<h1>'+self.main.clientConfig[0]+' '+self.main.clientConfig[1]+'</h1>A tool developed to help households manage their buget wisely and easly.<br><center>Build ID: <i>'+self.update.buildid()+'</i><br><br><small>Copyright 2014 bleauweb.net, all rights reserved!</small></center>')

    def readTable(self):
        return True
    
    def removeEntry(self):
        ok = QMessageBox.question(self, 'Remove Dialog', 'You sure you want to delete this row? It can\'t be undone!', QMessageBox.Yes, QMessageBox.Abort)
        if ok == QMessageBox.Yes:
            currentRow = self.tabWidget.currentWidget().currentRow()
            if int(currentRow) != int(-1):
                self.tabWidget.currentWidget().removeRow(currentRow)
        self.save()
        self.genCurrentTable()
    
    def addStartEntry(self):
        self.tabWidget.currentWidget().insertRow(0)
        self.save()
        self.genCurrentTable()
    
    def addEntry(self):
        rowCount = self.tabWidget.currentWidget().rowCount()
        self.tabWidget.currentWidget().insertRow(rowCount)
        self.save()
        self.genCurrentTable()

    def exitProgram(self):

        """
            Makes sure the user does not acidently close the application without saving.
        """
            
        tableTitle = self.tabWidget.tabText(self.tabWidget.currentIndex())
        database1 = database.csdv(tableTitle)
        
        if self.updateDB(self.tabWidget.currentIndex()) == database1.get() or not isinstance(self.tabWidget.currentWidget(), QTableWidget):
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

    def keyboardshortcuts(self):
        self.keyboardshortcutsWidget = QWebView()
        self.keyboardshortcutsWidget.load('http://localhost/update/clientfiles/data/resources/documents/help/Keyboard_Shortcuts.html')
        self.keyboardshortcutsWidget.show()
        self.keyboardshortcutsWidget.reload()
    
    def userActions(self):
        """
            Contains all the user actions for the Menubar and Toolbars
        """
        
        ## Actions to take when user requests to exit the program.
        self.exitAction = QAction(QIcon(''), 'Quit BlueMoney', self)
        self.exitAction.setShortcuts(['Ctrl+Q'])
        self.exitAction.setStatusTip("Exit the application...")
        self.exitAction.triggered.connect(self.exitProgram)
        self.exitAction.setIconVisibleInMenu(False)

        ## Action take take when user requests keyboard shortcut documentation.
        self.helpKeyboardShortcuts = QAction(QIcon(''), 'Keyboard Shortcuts', self)
        self.helpKeyboardShortcuts.setShortcuts(['Ctrl+shift+K'])
        self.helpKeyboardShortcuts.setStatusTip("Help documentation on keyboard shortcutss...")
        self.helpKeyboardShortcuts.triggered.connect(self.keyboardshortcuts)

        ## Action to take when user requests the about us popup
        self.aboutAction = QAction(QIcon(''), 'About BlueMoney', self)
        self.aboutAction.setShortcut('ctrl+alt+A')
        self.aboutAction.setStatusTip("More information about this application...")
        self.aboutAction.triggered.connect(self.aboutUs)


        ## Action to take when user requests to find an object
        self.findAction = QAction(QIcon(''), 'Find Entry', self)
        self.findAction.setShortcut('ctrl+F')
        self.findAction.triggered.connect(self.search)


        ## Action to take when user requests to submit feedback
        self.feedbackAction = QAction(QIcon(''), 'Submitt Feedback', self)
        self.updateAction.setShortcut('ctrl+shift+F')
        #self.updateAction.triggered.connect()


        ## Action to take when user requests to submit bug report
        self.bugreportAction = QAction(QIcon(''), 'Report Bug', self)
        self.bugreportAction.setShortcut('ctrl+shift+B')


        ## Action to take when user requests to submit suggestion
        self.fbrequestAction = QAction(QIcon(''), 'Feature Request', self)


        ## Action to take when user requests to save program data
        self.saveAction = QAction(QIcon(''), 'Save Entries...', self)
        self.saveAction.setShortcut('ctrl+S')
        self.saveAction.setStatusTip("Save entries into current document...")
        self.saveAction.triggered.connect(self.save)
    
    
        ## Action to take when user requests to add addition data entry
        self.addAction = QAction(QIcon(''), 'Add Entry...', self)
        self.addStartAction = QAction(QIcon(''), 'Add Top Entry...', self)
        
        self.addAction.setShortcuts(['ctrl+shift+A', 'ctrl+1'])
        
        self.addAction.setStatusTip("Add a database entry to current document...")
        self.addStartAction.setStatusTip("Add a database entry to top of current document...")
        
        self.addAction.triggered.connect(self.addEntry)
        self.addStartAction.triggered.connect(self.addStartEntry)
    
        self.addAction.setIconVisibleInMenu(False)
        self.addStartAction.setIconVisibleInMenu(False)
    
    
        ## Action to take when user requests to remove entry
        self.removeAction = QAction(QIcon(''), 'Remove Entry...', self)
        self.removeAction.setShortcuts(['ctrl+Backspace', 'ctrl+2', 'ctrl+R', 'fn+Delete'])
        self.removeAction.setStatusTip("Remove a database entry to current document...")
        self.removeAction.triggered.connect(self.removeEntry)
        self.removeAction.setIconVisibleInMenu(False)


        ## Action to take when user requests to update client
        self.updateAction = QAction(QIcon(''), 'Update Client', self)
        self.updateAction.setShortcut('ctrl+shift+U')
        #self.updateAction.triggered.connect(self.updateClient)
        
        ## Action to take when user requests to view bills page
        self.billsAction = QAction(QIcon(''), 'Switch to Bills', self)
        self.billsAction.setShortcut('Ctrl+2')
        self.billsAction.setStatusTip("Edit the Bills...")
        self.billsAction.triggered.connect(self.goToBills)
        
        
        ## Action to take when user requests to view bills page
        self.budgetAction = QAction(QIcon(''), 'Switch to Budget', self)
        self.budgetAction.setShortcut('Ctrl+1')
        self.budgetAction.setStatusTip("Edit the Budget...")
        self.budgetAction.triggered.connect(self.goToBudget)
        
        ## Action to take when user requests to view registry page
        self.registryAction = QAction(QIcon(''), 'Switch to Registry', self)
        self.registryAction.setShortcut('Ctrl+3')
        self.registryAction.setStatusTip("Edit the Check Registry...")
        self.registryAction.triggered.connect(self.goToRegistry)
        
        ## Action to take when user requests to view bills page
        self.recipiesAction = QAction(QIcon(''), 'Switch to Recipies', self)
        self.recipiesAction.setShortcut('Ctrl+4')
        self.recipiesAction.setStatusTip("Edit the Recipies...")
        self.recipiesAction.triggered.connect(self.goToRecipies)
        
        ## Action to take when user requests to view registry page
        self.itemsAction = QAction(QIcon(''), 'Switch to Items', self)
        self.itemsAction.setShortcut('Ctrl+5')
        self.itemsAction.setStatusTip("Edit the Items List...")
        self.itemsAction.triggered.connect(self.goToItems)


        ## Action to take when user requests to view registry page
        self.shoppingListAction = QAction(QIcon(''), 'Switch to Shopping List', self)
        self.shoppingListAction.setShortcut('Ctrl+6')
        self.shoppingListAction.setStatusTip("Switch to the shopping list tab...")
        self.shoppingListAction.triggered.connect(self.goToShoppingList)


    """
       Really need to find a better way to go between tabs then this.
       This work arround makes it so user can't move tabs around...
    """
    def goToBills(self):
        self.tabWidget.setCurrentWidget(self.tabWidget.widget(1))
    
    def goToBudget(self):
        self.tabWidget.setCurrentWidget(self.tabWidget.widget(0))

    def goToRegistry(self):
        self.tabWidget.setCurrentWidget(self.tabWidget.widget(2))

    def goToRecipies(self):
        self.tabWidget.setCurrentWidget(self.tabWidget.widget(3))
    
    def goToItems(self):
        self.tabWidget.setCurrentWidget(self.tabWidget.widget(4))
    
    def goToShoppingList(self):
        self.tabWidget.setCurrentWidget(self.tabWidget.widget(5))


    def genMenubar(self):
        """
            contains all the menubar items & code
        """
        self.menubar = QMenuBar()
    
        ## Files Menubar Items
        self.fileMenu = self.menubar.addMenu("&File")
        self.fileMenu.addSeparator()

        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.aboutAction)
        self.fileMenu.addAction(self.exitAction)


        ## Edit Menubar Items
        self.editMenu = self.menubar.addMenu("&Edit")
        self.editMenu_tabs = self.editMenu.addMenu("&Switch Tabs")
        self.editMenu.addSeparator()
        
        self.editMenu.addAction(self.findAction)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.addAction)
        self.editMenu.addAction(self.addStartAction)
        self.editMenu.addAction(self.removeAction)

        self.editMenu_tabs.addAction(self.budgetAction)
        self.editMenu_tabs.addAction(self.billsAction)
        self.editMenu_tabs.addAction(self.registryAction)
        self.editMenu_tabs.addAction(self.recipiesAction)
        self.editMenu_tabs.addAction(self.itemsAction)
        self.editMenu_tabs.addAction(self.shoppingListAction)


        ## Tools Menubar Items
        self.toolsMenu = self.menubar.addMenu("&Tools")

        self.toolsMenu.addAction(self.updateAction)
        self.toolsMenu.addSeparator()

        self.toolsMenu_feedback = self.toolsMenu.addMenu("Feedback and Reporting")
        self.toolsMenu_toolbars = self.toolsMenu.addMenu("Toolbars")
    
        self.toolsMenu_feedback.addAction(self.bugreportAction)
        self.toolsMenu_feedback.addAction(self.feedbackAction)
        self.toolsMenu_feedback.addAction(self.fbrequestAction)
    
        self.helpMenu = self.menubar.addMenu("&Help")
        self.helpMenu.addAction(self.helpKeyboardShortcuts)

    def genCurrentTable(self):
        tableTitle = self.tabWidget.tabText(self.tabWidget.currentIndex())
        database1 = database.csdv(tableTitle)
        db = database1.get()
    
        self.tabWidget.currentWidget().setColumnCount(int(len(db[0])))
        self.tabWidget.currentWidget().setRowCount(int(len(db[1:])))
    
        colCount = 0
        for item in db[1:]:
            rowCount = 0
            for items in item:
                itemsInput = QTableWidgetItem(str(items))
                self.tabWidget.currentWidget().setItem(colCount, rowCount, itemsInput)
                rowCount = rowCount+1
            colCount = colCount+1
    
        self.tabWidget.currentWidget().setHorizontalHeaderLabels(db[0])

    def genTable(self, tableID):
        
        ## return falsse if there is not widget at that id.
        if not self.tabWidget.widget(tableID):
            return False
        
        tableTitle = self.tabWidget.tabText(tableID)
        database1 = database.csdv(tableTitle)
        db = database1.get()
    
        self.tabWidget.widget(tableID).setColumnCount(int(len(db[0])))
        self.tabWidget.widget(tableID).setRowCount(int(len(db[1:])))
    
        colCount = 0
        for item in db[1:]:
            rowCount = 0
            for items in item:
                itemsInput = QTableWidgetItem(str(items))
                self.tabWidget.widget(tableID).setItem(colCount, rowCount, itemsInput)
                rowCount = rowCount+1
            colCount = colCount+1
    
        self.tabWidget.widget(tableID).setHorizontalHeaderLabels(db[0])

    def updateDB(self, tableID):
        ## return falsse if there is not widget at that id.
        if not self.tabWidget.widget(tableID) or not isinstance(self.tabWidget.currentWidget(), QTableWidget):
            return False
        
        tableTitle = self.tabWidget.tabText(tableID)
        database1 = database.csdv(tableTitle)
        db = database1.get()

        colCount = self.tabWidget.widget(tableID).columnCount()
        rowCount = self.tabWidget.widget(tableID).rowCount()
        constructList = []

        dbHeaders = db[0]
        for x in range(0, rowCount):
            constructInner = []
            for y in range(0, colCount):
                if isinstance(self.tabWidget.widget(tableID).item(x,y), type(None)):
                    constructInner.append('')
                else:
                    constructInner.append(self.tabWidget.widget(tableID).item(x,y).text())
            constructList.append(constructInner)
        constructList.insert(0, dbHeaders)
        return constructList

    def save(self):
        self.controls()
        if isinstance(self.tabWidget.currentWidget(), QTableWidget):
            self.saved.emit()
            tableTitle = self.tabWidget.tabText(self.tabWidget.currentIndex())
            database1 = database.csdv(tableTitle)
            db = database1.get()
            database1.saveOver(tableTitle, self.updateDB(self.tabWidget.currentIndex()))
            self.genCurrentTable()

    def search(self):
        '''
            Need to find a way for the search function to move items in the row
            to the next. without bugging out of course. :'(
            
            currently the search box works if the rows are
        '''
        ## List containing all items pertaining to the search in a [x,y] format.
        foundList = []
        
        ## Text entered into search box.
        searchBoxInput = self.searchBox.displayText()
        
        ## returns pointer to currently displayed widget.
        table = self.tabWidget.currentWidget()
        
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
            msgBox = QMessageBox.information(self, 'No Items Found', 'We were unable to find any items on this page with "'+searchBoxInput+'" in them.')
    
        return foundList
    
    def updateNotify(self):
        """
           Not yet fully implimented. Currently contains a bug that makes mac os x
           not able to see the app icon, need to fix this before implimenting.
        """
        updateNotify = notify('Update Notification', 'There is an update waiting for you!', 'BlueMoney Budget')
        updateNotify.push()

    def genToolbar(self):
        """
            contains all the toolbar elements and code
        """

        self.spacer = QWidget()
        self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.searchBox = QLineEdit()
        self.searchBox.setPlaceholderText('Search...')
        self.searchBox.setFixedWidth(200)
        self.searchBox.setTextMargins(20,0,20,0)
        self.searchBox.setStyleSheet("QLineEdit {  border: 1px solid gray;""border-radius: 10px;}");
        
        self.toolbar = self.addToolBar('Main Toolbar')
    
        self.toolbar.setFloatable(True)
        self.toolbar.setIconSize(QSize(20, 20))
        self.toolbar.setMovable(True)
        #self.toolbar.addAction(self.exitAction)
        #self.toolbar.addSeparator()
        self.toolbar.addAction(self.addAction)
        self.toolbar.addAction(self.removeAction)
        #self.toolbar.addAction(self.saveAction)
        #self.toolbar.addSeparator()
        #self.toolbar.addAction(self.billsAction)
        #self.toolbar.addAction(self.registryAction)
        self.toolbar.addWidget(self.spacer)
        self.toolbar.addWidget(self.searchBox)
    
    def debug(self):
        """
           function for testing code. Kept for future use.
        """
        return True
    
    def removeListItem(self):
        """
           Yet to be implimented.
        """
        return True
    
    def genSignal(self):
        """
            Contains all of the signals to keep track off
        """
        self.connect(self.tabWidget.widget(0), SIGNAL('itemSelectionChanged()'), self.save)
        self.connect(self.tabWidget.widget(1), SIGNAL('itemSelectionChanged()'), self.save)
        self.connect(self.searchBox, SIGNAL('returnPressed()'), self.search)
        self.connect(self.tabWidget, SIGNAL('currentChanged(int)'), self.controls)
        self.connect(self.spacer1, SIGNAL('itemSelectionChanged()'), self.debug)
        self.saved.connect(self.debug)
        return True


    def initUI(self):
        self.tabWidget = QTabWidget()
        self.tableBudget = QTableWidget()
        self.tabWidget.addTab(self.tableBudget, 'Budget')
        
        self.tableBills = QTableWidget()
        self.tabWidget.addTab(self.tableBills, 'Bills')
        
        self.tableRegistry = QTableWidget()
        self.tabWidget.addTab(self.tableRegistry, 'Registry')
        
        self.tableRecipies = QTableWidget()
        self.tabWidget.addTab(self.tableRecipies, 'Recipies')
        
        self.tableItems = QTableWidget()
        self.tabWidget.addTab(self.tableItems, 'Items')
        
        ## Contents for the Shopping List Tab
        self.listtitle = QLabel('Shopping List')
        self.shoppingspace = QWidget()
        self.editShoppingList = QWidget()
        self.spacer1 = QGridLayout(self.shoppingspace)
        self.spacer = QWidget()
        self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.editShoppingList.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.spacer1.setSpacing(10)
        self.shoppinglist = QListWidget()
        self.tabWidget.addTab(self.shoppingspace, 'Shopping List')
        self.spacer1.addWidget(self.listtitle, 0, 0)
        self.spacer1.addWidget(self.shoppinglist, 1, 0)
        self.spacer1.addWidget(self.editShoppingList, 1, 2)
        self.spacer1.addWidget(self.spacer, 2,0)
        self.shoppinglist.addItem('Lay\'s Wavy Hiskory BBQ Chips (x1)')
        self.shoppinglist.addItem('8Pack Gatorade Fruit Punch (x1)')
        
        self.tabWidget.setDocumentMode(True)

        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setMovable(False)

        self.userActions()
        self.genMenubar()
        self.genToolbar()
        
        self.taskbarmenu = QMenu()
        self.taskbarmenu.addAction(self.aboutAction)
        self.taskbarmenu.addSeparator()
        self.taskbarmenu.addAction(self.exitAction)
        self.taskbar = QSystemTrayIcon(self)
        self.taskbar.setIcon(QIcon('/data/resources/icons/32x32.png'))
        self.taskbar.setContextMenu(self.taskbarmenu)
        self.taskbar.show()
    
    
        #self.setGeometry(150, 200, 200, 300)
        
        ## use unified toolbar and title bar on mac os x
        self.setUnifiedTitleAndToolBarOnMac(True)
        self.genTable(0)
        self.genTable(1)
        self.genTable(2)
        self.genTable(3)
        self.genTable(4)
        
        
        
        self.windowBody =  QWidget(self)
        window = QVBoxLayout()
        window.setContentsMargins(0, 0, 0, 20)
        window.addWidget(self.tabWidget)
        self.windowBody.setLayout(window)
        self.statusBar().showMessage('Ready')
        
        self.show()

        self.genSignal()

    def controls(self):
        """
        Used to control element settings
        """
        if isinstance(self.tabWidget.currentWidget(), QTableWidget):
            self.addAction.setEnabled(True)
            self.addStartAction.setEnabled(True)
            if self.tabWidget.currentWidget().rowCount() == 0:
                self.removeAction.setEnabled(False)
            else:
                self.removeAction.setEnabled(True)
        else:
            self.removeAction.setEnabled(False)
            self.addAction.setEnabled(False)
            self.addStartAction.setEnabled(False)

    def resizeEvent(self, event):
        """
            runs this command while the window changes size
        """
        ## Detects if the application is running in unified
        ## mac toolbar with title on Mac OS X. To figure
        ## if the main table needs to be resized with or
        ## without a windowGap for the menues.
        if self.unifiedTitleAndToolBarOnMac():
            windowGap = 0
            self.windowWidth = self.width()
            self.windowHeight = self.height()
        else:
            windowGap = self.toolbar.height()-40
            self.windowWidth = self.width()
            self.windowHeight = self.height()-windowGap-40
        ## Resizes the window acording to the variables above.
        ## setGeometry(Top, Bottom, Width, Height)
        self.windowBody.setGeometry(0, windowGap, self.windowWidth, self.windowHeight)


def buildWindow():
    window = QApplication(sys.argv)
    BlueMoney = run()
    BlueMoney.resize(BlueMoney.appWidth, BlueMoney.appHeight)
    BlueMoney.setWindowTitle('Blue Money Budget')
    window.aboutToQuit.connect(BlueMoney.exitProgram)
    sys.exit(window.exec_())

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == 'cli':
            sys.argv.pop(1)
            main = main.loopback()
            main.run(sys.argv)
    buildWindow();