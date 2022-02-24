# -*- coding: utf-8 -*-
"""
See `prereleaser_middle`.

"""


import re
import os
import os.path
import glob


logger = __import__('logging').getLogger(__name__)

def prereleaser_middle(data): # pragma: no cover
    """
    zest.releaser prerelease middle hook.

    The prerelease step:

        * asks you for a version number
        * updates the setup.py or version.txt and the
          CHANGES/HISTORY/CHANGELOG file
        * offers to commit those changes to git

    Within the middle hook:

        * All data dictionary items are available and some questions
          (like new version number) have been asked.
        * No filesystem changes have been made yet.


    This hooks:

    - Adds the version number to ``versionadded``, ``versionchanged`` and
      ``deprecated`` directives in Python source.

    Assumptions:

    - The source is found in ``src/{name}`` where ``name`` comes from
      ``data['name']`` which in turn comes from setup.py.

    .. todo: This does not look at .rst files in the ``docs/`` directory.

    .. versionadded:: NEXT
    """
    project_name = data['name']
    if '.' in project_name:
        # Namespace packages
        project_name = project_name.split('.')[0]
    new_version = data['new_version']

    # Put the version number in source files.
    regex = re.compile(b'.. (versionchanged|versionadded|deprecated):: NEXT')
    if not isinstance(new_version, bytes):
        new_version_bytes = new_version.encode('ascii')
    else:
        new_version_bytes = new_version

    replacement = br'.. \1:: %s' % (new_version_bytes,)

    base_dir = os.path.join(data['reporoot'], 'src', project_name)
    if not os.path.exists(base_dir):
        raise Exception(f"Unable to find source directory at {base_dir!r}")

    pattern = os.path.join(base_dir, "*.py")
    print("Searching for", pattern)
    for path in glob.iglob(pattern, recursive=True):
        print(path)
        with open(path, 'rb') as f:
            contents = f.read()
        new_contents, count = regex.subn(replacement, contents)
        if count:
            print("Replaced version NEXT in", path)
            with open(path, 'wb') as f:
                f.write(new_contents)
