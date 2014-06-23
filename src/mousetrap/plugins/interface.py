class Plugin(object):
    def __init__(self, config):
        '''Override to initialize and configure yourself.
        (Do not call parent/this constructor.)'''
        raise NotImplementedError('Must implement.')

    def run(self, app):
        '''Called each pass of the loop.'''
        raise NotImplementedError('Must implement.')
