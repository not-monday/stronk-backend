from stronk import db
from stronk.models.user import User


class Weight(db.Model):
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        primary_key=True,
                        index=True,
                        nullable=False)
    weight = db.Column(db.Float, nullable=False)
    measured_at = db.Column(db.DateTime, primary_key=True, nullable=False)

    @classmethod
    def get_weights_by_user_id(cls, user_id):
        """Returns a list of all weights for a user with user id."""
        res = cls.query.filter_by(user_id=user_id)
        weights = []
        for row in res:
            weights.append({
                "measured_at": row.measured_at,
                "weight": row.weight
            })

        return {
            "user": self.get_user(user_id=user_id).to_dict(),
            "reviews": weights
        }

    def get_user(self, user_id=None):
        """Returns User object for the Weight. """
        u_id = user_id if user_id else self.user_id
        res = User.query.filter_by(id=u_id)
        if res:
            return res
        raise NoResultFound('User does not exist.')

    def to_dict(self):
        """Returns a dictionary representing the attributes of the
           ProgramReviews. Key is the name of the attribute and value is the
           value of the attribute."""
        return {
            "user_id": self.get_user().to_dict(),
            "weight": self.weight,
            "measured_at": self.measured_at
        }
