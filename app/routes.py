#import libs and internal files
from flask import render_template, flash, redirect, url_for, request, session
from app import app, db
from app.models import User
from app.forms import LoginForm, RegistrationForm
from app.models import Game, User
from app.forms import PostForm
from app.models import Post
from flask import jsonify

#set route for / and /index to loginpage
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if "User" in session:
        return redirect(url_for('Uebersicht'))
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index'))
        session["User"] = form.username.data
        return redirect(url_for('Uebersicht'))
    return render_template("index.html", title='Dashboard', form=form)

#set route for /Detail
@app.route('/Detail/<id>', methods=['GET', 'POST'])
def Detail(id):
    form = PostForm()
    if "User" in session:
        if  form.validate_on_submit():
            user= User.query.filter_by(username=session["User"]).first()
            post= Post(post=form.post.data, game_id=id, user_id=user.id, rating=form.rating.data)
            db.session.add(post)
            db.session.commit()
            flash('post posted')
            return redirect(url_for('Detail', id=id))  
        else:
            game = Game.query.filter_by(id=id).first()
            #posts = Post.query.join(User, (User.id == Post.user_id)).filter(Post.game_id == id)
            #posts = db.session.query(Post).join(User, Post.user_id == User.id).filter(Post.game_id == id)
            posts = Post.query.filter_by(game_id=id)
            for post in posts:
                print(post)
            #print(posts)
            return render_template("Detail.html", game=game, posts=posts, form=form)
    else:
        return redirect(url_for('index'))

#set route for /Uebersicht (Dashboard)
@app.route('/Uebersicht')
def Uebersicht():
    if "User" in session:
        games = Game.query.all()
        return render_template("Uebersicht.html", games=games, user=session["User"])
    else:
        return redirect(url_for('index'))

#set route for /logout for redirection to index
@app.route('/logout')
def logout():
    if "User" in session:
        session.pop("User", None)
    return redirect(url_for('index'))

#set route for /Registrierung
@app.route('/Registrierung', methods=['GET', 'POST'])
def Registrierung():
    if "User" in session:
        return redirect(url_for('Uebersicht'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            return 'Please use a different username.'
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please login.')
        return redirect(url_for('index'))
    return render_template('Registrierung.html', title='Register', form=form)

#set route for /initialize (Game DB seeding)
@app.route('/initialize', methods=['GET', 'POST'])
def seed_gamedata():
    db.session.query(Game).delete()
    db.session.commit()
    game1 = Game(game='Organ Attack', photo_path='/static/organattack.jpg', filename='organattack.jpg', rating='9')
    game2 = Game(game='Uno', photo_path='/static/uno.jpg', filename='uno.jpg', rating='4')
    game3 = Game(game='Wingspan', photo_path='/static/wingspan.jpg', filename='wingspan.jgp', rating='9.5')
    db.session.add(game1)
    db.session.add(game2)
    db.session.add(game3)
    db.session.commit()
    return 'Seeding data has been added'

#set route for /api/getcomments (query comments)
@app.route('/api/getcomments')
def getcomments():
    comments= Post.query.all()
    return jsonify([x.todictcomments() for x in comments])

#set route for /api/getgames (query games)
@app.route('/api/getgames')
def getgames():
    games= Game.querry.all()
    return jsonify([x.todictgames() for x in games])
