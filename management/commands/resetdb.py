import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection, transaction
from dataclasses import dataclass

from otree import common_internal
from typing import Tuple, List

logger = logging.getLogger('otree')

MSG_RESETDB_SUCCESS_FOR_HUB = 'Created new tables and columns.'
MSG_DB_ENGINE_FOR_HUB = 'Database engine'

@dataclass
class DBDeletionInfo:
    db_engine: str
    table_delete_command: str


def db_label_and_drop_cmd(db_engine: str) -> DBDeletionInfo:
    db_engine_lower = db_engine.lower()
    if 'oracle' in db_engine_lower:
        return DBDeletionInfo('Oracle', 'DROP TABLE "{table}" CASCADE CONSTRAINTS;')
    if 'postgres' in db_engine_lower:
        return DBDeletionInfo('Postgres', 'DROP TABLE "{table}" CASCADE;')
    if 'mysql' in db_engine_lower:
        return DBDeletionInfo(
            'MySQL',
            (
                'SET FOREIGN_KEY_CHECKS = 0;'
                'DROP TABLE {table} CASCADE;'
                'SET FOREIGN_KEY_CHECKS = 1;'
            )
        )
    # put this last for test coverage
    if 'sqlite3' in db_engine_lower:
        return DBDeletionInfo('SQLite', 'DROP TABLE {table};')
    raise ValueError(
        'resetdb command does not recognize DB engine "{}"'.format(db_engine))

def cursor_execute_drop_cmd(cursor, stmt):
    cursor.execute(stmt)


def migrate_db(options):
    # need to hide the migrations/ folder so that Django thinks
    # it doesn't exist.
    # Tried setting MIGRATIONS_MODULES but doesn't work
    # (causes ModuleNotFoundError)
    common_internal.patch_migrations_module()

    call_command(
        'migrate', interactive=False, run_syncdb=True, **options
    )


class Command(BaseCommand):
    help = (
        "Resets your development database to a fresh state. "
        "All data will be deleted.")

    def add_arguments(self, parser):
        ahelp = (
            'Tells the resetdb command to NOT prompt the user for '
            'input of any kind.')
        parser.add_argument(
            '--noinput', action='store_false', dest='interactive',
            default=True, help=ahelp)

    def _confirm(self) -> bool:
        self.stdout.write(
            "This will delete and recreate your database. ")
        answer = input("Proceed? (y or n): ")
        if answer:
            return answer[0].lower() == 'y'
        return False


    def _get_tables(self) -> List[str]:
        with connection.cursor() as cursor:
            tables = connection.introspection.get_table_list(cursor)
        # in the old version, juan reversed the list, not sure why,
        # maybe something about foreign key dependencies?
        return [
            t.name for t in tables
            # do this so it will fail loudly if the "type" doesn't match
            if {'t': True, 'v': False, 'p': False}[t.type]
        ]

    def _drop_tables(self, tables, drop_cmd: str):
        with connection.cursor() as cursor:
            for table in tables:
                stmt = drop_cmd.format(table=table)
                cursor_execute_drop_cmd(cursor, stmt)

    def handle(self, *, interactive, **options):
        if interactive and not self._confirm():
            self.stdout.write('Canceled.')
            return

        dbconf = settings.DATABASES['default']
        drop_db_info = db_label_and_drop_cmd(dbconf['ENGINE'])
        db_engine = drop_db_info.db_engine


        # hub depends on this string
        logger.info(f"{MSG_DB_ENGINE_FOR_HUB}: {db_engine}")

        tables = self._get_tables()

        logger.info(f"Dropping {len(tables)} tables...")
        is_sqlite = 'sqlite' in db_engine.lower()
        if is_sqlite:
            # otherwise, when I drop tables I get:
            # django.db.utils.IntegrityError: FOREIGN KEY constraint failed
            # see: https://www.sqlitetutorial.net/sqlite-drop-table/
            # potentially i could do 'DELETE FROM {table};'
            # for each table before i drop any table,
            # but that's more code, and I'm not sure it will work.
            connection.disable_constraint_checking()
        try:
            self._drop_tables(tables, drop_db_info.table_delete_command)
        finally:
            if is_sqlite:
                # maybe overkill but perhaps resetdb could be called via call_command()
                connection.enable_constraint_checking()

        migrate_db(options)

        # mention the word 'columns' here, so people make the connection
        # between columns and resetdb, so that when they get a 'no such column'
        # error, they know how to fix it.
        # (An alternative is to generically catch "no such column" errors,
        # but I recall that this was difficult - because there were many
        # code paths or exception classes. Could re-investigate.)

        # 2018-11-08: oTree Hub depends on this string
        logger.info(MSG_RESETDB_SUCCESS_FOR_HUB)
