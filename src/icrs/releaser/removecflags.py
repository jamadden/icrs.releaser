# -*- coding: utf-8 -*-
"""
See `prereleaser_before`.

"""

import os
import sys

def prereleaser_before(data): # pragma: no cover pylint:disable=unused-argument
    """
    Strip CFLAGS and other compile settings that
    may not be portable.

    .. versionadded:: NEXT
    """
    # Especially CFLAGS. If this is compiled in a newer machine with a
    # setting like -march=native, it will produce wheels that won't
    # run on older machines, generating illegal instruction faults.
    for bad_env in (
            'CFLAGS',
            'CPPFLAGS',
            'CXXFLAGS',
            'LDFLAGS',
    ):
        if bad_env in os.environ:
            print("Removing potentially dangerous env setting",
                  bad_env, os.environ[bad_env], file=sys.stderr)
            del os.environ[bad_env]
