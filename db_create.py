from app import db
from models import Agent

# create the database and the db tables
db.create_all()
#
# # insert
# # db.session.add(BlogPost("Good", "I\'m good."))
# # db.session.add(BlogPost("Well", "I\'m well."))
# db.session.add(Agent("Windows", "Ashley-PC", "192.168.1.1", "64 GB"))
#
# # commit the changes
db.session.commit()


