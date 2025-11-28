from app.domain.user.repository import UserRepository

class UserService:
    def __init__(self,user_repository: UserRepository):
        self.user_repository = user_repository


    def list_users(self)->List[User]:
        return self.user_repository.list_users()