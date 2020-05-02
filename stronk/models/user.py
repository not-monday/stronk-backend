from stronk import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # TODO: change to string type
    name = db.Column(db.String(64), index=True, nullable=False)
    username = db.Column(db.String(64), index=True,
                         unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))  # TODO remove field
    current_program = db.Column(db.Integer, db.ForeignKey('program.id'))

    def to_dict(self):
        """Returns a dictionary representing the attributes of the program.
           Key is the name of the attribute and value is the value of the
           attribute. """
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "current_program": self.current_program
        }

    def update(self, attrs):
        """Updates model given attrs.

        Params:
            attrs: Dictionary containing attributes to update. Key is the 
                   attribute name and value is the new value.
        """
        if attrs.get('name'):
            self.name = attrs.get('name')
        if attrs.get('email'):
            self.email = attrs.get('email')
        if attrs.get('username'):
            self.username = attrs.get('username')
        if attrs.get('password_hash'):
            self.password_hash = attrs.get('password_hash')
        if attrs.get('current_program'):
            self.current_program = attrs.get('current_program')
