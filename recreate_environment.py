# use this when you've made changes to the code (on the dev site) that affected the database schema.
# it will drop the dev DB and recreate it, thus providing a blank slate.

import sys
import os
import commit_and_push

heroku_apps = {
    'demo': 'otree-demo',
}

def main():
    if len(sys.argv) == 1:
        # default to local
        environment = 'local'
    else:
        environment = sys.argv[1]

    syncdb = 'python manage.py syncdb --traceback'

    if environment == 'local':
        open('_otree_experiments/db.sqlite3', 'w').write('')
        os.system(syncdb)
        # then launch from PyCharm
    else:
        # heroku
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
        os.system(syncdb)

if __name__ == '__main__':
    main()