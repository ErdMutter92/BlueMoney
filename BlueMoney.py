import control, view, firstrun, platform, os

class BlueMoney:

    system = platform.system()
    
    if system == 'darwin':
        dataDir = '.'
    else:
        dataDir = '.'

    if not os.path.exists(dataDir+'/data/firstrun'):
        setup = firstrun.Firstrun(dataDir)
    view = view.View()