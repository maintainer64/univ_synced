import logging
from core.any_migration.application.repository import AnyMigrationBase

logger = logging.getLogger(__name__)


class FullManyToOneMigrationUseCase:
    def __init__(
        self, faculty_migrate: AnyMigrationBase, deps_migrate: AnyMigrationBase, groups_migrate: AnyMigrationBase,
    ):
        self.faculty_migrate = faculty_migrate
        self.deps_migrate = deps_migrate
        self.groups_migrate = groups_migrate

    async def execute(self):
        z = await self.faculty_migrate.migrate()
        logger.info(f"Faculty migration complete, {z}")
        z = await self.deps_migrate.migrate()
        logger.info(f"Deps migration complete, {z}")
        z = await self.groups_migrate.migrate()
        logger.info(f"Groups migration complete, {z}")
