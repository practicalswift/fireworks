class Configuration:
    def __init__(self):
        #For now, configuration is hard-coded.
        #In the future, load from commandline args and config file.
        self.sections = \
        {
        'modules':
            {
            'frontend': 'qt',
            'backend': 'lightningd'
            }
        }


    def getValue(self, section, name):
        return self.sections[section][name]

