from stronk import db
from stronk.models.user import User


class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(),
                       db.ForeignKey('user.id'),
                       index=True,
                       nullable=False)
    name = db.Column(db.String(128), index=True, nullable=False, unique=True)
    duration = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(256), nullable=False)

    def to_dict(self):
        """Returns a dictionary representing the attributes of the program.
           Key is the name of the attribute and value is the value of the
           attribute. """
        return {
            "id": self.id,
            "author": self.get_author(),
            "name": self.name,
            "duration": self.duration,
            "description": self.description
        }

    def get_author(self):
        """Returns the User object for the author of the program."""
        return User.query.filter_by(id=self.author).first().to_dict()

    def update(self, attrs):
        """Updates model given attrs.

        Params:
            attrs: Dictionary containing attributes to update. Key is the 
                   attribute name and value is the new value.
        """
        if attrs.get('author'):
            self.author = attrs.get('author')
        if attrs.get('name'):
            self.name = attrs.get('name')
        if attrs.get('duration'):
            self.duration = attrs.get('duration')
        if attrs.get('description'):
            self.description = attrs.get('description')
