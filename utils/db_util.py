from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils.schemas import User
from utils.models import RegisteredUsers


class UnitOfWork:
    def __init__(self):
        self.session_maker = sessionmaker(bind=create_engine('sqlite:///users.db', connect_args={'check_same_thread': False}))
    
    def __enter__(self):
        self.session = self.session_maker()
        return self
    
    def __exit__(self, exc_type, exc_val, traceback):
        if exc_type is None:
            self.rollback()
            self.session.close()
        self.session.close()
            
    def commit(self):
        self.session.commit()
        
    def rollback(self):
        self.session.rollback()

def get_user(username:str) -> User:
    with UnitOfWork() as unit_of_work:
        # Inst repository
        conn = unit_of_work.session
        db_data = conn.query(RegisteredUsers).filter(RegisteredUsers.username == username).first()
        
        if db_data is not None:
            response = db_data.dict_out()
            data = User(username=response['username'], hashed_password=response['password'])
            return data 

    return db_data


def set_new_user(username:str, password:str):
    with UnitOfWork() as unit_of_work:
        # Inst repository
        conn = unit_of_work.session
        data = RegisteredUsers(username=username, password=password)
        conn.add(data)
        conn.commit()
            
    return



