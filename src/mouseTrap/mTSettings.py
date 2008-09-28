import ConfigParser


class Settings( ConfigParser.ConfigParser ):

    def optionxform( self, optionstr ):
        return optionstr
    
