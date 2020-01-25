from stronk import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    current_program = db.Column(db.Integer, db.ForeignKey('program.id'))

    def __repr__(self):
        return '<User {}>'.format(self.username)  