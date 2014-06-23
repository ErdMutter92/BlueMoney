"""
   Author: Alexis M. Bleau
   Title: Notification Wrapper for applescript
   Discription: using the applescript library, this
   class allows for you to send notifications to the
   notification center.
    
"""
import applescript

class notify:

    title_ = ''
    subtitle_ = ''
    text_ = ''
    soundName_ = ''
    
    def __init__(self, title='', text='', subtitle='', soundName=''):
        self.soundName_ = ' sound name "'+soundName+'"'
        self.title_ = ' with title "'+title+'"'
        self.subtitle_ = ' subtitle "'+subtitle+'"'
        self.text_ = 'display notification "'+text+'"'

    def setTitle(self, title):
        self.title_ = ' with title "'+title+'"'

    def setSubtitle(self, subtitle):
        self.subtitle_ = ' subtitle "'+subtitle+'"'

    def setText(self, text):
        self.text_ = 'display notification "'+text+'"'

    def setSound(self, soundName):
        self.soundName_ = ' sound name "'+soundName+'"'

    def push(self):
        notification = self.text_+self.title_+self.subtitle_+self.soundName_
        applescript.AppleScript(notification).run()
