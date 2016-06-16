from .test import test
from .program import run

config = {
    'wantdiff': True,
    'wantsfiles': True,
    'threadsafe': True,
    'behavior': {
        'creates': [['dump', 'featureLocation']]
    }
}