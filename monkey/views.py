
from flask import Flask, render_template, abort, session, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from math import ceil

from monkey import app
from monkey.model import Monkey
from monkey.database import db

@app.route('/edit_friends/<int:val>', methods = ['POST'])
def friend(val):
     form = request.form
     friend_name = form["AddFriend"]
     res = Monkey.query.filter_by(id=val).first()
     res1 = Monkey.query.filter_by(name=friend_name).first()
     r = res.befriend(res1)
     if r:
         db.session.add(r)
         db.session.commit()
     return redirect(url_for('edit_friends', val=val))

@app.route('/unfriend/<int:m_id>/<int:f_id>', methods = ['GET'])
def unfriend(m_id, f_id):
     res = Monkey.query.filter_by(id=m_id).first()
     res1 = Monkey.query.filter_by(id=f_id).first()
     r = res.unfriend(res1)
     if r:
         db.session.add(r)
         db.session.commit()
     return redirect(url_for('edit_friends', val=m_id))

@app.route('/edit_friends/<int:val>', methods = ['GET'])
def edit_friends(val):
     res = Monkey.query.filter_by(id=val).first()
     res1 = db.session.execute(res.friend).fetchall()
     res2 = db.session.query(Monkey).filter(Monkey.id != val).all()
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
