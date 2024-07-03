from dependency_injector import containers, providers
from dependency_injector.ext import flask
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from settings import settings

from src.application.views.download import download_file
from src.application.views.delete import delete_file
from src.application.views.upload import upload_file
from src.application.views.login import login
from src.application.views.logout import logout
from src.core.components.file_manager import FileManager
from src.core.components.hash import HashComponent
from src.core.usecases import upload_file_usecase, delete_file_usecase, download_file_usecase

from src.application.database.psql.db import sa_create_engine, SessionSyncFactory, SessionSyncWrapper
from src.data.repository.psql import PSQLSyncRepo

class ApplicationContainer(containers.DeclarativeContainer):
    """Application container."""

    app = flask.Application(Flask, __name__)
    bc = flask.Extension(Bcrypt, app)
    login_manager = flask.Extension(LoginManager)

    file_manager = providers.Factory(FileManager, root_dir=settings.UPLOAD_FOLDER)
    hash_component = providers.Factory(HashComponent, hash_alg=settings.HASH_ALGORITM)
    engine = providers.Factory(sa_create_engine, url=settings.DATABASE_SYNC_URL)
    ssf = providers.Factory(SessionSyncFactory, engine=engine)
    ssw = providers.Factory(SessionSyncWrapper, factory=ssf)
    repo = providers.Factory(PSQLSyncRepo, session_wrapper=ssw)
    upload_usecase = providers.Factory(
        upload_file_usecase.Usecase,
        hash_component=hash_component,
        file_manager=file_manager,
        repo=repo,
    )
    delete_usecase = providers.Factory(
        delete_file_usecase.Usecase,
        file_manager=file_manager,
        repo=repo,
    )
    download_usecase = providers.Factory(
        download_file_usecase.Usecase,
        file_manager=file_manager,
        repo=repo,
    )
    download_view = flask.View(download_file, download_usecase=download_usecase)
    upload_view = flask.View(upload_file, upload_usecase=upload_usecase)
    delete_view =  flask.View(delete_file, delete_usecase=delete_usecase)
    login_view = flask.View(login, repo=repo, bc=bc)
    logout_view = flask.View(logout)
