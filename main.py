from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
import sqlite3
from flask_sqlalchemy import SQLAlchemy

class MyForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    rating = StringField('Rating', validators=[DataRequired()])
    submit = SubmitField('Submit')


'''
Red underlines? Install the required packages first:
Open the Terminal in PyCharm (bottom left).

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''
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

with app.app_context():
    db.create_all()

# with app.app_context():
#     new_book = Book(title="Goosebumps", author="R.L. Stein", rating=9.5)
#     db.session.add(new_book)
#     db.session.commit()




all_books = []


@app.route('/')
def home():
    return render_template('index.html', all_books = all_books)


@app.route("/add", methods=["POST", 'GET'])
def add():
    addForm = MyForm()
    if addForm.validate_on_submit():
        form_data = {
            "title": addForm.title.data,
            "author": addForm.author.data,
            'rating': addForm.rating.data
        }
        all_books.append(form_data)
        return redirect(url_for('home'))
        print(all_books)
    return render_template('add.html', form=addForm)


if __name__ == "__main__":
    app.run(debug=True, port=9000)

