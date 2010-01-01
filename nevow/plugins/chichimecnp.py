"""
Create a mapping to help automatically load javascript from within Athena,
from the static directory
"""

from nevow import athena

from chichimec.util import RESOURCE

pkg = athena.AutoJSPackage(RESOURCE('static'))
