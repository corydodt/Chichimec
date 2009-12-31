"""
Create a mapping to help automatically load javascript from within Athena,
from the static directory
"""

from nevow import athena

from {options[projectName]} import RESOURCE

pkg = athena.AutoJSPackage(RESOURCE('static'))
