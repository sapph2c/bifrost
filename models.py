from app import db


class BlogPost(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)

    def __init__(self, title, description):
        self.title = title
        self.description = description

    def __repr__(self):
        return f"title: {self.title}, description: {self.description}"
