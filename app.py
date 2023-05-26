from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(30))
    category= db.Column(db.String,nullable=False)
    summary = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text,nullable=False)
    date = db.Column(db.DateTime,default=datetime.utcnow)
    
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/create',methods=["POST","GET"])
def create():
    if request.method == "POST":
        title=request.form['title']
        author=request.form['author']
        category=request.form['cat']
        summary=request.form['sum']
        content=request.form['con']
        new=Blog(title=title, author=author, category=category,summary=summary,content=content,date=datetime.now())
        db.session.add(new)
        db.session.commit()
    return redirect(url_for('all_blogs'))

@app.route('/search',methods=["POST","GET"])
def search():
    if request.method == "POST":
        search=request.form['search']
        search="%{}%".format(search)
        similar=Blog.query.filter(Blog.title.like(search)).all()
        return render_template('all_blogs.html',all_blogs=similar)

@app.route('/all_blogs')
def all_blogs():
    all_blogs = Blog.query.all()
    return render_template('all_blogs.html',all_blogs=all_blogs)

@app.route('/<int:id>')
def blog(id):
    blog=Blog.query.filter_by(id=id).one()
    return render_template('blog.html',blog=blog)

if (__name__=='__main__'):
    app.run(debug=True)