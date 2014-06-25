#!/usr/bin/env python
# standalone script to be run from the shell as "./recreate_environment.py [arg]",
# where [arg] is local (for your development machine),
# or dev/staging/production (for Heroku)
# use this when you've made changes to the code that affected the database schema.
# it will drop the dev DB and recreate it, thus providing a blank slate.

import sys
import os
import commit_and_push

# replace the below app names with your heroku app names
heroku_apps = {
    'dev': 'heroku-app-name-dev',
    'staging': 'heroku-app-name-staging',
    'production': 'heroku-app-name-production'
}

def main():
    environment = sys.argv[1]
    syncdb = 'python manage.py syncdb --traceback'
    create_session = 'python manage.py create_session'

    if environment == 'local':
        open('_ptree_experiments/db.sqlite3', 'w').write('')
        os.system(syncdb)
        os.system(create_session)

        # then launch from PyCharm
    else: # heroku

        if environment == 'production':
            confirmed = raw_input('Enter "y" if you are sure you want to reset the production database.').lower() == 'y'
            if not confirmed:
                print 'exit.'
                return

        reset_db = 'heroku pg:reset DATABASE --confirm {}'.format(heroku_apps[environment])
        os.system(reset_db)

        commit_and_push.run(environment)

        heroku_run_command = 'heroku run {} --remote {}'

        syncdb = heroku_run_command.format(syncdb, environment)
        create_session = heroku_run_command.format(create_session, environment)

        os.system(syncdb)
        print create_session
        os.system(create_session)

if __name__ == '__main__':
    main()

# creating objects on production
# DOES NOT RESET DATABASE
# heroku run python manage.py create_session --remote production
