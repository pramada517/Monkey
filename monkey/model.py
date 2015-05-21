from flask_sqlalchemy import SQLAlchemy

from monkey.database import db

friends = db.Table('friends',
    db.Column('monkey_id', db.Integer, db.ForeignKey('monkey.id')),
    db.Column('friend_id', db.Integer, db.ForeignKey('monkey.id'))
)
class Monkey(db.Model):
    __tablename__ = 'monkey'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    age = db.Column(db.Integer)
    email = db.Column(db.String(60))
    bestfriend_id = db.Column(db.Integer, db.ForeignKey("monkey.id"))
    friend = db.relationship('Monkey', 
                               secondary=friends, 
                               primaryjoin=(friends.c.monkey_id == id), 
                               secondaryjoin=(friends.c.friend_id == id), 
                               backref=db.backref('friends', lazy='dynamic'), 
                               lazy='dynamic')

    bestfriend = db.relationship('Monkey', uselist = False, remote_side = [id])

    def __init__(self, name, age, email, bestfriend_id):
        self.name = name
        self.age = age
        self.email = email
        self.bestfriend_id = bestfriend_id

    def __repr__(self):
        return '<Name %s>' % self.name

    def befriend(self, monkey):
        if not self.is_friend(monkey):
            self.friend.append(monkey)
            return self
        else:
            return None

    def unfriend(self, monkey):
        if self.is_friend(monkey):
            self.friend.remove(monkey)
            return self
        else:
            return None

    def is_friend(self, monkey):
        return self.friend.filter(
            friends.c.friend_id == monkey.id).count() > 0

    def are_bestfriends(self, monkey):
        return self.bestfriend == monkey

    def be_bestfriend(self, monkey):
        if not self.are_bestfriends(monkey):
            self.bestfriend = monkey

    def unbestfriend(self):
            self.bestfriend = None
