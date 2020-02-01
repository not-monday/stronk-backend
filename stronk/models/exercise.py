from stronk import db

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, nullable=False, unique=True)
    description = db.Column(db.String(500), nullable=False)

    def to_dict(self):
        """Returns a dictionary representing the attributes of the program.
           Key is the name of the attribute and value is the value of the
           attribute. """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }
    
    def update(self, attrs):
        """Updates model given attrs.

        Params:
            attrs: Dictionary containing attributes to update. Key is the 
                   attribute name and value is the new value.
        """
        if attrs.get('name'):
            self.name = attrs.get('name')
        if attrs.get('description'):
            self.description = attrs.get('description')