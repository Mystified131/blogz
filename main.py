from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Jackson1313@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    entry = db.Column(db.String(120))

    def __init__(self, name, entry):
        self.name = name
        self.entry = entry

@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect('/Blog')

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
        if not entry:
            errorentry = "Please submit and entry for the post"
        if errorname or errorentry:
            return render_template('newpost.html', errorname = errorname, errorentry = errorentry)
        else:
            Blog.name = name
            Blog.entry = entry
            new_entry = Blog(name, entry)
            db.session.add(new_entry)
            db.session.commit()
            newentry = db.session.query(id)
            return redirect("/Blog?id=" + newentry)

    return render_template('newpost.html', errorname = "", errorentry = "")

        







if __name__ == '__main__':
    app.run()