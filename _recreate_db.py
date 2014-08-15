# still getting this to work
import sys
import os
import commit_and_push

def main():
    if os.environ['HEROKU']:
        if os.environ['OTREE_PRODUCTION']:
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


    if environment == 'local':
        open('_otree_experiments/db.sqlite3', 'w').write('')
        os.system(syncdb)
        # then launch from PyCharm
    else:
        if environment == 'production':


