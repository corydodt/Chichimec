import string

from twisted.python.util import sibpath

def _resourceDefs():
    global RGEN, RESOURCE
    RGEN = lambda s: lambda filename: sibpath(s, filename)
    RESOURCE = RGEN(__file__)

_resourceDefs()

def nameFix(s):
    """
    Return an all-lowercase version of s, a PEP-8 compliant package name based
    on the input
    """
    s = s.lower()
    s = s.translate(string.maketrans("", ""), string.punctuation + " ")
    if not len(s):
        raise ValueError("string must be at least 1 character long, excluding punctuation")

    return s[:128]
