from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from passlib.handlers.sha2_crypt import sha512_crypt as crypto

from utils.models import RegisteredUsers, Base


# Connect to DB
engine = create_engine('sqlite:///samedw_mod/users.db')
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

def load_basic(username:str, password:str):
    # TODO add db check if user exist
    data = RegisteredUsers(username=username, password=crypto.hash(password))
    session.add(data)
    session.commit()
    return


if __name__ == "__main__":
    load_basic('user1@gmail.com', '12345')


