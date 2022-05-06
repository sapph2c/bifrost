from app import db


def create_database():
    """Creates the Agent and Commands tables in the backend database

    """
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    create_database()
