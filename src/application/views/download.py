from flask import request, redirect, flash
from src.core.usecases.download_file_usecase import Usecase


def download_file(download_usecase: Usecase):
    if request.method == "POST":
        file_name = request.form.get("file_name")
        if file_name is None:
            flash("Input hash of file!")
            return redirect(request.url)
        try:
            result = download_usecase(file_name=file_name)
            if result is None:
                return """No file this what hash"""
            return result
        except Exception as e:
            raise Exception(f"Error `{e}` on download file with hash {file_name}")
    return """
    <!doctype html>
    <title>Download File</title>
    <h1>Download File</h1>
    <h2>Input file hash to download</h2>
    <form method=post enctype=multipart/form-data>
      <input type=text name=file_name>
      <input type=submit value=Download>
    </form>
    """
