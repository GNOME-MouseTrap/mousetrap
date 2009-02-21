
def get_idm(idm):
    """
    Returns the idm's class instance.

    Arguments:
    - idm: The requested idm.
    """
    return __import__("ocvfw.idm.%s" % idm,
                      globals(),
                      locals(),
                      [''])
