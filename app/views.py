from flask import render_template, url_for, redirect, request, make_response
from app import app, data
from .forms import RegistrationForm, CategoryForm, RecordForm

from . import model
from datetime import datetime


@app.route("/")
def index():
    return redirect(url_for("registration"), code=302)


@app.route("/registration")
def registration():
    form = RegistrationForm()
    return render_template("registration.html", form=form)


@app.route("/category")
def category():
    form = CategoryForm()
    return render_template("category.html", form=form)


@app.route("/record")
def record():
    user_name = request.args.get("name")
    if user_name is not None and user_name not in [user.get_name() for user in data["users"]]:
        return f'''<h3>No such user {user_name}</h3><a href="/users"><input type="button" value="go to users"></a>'''

    users = [user.get_name() for user in data["users"]]
    categories = [category.get_type() for category in data["categories"]]
    form = RecordForm()

    return render_template("record.html", form=form, user_name=user_name, users=users, categories=categories)


@app.route("/users/user", methods=("GET", "POST"))
def user_page():
    if request.method == "GET":
        name = request.args.get("name")

        if name not in [user.get_name() for user in data["users"]]:
            return f'''<h3>No such user {name}</h3><a href="/users"><input type="button" value="go to users"></a>'''

        categories = [category.get_type() for category in data["categories"]]
        records = [record for record in data["records"] if record.get_user().get_name() == name]
        category = request.args.get("category")

        if category in [cat.get_type() for cat in data["categories"]]:
            records = [record for record in records if record.get_category().get_type() == category]

        return render_template("userpage.html", categories=categories, name=name, records=records)

    else:
        user_name = request.form.get("user")
        if user_name not in [user.get_name() for user in data["users"]]:
            return f'''<h3>No such user {user_name}</h3><a href="/users">
            <input type="button" value="go to users"></a>'''

        user = [user for user in data["users"] if user.get_name() == user_name][0]

        category_type = request.form.get("category")
        if category_type not in [category.get_type() for category in data["categories"]]:
            return f'''<h3>No such category {category_type}</h3><a href="/users">
            <input type="button" value="go to users"></a> '''

        category = [category for category in data["categories"] if category.get_type() == category_type][0]

        try:
            date_format = "%Y-%m-%d %H:%M:%S"
            date_time = datetime.strptime(request.form.get("date_time"), date_format)
        except ValueError:
            return '''<h3>Неправильний формат дати/часу</h3>
                      <h4>Приклад форматування: 2020-01-01 22:00:00</h4>'''

        pay = int(request.form.get("pay"))

        record = model.Record(user, category, date_time, pay)
        data["records"].append(record)

        return f'''<h3>Record {str(record)} is successfully added</h3>
            <a href="/users/user?name={user_name}">Особистий кабінет</a>'''


@app.route("/users", methods=("GET", "POST"))
def users():
    if request.method == "POST":
        submit = request.form.get("submit")
        if submit == "Створити":
            username = request.form.get("username")
            data["users"].append(model.User(username))

            f = open("app/resources/users.txt", "a")
            f.write(username + "\n")
            f.close()

            return f'''<h3>User {username} is successfully created</h3>
            <a href="/users/user?name={username}">Особистий кабінет</a>'''

        elif submit == "Додати":
            category_type = request.form.get("category_name")
            data["categories"].append(model.Category(category_type))

            return f'''<h3>Category {category_type} is successfully added</h3>
            <a href="/users">Всі користувачі</a>'''

    all_users = data["users"]
    all_categories = data["categories"]
    return render_template("users.html", users=all_users, categories=all_categories)

