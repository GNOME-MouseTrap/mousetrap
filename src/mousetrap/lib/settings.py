import ConfigParser
import environment as env

class settings( ConfigParser.ConfigParser ):

    def optionxform( self, optionstr ):
        return optionstr

def load():
    cfg = settings()
    cfg.readfp(open( env.configFile ))
    return cfg
