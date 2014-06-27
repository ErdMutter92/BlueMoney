import control, view, firstrun, platform, os, sys, error, traceback

class BlueMoney:

    try:
        system = platform.system()
        if system == 'darwin':
            dataDir = '.'
        else:
            dataDir = '.'

        if not os.path.exists(dataDir+'/data/firstrun'):
            setup = firstrun.Firstrun(dataDir)
        view = view.View()
    except IndexError as e:
        error.report('IndexError', e)
    except Exception as e:
        error.report('Unknown Exception', e)
    except GeneratorExit as e:
        error.report('System Exit', e)