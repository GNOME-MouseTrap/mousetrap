'''
Each module in mousetrap.pointers must define a Pointer class
that inherits mousetrap.pointers.interface.Pointer.
'''


class Pointer(object):
    def update_image(self, image):
        raise Exception('Unimplemented method add_image().')

    def get_new_position(self):
        '''Returns new location (x, y) or None if no change.'''
        raise Exception('Unimplemented method get_position().')
