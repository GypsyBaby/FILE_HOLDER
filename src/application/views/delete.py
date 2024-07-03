from flask import request, redirect, flash
from flask_login import login_required, current_user
from src.core.usecases.delete_file_usecase import Usecase

@login_required
def delete_file(delete_usecase: Usecase):
    if request.method == "POST":
        file_name = request.form.get("file_name")
        if file_name is None:
            flash("Input hash of file!")
            return redirect(request.url)
        try:
            user_id = current_user.id
        except Exception as e:
            raise Exception(f"Error {e} while try to get user_id")
        try:
            delete_usecase(file_name=file_name, user_id=user_id)
        except Exception as e:
            raise Exception(f"Error `{e}` on deleting file with hash {file_name}")
        return f"""Succesfully!"""
    return """
    <!doctype html>
    <title>Delete File</title>
    <h1>Delete File</h1>
    <h2>Input file hash to delete</h2>
    <form method=post enctype=multipart/form-data>
      <input type=text name=file_name>
      <input type=submit value=Delete>
    </form>
    """