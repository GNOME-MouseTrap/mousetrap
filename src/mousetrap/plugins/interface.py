from mousetrap.i18n import _


class Plugin(object):
    def __init__(self, config):
        '''Override to initialize and configure yourself.
        (Do not call parent/this constructor.)'''
        raise NotImplementedError(_('Must implement.'))

    def run(self, app):
        '''Called each pass of the loop.'''
        raise NotImplementedError(_('Must implement.'))
