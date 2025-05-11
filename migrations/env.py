import logging
from logging.config import fileConfig

from flask import current_app

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# Import the app factory
from Hunt4TheMurderer import create_app

# Create the app using the factory
app = create_app()[0]

def get_engine():
    try:
        return current_app.extensions['migrate'].db.get_engine()
    except TypeError:
        return current_app.extensions['migrate'].db.engine

def get_engine_url():
    try:
        return get_engine().url.render_as_string(hide_password=False).replace('%', '%%')
    except AttributeError:
        return str(get_engine().url).replace('%', '%%')

def get_metadata():
    db = current_app.extensions['migrate'].db
    if hasattr(db, 'metadatas'):
        return db.metadatas[None]
    return db.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    with app.app_context():
        url = get_engine_url()
        context.configure(
            url=url, target_metadata=get_metadata(), literal_binds=True
        )
        with context.begin_transaction():
            context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    with app.app_context():
        def process_revision_directives(context, revision, directives):
            if getattr(config.cmd_opts, 'autogenerate', False):
                script = directives[0]
                if script.upgrade_ops.is_empty():
                    directives[:] = []
                    logger.info('No changes in schema detected.')
        connectable = get_engine()
        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=get_metadata(),
                process_revision_directives=process_revision_directives,
                **current_app.extensions['migrate'].configure_args
            )
            with context.begin_transaction():
                context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
