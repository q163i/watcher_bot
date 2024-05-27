# Import Logging
from LoggerConfig import custom_logger
logger = custom_logger()

from DefineTables import Admins, BlockedUsers

from sqlalchemy import func

class check_list:
    def __init__(self, session):
        self.session = session

    def check_table(self, table_class, log_message):
        item_count = self.session.query(table_class).count()
        logger.info(f"[DB] {log_message}: {item_count}")
        return item_count

    def check_unique_users_and_messages(self):
        unique_users_count = self.session.query(func.count(BlockedUsers.telegram_id.distinct())).scalar()
        logger.info(f"[DB] Unique blocked users: {unique_users_count}")
        return unique_users_count

    def check_all(self):
        self.check_table(Admins, "admins")
        self.check_table(BlockedUsers, "blockedMessages")
        self.check_unique_users_and_messages()