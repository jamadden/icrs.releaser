# -*- coding: utf-8 -*-
"""
See `release_middle`.

"""


logger = __import__('logging').getLogger(__name__)

def release_before(data):
    print("BEFORE")
    print(data)

def release_middle(data):
    print("MIDDLE")
    print(data)
    raise Exception
