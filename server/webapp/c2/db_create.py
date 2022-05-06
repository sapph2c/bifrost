import models


def create_database():
    """Creates the Agent and Commands tables in the backend database

    """
    models.db.create_all()
    models.db.session.commit()


if __name__ == "__main__":
    create_database()
