from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
import sqlite3
from flask_sqlalchemy import SQLAlchemy

class MyForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    rating = DecimalField('Rating', places=1, validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditForm(FlaskForm):
    new_rating = DecimalField('New Rating', validators=[DataRequired()])
    submit = SubmitField('Submit')

db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"
db.init_app(app)
bootstrap = Bootstrap5(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=False, nullable=False)
    rating = db.Column(db.Float, unique=False, nullable=False)

all_books = []


@app.route('/')
def home():
    all_books = db.session.execute(db.select(Book).order_by(Book.title)).scalars()
    return render_template('index.html', all_books = all_books)


@app.route("/add", methods=["POST", 'GET'])
def add():
    addForm = MyForm()
    if addForm.validate_on_submit():
        with app.app_context():
            new_book = Book(title=addForm.title.data, author=addForm.author.data, rating=float(addForm.rating.data))
            db.session.add(new_book)
            db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=addForm)

@app.route('/edit', methods=['POST', 'GET'])
def edit(id):
    edit_form = EditForm()
    if edit_form.validate_on_submit():
        book_id = request.form['id']




if __name__ == "__main__":
    app.run(debug=True, port=9000)

