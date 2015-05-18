from os.path import abspath, dirname, join

from flask import Flask, render_template, abort, session, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from math import ceil

_cwd = dirname(abspath(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + join(_cwd, 'monkey.db')
db = SQLAlchemy(app)
SQLALCHEMY_ECHO = True
DEBUG = True

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

    def unfriend(self, monkey):
        if self.is_friend(monkey):
            self.friend.remove(monkey)
            return self

    def is_friend(self, monkey):
        return self.friend.filter(
            friends.c.friend_id == monkey.id).count() > 0

    def are_bestfriends(self, monkey):
        return self.bestfriend == monkey

    def be_bestfriend(self, monkey):
        if not self.are_bestfriends(monkey):
            self.bestfriend = monkey
            return self

    def unbestfriend(self):
            self.bestfriend = None
            return self 

@app.route('/befriend/<int:m_id>/<int:f_id>', methods = ['GET'])
def befriend(m_id, f_id):
     res = Monkey.query.filter_by(id=m_id).first()
     res1 = Monkey.query.filter_by(id=f_id).first()
     r = res.befriend(res1)
     db.session.add(r)
     db.session.commit()
     return redirect(url_for('index'))

@app.route('/unfriend/<int:m_id>/<int:f_id>', methods = ['GET'])
def unfriend(m_id, f_id):
     res = Monkey.query.filter_by(id=m_id).first()
     res1 = Monkey.query.filter_by(id=f_id).first()
     r = res.unfriend(res1)
     db.session.add(r)
     db.session.commit()
     return redirect(url_for('index'))

@app.route('/edit_friends/<int:val>', methods = ['GET'])
def edit_friends(val):
     res = Monkey.query.filter_by(id=val).first()
     res1 = db.session.execute(res.friend).fetchall()
     res2 = db.session.query(Monkey).filter(Monkey.id != val)
     return render_template('edit_friends.html',
                                 monkey = res, friends = res1, others = res2)

@app.route('/view_friends/<int:val>', methods = ['GET'])
def view_friends(val):
     res = Monkey.query.filter_by(id=val).first()
     res1 = db.session.execute(res.friend).fetchall()
     return render_template('view_friends.html',
                                 monkey = res, friends = res1)

@app.route('/add_monkey', methods = ['GET','POST'])
def add_monkey():
    #: Get the parsed contents of the form data
    if request.method == 'POST':
        form = request.form
        new_monkey = Monkey(form["Name"], form["Age"], form["Email"], 0)
        db.session.add(new_monkey)
        db.session.commit()
        monkey = Monkey.query.all()
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('add_monkey.html')
 
@app.route('/monkey/edit/<int:val>', methods = ['GET', 'POST'])
def edit_monkey(val):
    if request.method == 'POST':
        res = Monkey.query.filter_by(id=val).first()
        form = request.form
        res.name = form["Name"]
        res.age = form["Age"]
        res.email = form["Email"]
        bf_name = form["BestFriend"]
        bf = Monkey.query.filter_by(name=bf_name).first()
        if bf:
          res.be_bestfriend(bf)
        else:
          res.unbestfriend()

        db.session.commit()
        result = Monkey.query.all()
        return redirect(url_for('index'))
    elif request.method == 'GET':
        result = Monkey.query.filter_by(id=val).first()
        result2 = db.session.query(Monkey).filter(Monkey.id != val)
        return render_template('edit_monkey.html', monkey = result, others = result2)

@app.route('/monkey/view/<int:val>', methods = ['GET'])
def get_monkey(val):
     res = Monkey.query.filter_by(id=val).first()
     return render_template('view_monkey.html', monkey = res)

@app.route('/monkey/remove/<int:val>', methods = ['GET'])
def remove_monkey(val):
     res = Monkey.query.filter_by(id=val).first()
     db.session.delete(res)
     db.session.commit()
     return redirect(url_for('index'))

@app.route('/')
def index():
    monkey = Monkey.query.all()
    return render_template('index.html',
                           monkey = monkey)
 
if __name__ == '__main__':
    db.create_all()
    app.run()	

