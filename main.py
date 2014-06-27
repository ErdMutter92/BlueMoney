"""
    Author: Alexis M. Bleau <alexis@bleauweb.net>
    Title: Blue Money Loopback Interface
    
    Copyright 2014 by Alexis M. Bleau, All Rights Reserved!
    
    Discription: The command line interface for program. takes in user 
    commands andexecutes them within the definitions pre-determened. If
    arguments are provided at start: parses commands, executes commands, 
    and then quits. Otherwise the program runs in a continuous loop 
    prompting for user input of commands until the exit command is given.
    
"""
import database
import sys, shlex, os, subprocess

class loopback:
    
    bills = database.csdv('bills')
    registry = database.csdv('registry')
    
    clientConfig = ['Blue Money Buget', 'v0.0.4e']
    
    def gui(self):
        subprocess.call(["python", "gui.py"])
    
    def update(self):
        self.update = update.updater()
        self.update.client()

    def run(self, ui):
        '''
            Command line interface for program. takes in user commands 
            and executes them within the definitions pre-determened. If
            arguments are provided at start: parses commands, executes
            commands, and then quits. Otherwise the program runs in a
            continuous loop prompting for user input of commands until
            the exit command is given.
        '''
        #print(clientConfig[0]+' '+clientConfig[1]) ## prints program title in terminal.
        ## default setting, never ending while loop.
        self.continuewhile = True
        while self.continuewhile:
        ## if commands provided at start, turn never ending loop off, and load
        ## those commands into user input list for later processing.
            if len(ui) != 1:
                self.continuewhile = False
                self.ui = []
                for item in ui:
                    self.ui.append(item)
                self.ui = self.ui[1:]
            else:
                ## If no commandsprovided at start prompt for user input,
                ## append all user input to ui list for later processing.
                self.continuewhile = True
                self.ui = []
                for cmd in shlex.split(str(raw_input('cmd: '))):
                    self.ui.append(cmd)
    
            if len(self.ui) > 0:
                ## exits program at users request.
                if self.ui[0] == 'exit': return True;
                ## updates program at users request.
                elif self.ui[0] == 'update': self.update();
                ## Sends the Read Command at users request.
                elif self.ui[0] == 'read':
                    if self.ui[1] == 'bills':
                        self.bills.read()
                    elif self.ui[1] == 'registry':
                        self.registry.read()
                ## Runes the GUI at users request
                if self.ui[0] == 'gui': subprocess.call(["python", "gui.py"]);
                ## Sends the write Command at users request.
                elif self.ui[0] == 'write': print(':)');
                ## clears screen upon user's request.
                elif self.ui[0] == 'clear': os.system(['clear','cls'][os.name == 'nt']);
                ## Returns error if command unknown.
                else: print("Command not found: "+self.ui[0]);
