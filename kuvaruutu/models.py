from kuvaruutu import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    image = db.Column(db.LargeBinary, default=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    visible = db.Column(db.Boolean, default=1)

    def __init__(self, username, image, password):
        self.username = username
        self.image = image
        self.password = password

    def __repr__(self):
        return f'User("{self.username}"'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text)
    user_id = db.relationship