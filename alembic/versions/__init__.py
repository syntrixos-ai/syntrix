"""Alembic main script"""

from alembic import command
from alembic.config import Config
from app.core.config import settings

config = Config("alembic.ini")
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)


def upgrade():
    command.upgrade(config, "head")


def downgrade():
    command.downgrade(config, "-1")


if __name__ == "__main__":
    upgrade()
