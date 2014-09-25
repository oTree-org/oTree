## Homepage
http://www.otree.org/

## Live demo
http://demo.otree.org/

## Quick start

    git clone git@github.com:oTree-org/oTree.git
    cd oTree
    # if you are using Mac ("pip install -r" sometimes fails to install psycopg2, which is unnecessary locally)
    cat requirements.txt | while read PACKAGE; do pip install "$PACKAGE"; done
    # if you are using Windows
    gc .\requirements.txt | foreach {pip install $_}
    python recreate_environment.py
    python manage.py runserver

## Full documentation
https://github.com/oTree-org/oTree/wiki

## Contact email
info@otree.org
