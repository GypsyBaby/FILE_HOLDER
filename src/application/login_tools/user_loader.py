from src.application.login_tools.user import UserClass
from src.core.dto.user import UserFilter
from src.data.repository.psql import PSQLSyncRepo


def check_db(user_id: int, repo: PSQLSyncRepo):
    user_model = repo.get_user(fltr=UserFilter(id=user_id))
    if user_model is not None:
        return UserClass(id=user_model.id, login=user_model.login)
