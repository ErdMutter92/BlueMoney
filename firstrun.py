'''
    Title: Blue Money Firstrun Tool
    Author: Alexis Matthew Bleau <alexis@bleauweb.net>
    
    Copyright 2014 Alexis Bleau. All rights reserver.

    Discription: Sets up the application during the first run.
    Generates apropreate database files, and runs the applications
    repair script to generate the backup files.
'''
from urllib2 import *
import os, base64, hashlib, sys, textwrap, repair, platform

currentPlatform = platform.system()

if currentPlatform == 'Darwin':
    dataDir = '/Library/BlueMoney'
else:
    dataDir = '.'

class Firstrun():
    
    keyboardHelp = 'PGh0bWw+CjxoZWFkPgoJPHRpdGxlPkJsdWVNb25leSBLZXlib2FyZCBTaG9ydGN1dHM8L3RpdGxlPgo8L2hlYWQ+Cjxib2R5PgoJPHN0eWxlIHR5cGU9InRleHQvY3NzIj4KCQlib2R5IHsKCQkJYmFja2dyb3VuZC1jb2xvcjogI2VlZWVlZTsKCQl9CgkJdGFibGUsdHIsdGggewoJCQloZWlnaHQ6IDEwMHB4OwoJCQlwYWRkaW5nOiA1cHg7CgkJfQoJCS50aXRsZSB7CgkJCXdpZHRoOiAxNSU7CgkJfQoJCS5vZGQgewoJCQliYWNrZ3JvdW5kLWNvbG9yOiAjZGRkZGRkOwoJCX0KCQkua2V5IHsKCQkJd2lkdGg6IDQwJTsKCQl9CgkJLmRpc2MgewoJCQl3aWR0aDogMzUlOwoJCX0KCQloMSB7CgkJCWhlaWdodDogMjVweDsKCQl9Cgk8L3N0eWxlPgoJPGgxPktleWJvYXJkIFNob3J0Y3V0czwvaDE+Cgk8dGFibGU+CgkgIDx0ciBjbGFzcz0nb2RkJz4KCSAgICA8dGggY2xhc3M9J3RpdGxlJz5DbG9zZSBQcm9ncmFtPC90aD4KCSAgICA8dGggY2xhc3M9J2tleSc+V2luZG93czogQ3RybCtRPGJyIC8+T1MgWDogY21kK1E8L3RoPgoJICAgIDx0aCBjbGFzcz0nZGlzYyc+U3RvcHMgdGhlIHByb2dyYW0gZnJvbSBydW5uaW5nLCBjbG9zaW5nIG91dCBvZiBhbnkgZGlhbG9nIHdpbmRvd3MgaXQgY29udHJvbHMsIGFuZCByZW1vdmVzIHRoZSB0b29sYmFyIGljb24uPC90aD4KCSAgPC90cj4KCSAgPHRyID4KCSAgICA8dGggY2xhc3M9J3RpdGxlJz5BZGQgVGFibGUgRW50cnk8L3RoPgoJICAgIDx0aCBjbGFzcz0na2V5Jz5XaW5kb3dzOiBDdHJsK1NoaWZ0K0E8YnIgLz5PUyBYOiBjbWQrU2hpZnQrQTwvdGg+CgkgICAgPHRoIGNsYXNzPSdkaXNjJz5BZGRzIGEgbmV3IHRhYmxlIHJvdyB0byB0aGUgY3VycmVudGx5IGJlaW5nIHZpZXdlZCB0YWJsZS4gVGhpcyBhbHNvIHNhdmVzIHRoZSBjdXJyZW50bHkgdmlld2VkIHRhYmxlIGFmdGVyIGFkZGluZyB0aGUgdGFiLjwvdGg+CgkgIDwvdHI+CgkgIDx0ciBjbGFzcz0nb2RkJz4KCSAgICA8dGggY2xhc3M9J3RpdGxlJz5SZW1vdmUgVGFibGUgRW50cnk8L3RoPgoJICAgIDx0aCBjbGFzcz0na2V5Jz5XaW5kb3dzOiBDdHJsK0RlbDxiciAvPk9TIFg6IGNtZCtEZWw8L3RoPgoJICAgIDx0aCBjbGFzcz0nZGlzYyc+UmVtb3ZlcyBhIG5ldyB0YWJsZSByb3cgdG8gdGhlIGN1cnJlbnRseSBiZWluZyB2aWV3ZWQgdGFibGUuIFRoaXMgYWxzbyBzYXZlcyB0aGUgY3VycmVudGx5IHZpZXdlZCB0YWJsZSBhZnRlciByZW1vdmVpbmcgdGhlIHRhYi48L3RoPgoJICA8L3RyPgoJICA8L3RyPgoJICA8dHIgPgoJICAgIDx0aCBjbGFzcz0ndGl0bGUnPkZpbmQgRW50cnk8L3RoPgoJICAgIDx0aCBjbGFzcz0na2V5Jz5XaW5kb3dzOiBDdHJsK0Y8YnIgLz5PUyBYOiBjbWQrRjwvdGg+CgkgICAgPHRoIGNsYXNzPSdkaXNjJz5Hb2VzIHRvIHRoZSBuZXh0IGl0ZW0gY29udGFpbmluZyB0aGUgdGV4dCBmcm9tIHRoZSBzZWFyY2ggYm94LjwvdGg+CgkgIDwvdHI+CgkgIDx0ciBjbGFzcz0nb2RkJz4KCSAgICA8dGggY2xhc3M9J3RpdGxlJz5TYXZlIEN1cnJlbnQgVGFiPC90aD4KCSAgICA8dGggY2xhc3M9J2tleSc+V2luZG93czogQ3RybCtTPGJyIC8+T1MgWDogY21kK1M8L3RoPgoJICAgIDx0aCBjbGFzcz0nZGlzYyc+U2F2ZXMgdGhlIHdvcmsgZG9uZSBpbiB0aGUgY3VycmVudCB0YWIgdG8gaXQncyBkYXRhYmFzZSBmaWxlLjwvdGg+CgkgIDwvdHI+CgkgIDx0ciBjbGFzcz0nJz4KCSAgICA8dGggY2xhc3M9J3RpdGxlJz5Td2l0Y2ggVGFiczwvdGg+CgkgICAgPHRoIGNsYXNzPSdrZXknPldpbmRvd3M6IEN0cmwreyN9PGJyIC8+T1MgWDogY21kK3sjfTwvdGg+CgkgICAgPHRoIGNsYXNzPSdkaXNjJz5Td2l0Y2hlcyBiZXR3ZWVuIHRoZSB0YWJzLCB3aGVyZSB7I30gaXMgdGhlIHBvc2l0aW9uIG9mIHRoZSB0YWIgKDEgdG8gNik8L3RoPgoJICA8L3RyPgoJPC90YWJsZT4KPC9ib2R5Pgo8L2h0bWw+Cg=='

    block32 = 'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAABZ0RVh0Q3JlYXRpb24gVGltZQAwOC8xOC8wOaw6EPwAAAAcdEVYdFNvZnR3YXJlAEFkb2JlIEZpcmV3b3JrcyBDUzQGstOgAAACJElEQVRYhc2Xz23bUAyHvxQ5FnA3cDaQPYHVIw8FfOjd6gTNCGknyAZxN0hPvMroAJEHCBBvYE/gHkQZ+sMnPTkxkh9gwIYp8hNF8lFXx+OR99T1GGMRWQKpfRLHZAvkQK6qjzE+r2IyICIZcAdMY5yadsCdqq7PBhCRG2ANLEYEbmsDZKr6MgpARGaU6Zy8InilA5CqahEFYMGfIhxvat9jsjRvQ3QALO0F4Tv/A9x7d2Pgt8AqcO0BmNUfxyfHaN0THMoK7wQHUNVCVTNgTtkRbU3M/0kNAKv2oVQ+iMh9n4EBpjQfUaWFxekCULZajH6KyHoAYg8s8TNxinMCsCEzps9XkRCZ89fU4jUykDqGz28AUVAWbltpDMD3wMVtiFxEvvTYeDXTAejM9lpV/xiAWABBiEDXJG2Atk4VbPN8CCLpg8DviF6AhgxiTjlMzoU4H8Agqv7eDUAUNhVfBeAOJIOY4fd3pSllJuoQrr86QMdh6C6sv1Pgbw/EpIII+Nm2AXLH6DbkXVX3qrqkv00n5ve3818eA7AaepbWpr8GIL6FABrHsYi80B3HW8plYt8HYgfMQ59NTTtVvYG4wygBHoday9r0K/1t2onjLSQ5fsVuKXc7dxeoXT8D/gGfAyYbVU2rH14bZvh3kQBPIrIO1UVtIwoFP9A6HT/eTtiCyLnwVhychLWJ5x4iI7ShXETd2vnYb0YOyPu8G15So47jS+g/ZtsDvqC7VUgAAAAASUVORK5CYII='

    stop32 = 'iVBORw0KGgoAAAANSUhEUgAAAB0AAAAdCAYAAABWk2cPAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAABZ0RVh0Q3JlYXRpb24gVGltZQAwOC8xOS8wORSGd5kAAAAcdEVYdFNvZnR3YXJlAEFkb2JlIEZpcmV3b3JrcyBDUzQGstOgAAABvElEQVRIic2XwXWCQBCGP23AEmIHwQrCkTlJOrAUStEKoqe5YgWJHcQSqMAcGCLowO4m5r3873Fhh/mY3ZlhmF0uF0ISkRLI7Xp2TE5ADdSqug/5m01BRWQDVMBT8M2uOgOVqm6ToCKyBLbASwLsVkdgo6qfQaiIZLRbtfgFsFMD5Kr6MQo14PsDYLda9cHzHnBJG+FfqDb/QyjtGXpbeqDdphg1Zn+rhfm/Qi1LvaTZqWpXLiFwd34lsHPWX4zzHWnlGB1UdQNg5zEFHiSMPedFXAHMiqIogbeQIxjN7Fi7Tq9zi8DTgjYBsu6GE3EqECCfgobA5x8AAfJZURTh5jtS5H2lNJV5yMB0F/FPgSnQDjz2BdnHAlOhDVCOrJXEN5Bo6OSZRtTxHfSUChSRTEQ+A+U0ptOc6SY/VYdPhOvYUz0FjSn8mAZyD7WZ5uwtRhb+GNgL5qyq+6mGvxaRbQDogu25tWNXQW9yEJEa//N2oN2umDps7OU84FFVcxiWzAb/HNaRQMzOAzbmnwHUprY80nmq8v5UOGgOlgArErpLQA03Q9kdtAfOaOfW3+gIZF4X+z8TvgN/6L/MF/xGCeyc7nXSAAAAAElFTkSuQmCC'

    minus32 = 'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAK8AAACvABQqw0mAAAABZ0RVh0Q3JlYXRpb24gVGltZQAwOC8xOC8wOaw6EPwAAAAcdEVYdFNvZnR3YXJlAEFkb2JlIEZpcmV3b3JrcyBDUzQGstOgAAABVUlEQVRYhe2XzW2DQBBGH1HuLsF0YFyBuc4tJVCKS3EJuc11qSChA7sEKiAH1oifcQSBBQ75JA5Iq/kew+zsbFRVFVvqfcpiEfkAUv+cjCUF4ACnqp9jYkZjMiAiGXAFjmOCej2Aq6re/gwgIjFwAy4TjPvKgUxV75MARCShTudhhvlTJZCq6vcoAG/+tYBxX+c+xJthHlN/eQg5H/81APU/XyLtlg4+vg3gq31OwY3RxfsMAai32hpqfBoA32Sm7PM5Onq/TgbSlcw7frsCsHp7SJ3gl8NIVaOlHUVk0PWsPrCq/gHaAMXK3gV0i9DR2glWwSwsB90MuMCGJkBnHhCRO+u044eqxrCDw2gwEYmII+yRnKtq+nyxtmFGPcOFUOnjNxoA+Ok1DQSQ9qdjsxH5wfHMcpkoMQbSlwAtiIR6rp+jHEgsc9j7zcgA2eZuGFKbn4Y/J9SEquePCzsAAAAASUVORK5CYII='

    plus32 = 'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAABZ0RVh0Q3JlYXRpb24gVGltZQAwOC8xOC8wOaw6EPwAAAAcdEVYdFNvZnR3YXJlAEFkb2JlIEZpcmV3b3JrcyBDUzQGstOgAAABY0lEQVRYhe2XwXGDQAxFnzO5uwSnA+MKTI66pQRKcSmU4JuOgQpiOgglUAE5IDx4WduLsYFD/gyXHa3+R+jvilVd18yJ9yHBIvIFxPZsPSEFkAGZqh5Dcq5CKiAiCXAANiFJDSVwUNX0YQEi8gGkwH4AsYscSFT1d5AAEYloyrkeQd6iAmJVPQUJMPKfJxC72LkiegKs7Cfuv/mnZ+37zp4KiLqfw+eCNIAcVc3cNRG5t21t+eN24c1JkDCu4UKwN56+ABqrTYEzz1mAHTJDfD4GG+O7qEA8EfkF3+wCui7wne0+q93CrXjXoltXQA8+qz0af82irgsmx7+Abg8UOI0oIlfvalVduWu34j0o4LIC2YDNz0C2LAE2w5UTkZftzLicywjABsj8xeR5d1D12TChmVxegcrynzH7TOg9iCxox/MqUfnIrwroiIgY3xM5zSDaI4el/xl5hMzzb/hKzH4b/gEujpcM+TZK3gAAAABJRU5ErkJggg=='

    def mkCSDV(self, title, content):
        if not os.path.exists(dataDir+'/data/'+title+'.csdv'):
            print('Creating blank CSDV File for '+title+' items...')
            file = open(dataDir+'/data/'+title+'.csdv', 'a')
            file.write(content)
            file.close()
            return 1
        else:
            return 0

    def readBlob(self, file, blob):
        blob = base64.b64decode(blob)
        open(file,"wb").write(blob)
        return True

    def genFile(self, title, ext, location = dataDir+'/data/resources/'):
        if not os.path.exists(location+title+'.'+ext):
            self.readBlob(location+title+'.'+ext, getattr(self, title))
            print('Reconstituting '+title+'... ')

    def __init__(self, dataDir):
        if not os.path.exists(dataDir+'./data/firstrun'):
            print('Application is being setup!')
            self.setup(dataDir)
        else:
            print('Application has already been setup!')

    def setup(self, dataDir):
        print('Generating blank CSDV Resources...')
        if not os.path.exists(dataDir):
            os.mkdir(dataDir)
        
        if not os.path.exists(dataDir+'/data'):
            os.mkdir(dataDir+'/data')
        
        self.mkCSDV('bills', 'Description,Amount,Frequency,Last Payed')
        self.mkCSDV('budget', 'Discription,Alowance,Amount to Date')
        self.mkCSDV('registry', 'Check #,date,transaction,payment,deposit,balance')
        self.mkCSDV('items', 'NULL')
        self.mkCSDV('recipies', 'NULL')
        print('')
        
        #print('Reconstituting resource files...')
        #if not os.path.exists(dataDir+'/data/resources'):
        #    os.mkdir(dataDir+'/data/resources')
        #self.genFile('stop32', 'png')
        #self.genFile('minus32', 'png')
        #self.genFile('plus32', 'png')
        print('')
        
        print('First Run of Application Detected')
        if not os.path.exists('./data/backup'):
            os.mkdir('./data/backup')
        if not os.path.exists('./data/backup/data'):
            os.mkdir('./data/backup/data')
        if not os.path.exists('./data/backup/data/resources'):
            os.mkdir('./data/backup/data/resources')
        #backup = repair.repair('backup')
        open(dataDir+'/data/firstrun', 'w').write('')


