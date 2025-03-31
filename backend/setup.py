import logging
from backend.src.user.model import DBUser
from src.database.core import create_db, check_all_tables, get_db_session
from src.user.connector import create_new_user

def create_admin_user():
    with get_db_session() as db:
        user = db.query(DBUser).filter(DBUser.username == 'admin').first()
        if user is None:
            create_new_user(db,
                            "admin",
                            "admin_password",
                            "admin@admin")
            logging.info("Admin user created")
        else:
            logging.info("Admin user already exists")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Checking if all tables exists")
    logging.info(check_all_tables())
    if not all(check_all_tables()):
        logging.info("Creating database")
        create_db()
        logging.info("Database created")
    else:
        logging.info("All tables exists")
        logging.info("Nothing to do")
    logging.info("Creating admin user")
    create_admin_user()
