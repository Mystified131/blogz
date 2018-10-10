from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:Jackson1313@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'noginroirn48'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    entry = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, entry, owner_id):
        self.name = name
        self.entry = entry
        self.owner_id = owner_id

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index', 'Blog']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            flash("Logged in")
            return redirect('/newpost')
        elif not user:
            flash("User does not exist")
            return redirect('signup')
        else:
            flash('User password incorrect')

    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        if not email or not password or not verify:
            flash("Please fill in all form spaces")
            return redirect('/signup')
        if password != verify:
            flash("Password and Password Verify fields do not match")
            return redirect('/signup')
        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            flash("Signed In")
            return redirect('/newpost')
        else:
            flash('Duplicate User')
            return redirect('/signup')

    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/blog')

@app.route('/Blog', methods=['GET', 'POST'])
def blog():
    allentries = Blog.query.all()
    id = request.args.get('id')
    if id:
        entry = Blog.query.get(id)
        return render_template('entry.html', entry = entry)
    return render_template('Blog.html', entries=allentries)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        errorname = ""
        errorentry = ""
        name = request.form['name']
        if not name:
            errorname = "Please submit a name for the post"
        entry = request.form['entry']
        owner = User.query.filter_by(email=session['email']).first()
        owner_id = owner.id
        if not entry:
            errorentry = "Please submit and entry for the post"
        if errorname or errorentry:
            return render_template('newpost.html', errorname = errorname, errorentry = errorentry)
        else:
            new_entry = Blog(name, entry, owner_id)
            db.session.add(new_entry)
            db.session.commit()
            return render_template('entry2.html', name = name, entry = entry)

    return render_template('newpost.html', errorname = "", errorentry = "")

        







if __name__ == '__main__':
    app.run()