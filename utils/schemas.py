from pydantic import BaseModel
from typing import List


### Models and Data
class User(BaseModel):
    username: str
    hashed_password: str
    

### Create a user database
class DataBase(BaseModel):
    user: List[User]



    

