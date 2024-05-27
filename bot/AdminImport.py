from sqlalchemy.orm import sessionmaker
from DefineTables import Admins

class AdminImporter:
    def __init__(self, engine, allowed_users):
        self.session = sessionmaker(bind=engine)()
        self.allowed_users = allowed_users

    def import_admins(self):
        for user_id in self.allowed_users:
            existing_admin = self.session.query(Admins).filter_by(telegram_id=user_id).first()
            if existing_admin is None:
                new_admin = Admins(telegram_id=user_id)
                self.session.add(new_admin)

        self.session.commit()
        self.session.close()