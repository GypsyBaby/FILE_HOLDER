from flask import request, redirect, flash, url_for
from flask_login import login_required, current_user
from src.core.usecases.upload_file_usecase import Usecase
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif", "xlsx"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@login_required
def upload_file(upload_usecase: Usecase):
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        try:
            owner_id = current_user.id
        except Exception as e:
            raise Exception(f"Error {e} while try to get user_id")
        if file and allowed_file(file.filename):
            file_hash = upload_usecase(file=file, owner_id=owner_id)
            return f"""File succesfully uploaded. Hash: {file_hash}"""
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    """