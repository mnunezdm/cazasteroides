''' Module container '''
from karmaserver.modules.level import level
from karmaserver.modules.selection import selection
from karmaserver.modules.validation import validation


def get_all_modules():
    ''' Returns all modules, level, selection and validation '''
    return [level, selection, validation]
