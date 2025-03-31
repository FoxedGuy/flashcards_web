import logging
from src.user.model import DBUser, DBPrivilege
from src.database.core import create_db, check_all_tables, get_db_session
from src.user.connector import create_new_user

def create_privileges():
    with get_db_session() as db:
        privileges = db.query(DBPrivilege).all()
        if len(privileges) == 0:
            db.add(DBPrivilege(name="admin"))
            db.add(DBPrivilege(name="user"))
            db.commit()
            logging.info("Privileges created")
        else:
            logging.info("Privileges already exists")

def create_admin_user():
    with get_db_session() as db:
        user = db.query(DBUser).filter(DBUser.username == 'admin').first()
        if user is None:
            create_new_user(db,
                            "admin",
                            "admin_password",
                            "admin@admin",
                            db.query(DBPrivilege).filter(DBPrivilege.name == "admin").first().privilege_id)
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
    create_privileges()
    create_admin_user()
