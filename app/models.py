from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login

class User(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(255), index=True, unique=True)
    email= db.Column(db.String(255), index=True, unique=True)
    password_hash= db.Column(db.String(255))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
   

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Game(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    game= db.Column(db.String(255))
    photo_path= db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    rating= db.Column(db.Float, nullable=True)

    def todict(self):
        return dict(id = self.id, game = self.game, photo_path= self.photo_path, rating= self.rating)
    
class Post(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    game_id= db.Column(db.Integer, db.ForeignKey('game.id'))
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))
    post= db.Column(db.Text, nullable=False)
    date= db.Column(db.DateTime, index=True, default=datetime.utcnow)
    rating= db.Column(db.Integer)

    def __repr__(self):
        return '<post {}>'.format(self.post)
    
    def todict(self):
        return dict(id = self.id, post = self.post, date= self.date, rating= self.rating)
