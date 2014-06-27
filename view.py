from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtWebKit import *
import sys
import control

class View:
    
    def __init__(self):
        app = QApplication(sys.argv)
        main = Window()
        main.setWindowTitle('Blue Money Budget')
        sys.exit(app.exec_()) 
        
class Window(QMainWindow):
    """
        The main window of the application.
    """
    appWidth = int('750')
    appHeight = int('350')
    
    def getWindow(self):
        """
            returns the a pointer to the window's object
        """
        return self
    
    def __init__(self):
        self.core = control.Control(self.getWindow())
        super(Window, self).__init__()
        self.setUnifiedTitleAndToolBarOnMac(True)
        self.actions()
        self.toolBar()
        self.menubar()
        self.initUI()
        self.genSignal()
        self.setGeometry(150, 200, 800, 400)
        
        self.core.genTable(0)
        self.core.genTable(1)
        self.core.genSelectTable(self.tableRegistry, 2)
        self.core.genTable(3)
        self.core.genTable(4)
        
        
    def actions(self):
        self.exitAction = QAction(QIcon(''), 'Quit Program', self)
        self.exitAction.setShortcuts(['Ctrl+Q'])
        self.exitAction.triggered.connect(self.core.exit)
        self.exitAction.setIconVisibleInMenu(False)

        self.addAction = QAction(QIcon(''), 'Add Entry', self)
        self.addAction.setShortcuts(['Ctrl+A'])
        self.addAction.triggered.connect(self.core.add)
        self.addAction.setIconVisibleInMenu(False)

        self.removeAction = QAction(QIcon(''), 'Remove Entry', self)
        self.removeAction.setShortcuts(['Ctrl+R'])
        self.removeAction.triggered.connect(self.core.remove)
        self.removeAction.setIconVisibleInMenu(False)

        self.saveAction = QAction(QIcon(''), 'Save', self)
        self.saveAction.setShortcuts(['Ctrl+S'])
        self.saveAction.triggered.connect(self.core.save)
        self.saveAction.setIconVisibleInMenu(False)

        self.keyboardHelpAction = QAction(QIcon(''), 'Keyboard Shortcuts', self)
        self.keyboardHelpAction.setShortcuts(['Ctrl+shift+K'])
        self.keyboardHelpAction.triggered.connect(self.keyboardshortcuts)
        self.keyboardHelpAction.setIconVisibleInMenu(False)

        self.aboutUsAction = QAction(QIcon(''), 'About Us', self)
        self.aboutUsAction.setShortcuts(['Ctrl+shift+I'])
        self.aboutUsAction.triggered.connect(self.core.aboutUs)
        self.aboutUsAction.setIconVisibleInMenu(False)
        
    def toolBar(self):
        ## Horizontal & Vertical Spacer
        self.spacer = QWidget()
        self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        ## Search Box
        self.searchBox = QLineEdit()
        self.searchBox.setPlaceholderText('Search...')
        self.searchBox.setFixedWidth(200)
        self.searchBox.setTextMargins(20, 0, 20, 0)
        self.searchBox.setStyleSheet("QLineEdit {  border: 1px solid gray;""border-radius: 10px;}");
        
        self.toolbar = self.addToolBar('Main Toolbar')

        self.toolbar.addAction(self.addAction)
        self.toolbar.addAction(self.removeAction)
        
        self.toolbar.addWidget(self.spacer)
        self.toolbar.addWidget(self.searchBox)
        
    def menubar(self):
        self.menubar = QMenuBar()
        
        self.fileMenu = self.menubar.addMenu("&File")
        #self.fileMenu.addSeparator()
        
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.aboutUsAction)
        self.fileMenu.addAction(self.exitAction)
        
    def initUI(self):
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setDocumentMode(True)
        
        self.tableBudget = QTableWidget()
        self.tabWidget.addTab(self.tableBudget, 'Budget')
        
        self.billsWidget = QTableWidget()
        self.tabWidget.addTab(self.billsWidget, 'Bills')
        
        self.registryLayout = QVBoxLayout()
        self.tableRegistry = QTableWidget()
        self.registryWidget = QWidget()
        self.registryLayout.setSpacing(0)
        self.registryLayout.setContentsMargins(QMargins(0,0,0,0))
        self.test = QTableWidget()
        self.registryLayout.addWidget(self.tableRegistry, 0, 0)
        self.registryLayout.addWidget(self.test, 1, 0)
        self.registryWidget.setLayout(self.registryLayout)
        self.tabWidget.addTab(self.registryWidget, 'Registry')
        
        self.tableRecipies = QTableWidget()
        self.tabWidget.addTab(self.tableRecipies, 'Recipies')
        
        self.tableItems = QTableWidget()
        self.tabWidget.addTab(self.tableItems, 'Items')
        
        self.show()
        
    def keyboardshortcuts(self):
        self.keyboardshortcutsWidget = QWebView()
        self.keyboardshortcutsWidget.load('http://www.google.com/')
        self.keyboardshortcutsWidget.show()
        self.keyboardshortcutsWidget.reload()

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
        self.tabWidget.setGeometry(0, windowGap, self.windowWidth, self.windowHeight)
        
    def genSignal(self):
        """
            Contains all of the signals to keep track off
        """
        self.connect(self.tabWidget.widget(0), SIGNAL('itemSelectionChanged()'), self.core.save)
        self.connect(self.tabWidget.widget(1), SIGNAL('itemSelectionChanged()'), self.core.save)
        self.connect(self.searchBox, SIGNAL('returnPressed()'), self.core.search)
        self.connect(self.tabWidget, SIGNAL('currentChanged(int)'), self.core.controls)
        #self.connect(self.spacer1, SIGNAL('itemSelectionChanged()'), self.core.debug)
        #self.core.saved.connect(self.core.debug)
        return True



