[Homepage](http://www.otree.org/)

These are the core oTree libraries.

## Docs

[http://otree.readthedocs.io/en/latest/index.html](http://otree.readthedocs.io/en/latest/index.html)

## Quickstart

### Typical setup

```
pip install --upgrade otree-core
otree startproject oTree
otree resetdb
otree runserver
```

### Core dev setup

If you are modifying otree-core locally, clone or download this repo,
then run this from the project root:

```
pip install -e .
cd .. # or wherever you will start your project
otree startproject oTree
otree resetdb
otree runserver
```

See [this](http://otree.readthedocs.io/en/latest/django.html)
document that explains how oTree differs from a typical Django project.

[![Build Status](https://travis-ci.org/oTree-org/otree-core.svg?branch=master)](https://travis-ci.org/oTree-org/otree-core)
