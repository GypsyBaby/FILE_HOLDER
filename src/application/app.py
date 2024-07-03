from settings import settings
from src.application.container import ApplicationContainer
from src.application.login_tools.user_loader import check_db


def create_app():

    container = ApplicationContainer()
    app = container.app()
    app.container = container

    lm = container.login_manager()
    lm.init_app(app)

    @lm.user_loader
    def load_user(user_id):
        return check_db(user_id=user_id, repo=container.repo())

    app.secret_key = settings.SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_SYNC_URL
    app.debug = settings.DEBUG
    app.add_url_rule(
        "/download",
        methods=["GET", "POST"],
        view_func=container.download_view.as_view(),
    )
    app.add_url_rule(
        "/upload", methods=["GET", "POST"], view_func=container.upload_view.as_view()
    )
    app.add_url_rule(
        "/delete", methods=["GET", "POST"], view_func=container.delete_view.as_view()
    )
    app.add_url_rule(
        "/login", methods=["GET", "POST"], view_func=container.login_view.as_view()
    )
    app.add_url_rule(
        "/logout", methods=["GET", "POST"], view_func=container.logout_view.as_view()
    )

    return app
