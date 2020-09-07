`Homepage`_

These are the core oTree libraries.

Before you fork this project, keep in mind that otree-core is updated
frequently, and over time you might get upstream merge conflicts, as
your local project diverges from the oTree mainline version.

Instead, consider creating a project with ``otree startproject`` and
making your modifications in an app, using oTree’s public API. You can
create custom URLs, channels, override settings, etc.

Docs
----

http://otree.readthedocs.io/en/latest/index.html

Quickstart
----------

Typical setup
~~~~~~~~~~~~~

::

    pip install -U otree
    otree startproject oTree
    cd oTree
    otree devserver

Core dev setup
~~~~~~~~~~~~~~

If you are modifying otree-core locally, clone or download this repo,
then run this from the project root:

::

    pip install -e .
    cd .. # or wherever you will start your project
    otree startproject oTree
    cd oTree
    otree devserver


|Build Status|

.. _Homepage: http://www.otree.org/

.. |Build Status| image:: https://travis-ci.org/oTree-org/otree-core.svg?branch=master
   :target: https://travis-ci.org/oTree-org/otree-core