
.. image:: https://coveralls.io/repos/github/once.releaser/badge.svg?branch=main
    :target: https://coveralls.io/github/once.releaser?branch=main
    :alt: Coveralls

.. image:: https://codecov.io/gh/once.releaser/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/once.releaser

.. image:: https://img.shields.io/pypi/v/once.releaser.svg
    :target: https://pypi.python.org/pypi/once.releaser/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/once.releaser.svg
    :target: https://pypi.python.org/pypi/once.releaser
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/once.releaser.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/once.releaser.svg
    :target: https://pypi.python.org/pypi/once.releaser/
    :alt: License


================
once.releaser
================

Custom releaser hooks for JIRA project based on zest.releaser and cs.zestreleaser.changelog.
This hook extract the commit messages from the last release tag to the current tag and create the towncrier news fragments, based on the JIRA issue and the towncrier type.

Currently it only supports GIT VCS logs.

The commit messages must be in the following format::

    <optional prefix> <issue_name>-<issue_number> <towncrier type> <message> [<author>]


Author will be extracted from the git history.

Examples
--------

The following commit messages are valid:

- Revert WEBAGL-1234 feature Add new feature
- Add WEBAGL-1234 feature new feature
- WEBAGL-1235 bugfix Fix AttributeError RequestContainer object has no attribute getClientForURL

Fragments files will be created in the following format:

**news/WEBAGL-1234.feature** ::

    Add new feature [Rafael Bermúdez Horcajada <myemail@email.com>]
    Revert new feature [Rafael Bermúdez Horcajada <myemail@email.com>]


**news/WEBAGL-1235.bugfix** ::

    Fix AttributeError RequestContainer object has no attribute getClientForURL [Rafael Bermúdez Horcajada <myemail@email.com>]
    


Installation
------------

Using pip::

    $ pip install once.releaser


Authors
-------

- Rafael Bermúdez Horcajada


Contributors
------------

Put your name here, you deserve it!

- ?


Contribute
----------

- Issue Tracker: https://github.com/once.releaser/issues
- Source Code: https://github.com/once.releaser


License
-------

The project is licensed under the GPLv2.
