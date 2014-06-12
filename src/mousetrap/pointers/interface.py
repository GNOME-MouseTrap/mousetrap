'''
Each module in mousetrap.pointers must define a Pointer class
that inherits mousetrap.pointers.interface.Pointer.
'''


class Pointer(object):
    def update_image(self, image):
        raise NotImplementedError('Must implement.')

    def get_new_position(self):
        '''Returns new location (x, y) or None if no change.'''
        raise NotImplementedError('Must implement.')
