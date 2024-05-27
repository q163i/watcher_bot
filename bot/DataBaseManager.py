from DefineTables import Admins, BlockedUsers


class DatabaseManager:
    def __init__(self, session):
        self.session = session

    def get_admins(self):
        try:
            admins = self.session.query(Admins).all()
            admins_json = [{'id': admin.id, 'username': admin.username, 'telegram_id': admin.telegram_id} for admin in admins]
            return admins_json
        finally:
            self.session.close()

    def get_blockedUsers(self):
        blockedUsers = self.session.query(BlockedUsers).all()  # Query the BlockedUsers table
        blockedusers_json = [
            {'id': user.id, 'username': user.username, 'telegram_id': user.telegram_id, 'message': user.message,
             'timestamp': user.timestamp.isoformat()} for user in blockedUsers]
        return blockedusers_json
