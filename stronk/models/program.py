from stronk import db
from stronk.models.user import User

class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=False)
    name = db.Column(db.String(128), index=True, nullable=False, unique=True)
    duration = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(256), nullable=False)    

    def to_dict(self):
        return {
            "id": self.id,
            "author": self.get_author(),
            "name": self.name,
            "duration": self.duration,
            "description": self.description
        }
        
    def get_author(self):
        return User.query.filter_by(id=self.author).first().to_dict()