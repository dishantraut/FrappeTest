""" applicaiton running file """

from uuid import uuid4
from json import loads
from functools import wraps
from secrets import token_urlsafe
from flask import Flask, render_template, request, flash, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
from peewee import IntegrityError
from models import Books, Users
from req import make_http_request
from utils import check_password_strong, validate_email


################ * Application Configurations * ################


app = Flask(__name__, template_folder='./templates', static_folder='./static')
app.config.from_object(__name__)
app.config['SECRET_KEY'] = token_urlsafe(32)
LOGIN_DATA = False

################ * Custom Functions * ################


def custom_flash(message, category=None):
    """ Custom flash messages """
    flash({'message': message, 'category': category})


def validate_user_data(user_data):
    """
    Validate user registration data (add checks for email format, username uniqueness, etc.)

    Args:
        user_data (dict): A hasmap of data submitted by user during registration

    Returns:
        errors: if, any errors are detected a list of erros is returned
    """

    errors = []
    # * Implement email validation logic here (e.g., using a regular expression)
    if not validate_email(user_data.get('email')):
        errors.append("Invalid email format")

    # * Check for existing username
    if Users.select().where(Users.username == user_data.get('username')).exists():
        errors.append("Username already exists")

    # * Add more validation rules as needed (password strength, etc.)
    if check_password_strong(user_data.get('password')):
        errors.append(
            f"Password must be strong: {check_password_strong(user_data.get('password'))}"
            )

    if len(errors) == 0:
        return True
    else:
        return errors

################ * Applicatoin Functions * ################


def login_required(f):
    """ check if logged in or not """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "token" not in session and "username" not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.errorhandler(404)
def not_found(e):
    """ page not found """
    return render_template("error.html")


################ * All Routes * ################


@app.get('/register')
@app.post('/register')
def register():
    """ registration of new user """
    if request.method == 'POST':
        user_data = request.form.to_dict()
        print(user_data)
        vud = validate_user_data(user_data)
        print(vud)
        try:
            if vud:
                match_pwd = user_data.get('password') == user_data.get('confirm_password')
                if match_pwd:
                    Users.create(
                        email=user_data.get('email'),
                        username=user_data.get('username'),
                        pw_hash=generate_password_hash(user_data.get('password'))
                    )
                    custom_flash("User created", "success")
                    return render_template('login.html')
        except IntegrityError as err:
            custom_flash(f"{vud}!", "error")
            custom_flash(f"{err}!", "error")
    return render_template('register.html')


@app.get('/login')
@app.post('/login')
def login():
    """ login page """
    if request.method == "POST":
        form_data = request.form.to_dict()
        try:
            user_data = [k for k in Users.select().where(Users.username == form_data.get('username')).dicts()][0]
            if check_password_hash(user_data.get('pw_hash'), form_data.get('password')):
                session['token'] = uuid4()
                session['username'] = user_data.get('username')
                session['email'] = user_data.get('email')
                session['role'] = 'root'
                session['id'] = user_data.get('id')
                del form_data
                custom_flash(f"Login Success @ {user_data.get('username')}", "success")
                return redirect(url_for('all_books'))
        except Exception as err:
            custom_flash(f"{err}", "error")
    return render_template('login.html')


@app.get('/logout')
@app.post('/logout')
@login_required
def logout():
    """ logout page """
    custom_flash("You were logged out..!!", "success")
    session.pop('token', None)
    session.pop('username', None)
    return render_template('base.html')


@app.get('/all_books')
@app.put('/all_books')
@app.post('/all_books')
@app.delete('/all_books')
@login_required
def all_books():
    """ home page """
    form_data = request.form.to_dict()
    if request.method == "PUT":
        print(f"PUT = {form_data}")
    elif request.method == "POST":
        print(f"POST = {form_data}")
    elif request.method == "DELETE":
        print(f"DELETE = {form_data}")

    array_book = Books.select()
    return render_template('home.html', books=array_book)


@app.get('/get_data')
@login_required
def get_data():
    """ get books data """
    Books.truncate_table()
    # for each_page_no in range(2, 100):
    # url_to_ping = f"https://frappe.io/api/method/frappe-library?page={each_page_no}&title=and"
    url_to_ping = "https://frappe.io/api/method/frappe-library?page=2&title=and"
    result_json = make_http_request(url=url_to_ping, method='GET')
    if result_json:
        result_dict = loads(result_json)
    try:
        for each_record in result_dict.get('message'):
            Books.create(**each_record)
    except IntegrityError as err:
        custom_flash(f"{err}", "error")
    custom_flash("Data Load Done..!!!", "success")
    return render_template('base.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6060, debug=True)
