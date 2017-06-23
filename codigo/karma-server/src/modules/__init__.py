''' Module container '''
from modules.level import level
from modules.selection import selection
from modules.validation import validation

def get_all_modules():
    ''' Returns all modules, level, selection and validation '''
    return [level, selection, validation]
