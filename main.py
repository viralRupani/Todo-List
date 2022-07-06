from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, current_user, UserMixin, LoginManager
from flask_bootstrap import Bootstrap
from form import Register, Login

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todolist-database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ADLFUIADFIOUAIU'
db = SQLAlchemy(app)
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# CREATE TABLE
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    todos = relationship('Todo', back_populates='todo_user')


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    todo_user = relationship('User', back_populates='todos')
    todo_ = db.Column(db.String(50), nullable=False)
    due_date = db.Column(db.String(12))


db.create_all()


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if current_user.is_authenticated:
            new_todo = Todo(
                user_id=current_user.id,
                todo_=request.form.get('add_new_task'),
                due_date=request.form.get('due_date')
            )
            db.session.add(new_todo)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            flash('Please Login before make Todo')
            return redirect(url_for('login'))
    else:
        if current_user.is_authenticated:
            todos = Todo.query.filter_by(user_id=current_user.id).all()
            return render_template('todolist.html', user=current_user, todos=todos)
        else:
            return render_template('index.html')


@app.route('/remove-todo/<todo_id>')
def remove_todo(todo_id):
    todo_to_delete = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


# @app.route('/new_user')
# def new_user():
#     return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    register_form = Register()
    if register_form.validate_on_submit():
        user = User.query.filter_by(email=register_form.email.data).first()
        if not user:
            if register_form.password.data == register_form.re_password.data:
                new_user = User(
                    username=register_form.username.data,
                    email=register_form.email.data,
                    password=generate_password_hash(password=register_form.password.data,
                                                    method="pbkdf2:sha256",
                                                    salt_length=8)
                )
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for('login'))
            else:
                flash('Password Field Does not Match!')
                return redirect(url_for('register'))
        else:
            flash('User already Exist with this email Login Instead')
            return redirect(url_for('register'))
    else:
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        else:
            return render_template('register.html', form=register_form)


@app.route('/login', methods=["POST", "GET"])
def login():
    login_form = Login()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and check_password_hash(pwhash=user.password, password=login_form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Credentials Wrond!')
            return redirect(url_for('login'))
    else:
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        else:
            return render_template('login.html', form=login_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
