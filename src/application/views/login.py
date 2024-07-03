from flask import request, redirect, flash, url_for, render_template
from flask_login import login_user
from flask_bcrypt import Bcrypt

from src.application.forms.login import LoginForm
from src.core.dto.user import UserFilter
from src.data.repository.psql import PSQLSyncRepo
from src.application.login_tools.user import UserClass


def login(repo: PSQLSyncRepo, bc: Bcrypt):
    form = LoginForm(request.form)
    if form.validate_on_submit():
        # user login processing
        username = request.form.get("username", "", type=str)
        password = request.form.get("password", "", type=str)
        user = repo.get_user(fltr=UserFilter(login=username))
        if user is None:
            return """Invalid username"""
        user_obj = UserClass(id=user.id, login=user.login)
        if bc.check_password_hash(user.password, password):
            try:
                login_user(user_obj)
            except Exception as e:
                flash("Error while logging process")

            flash("You've been logged in!", "success")
            return redirect(url_for("upload_file"))
        else:
            flash("Your email or password doesn't match!", "error")
    return render_template("login.html", form=form)
