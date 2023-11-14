from typing import Dict, List, Optional

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from passlib.handlers.sha2_crypt import sha512_crypt as crypto

from rich.console import Console
console = Console()

from utils.util import create_access_token, authenticate_user, get_current_user_from_cookie, get_current_user_from_token
from utils.db_util import set_new_user
from utils.schemas import User

import os
from dotenv import load_dotenv

load_dotenv()

COOKIE_NAME = os.getenv('COOKIE_NAME')

"""
Login file modified.
1. Change error handling in OAuth class to redirect
2. Added signup and "mod" DB
3. Put sectret in .env file
4. Split up on files
5. Put users in proper database
6. Split up api with router
7.
"""

router = APIRouter(
    prefix="/secure",
    tags=["secure"],
    )
templates = Jinja2Templates(directory='templates')



@router.post('/token')
def login_for_access_token(response:Response, form_data:OAuth2PasswordRequestForm=Depends()) -> Dict[str, str]:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')
    access_token  = create_access_token(data={'username': user.username})
    
    # Set cookie in the response
    response.set_cookie(key=COOKIE_NAME, value=f'Bearer {access_token}', httponly=True)

    return {COOKIE_NAME: access_token, 'token_type':'bearer'}


### Home page
@router.get('/', response_class=HTMLResponse)
def index(request:Request):
    try:
        user = get_current_user_from_cookie(request)
    except:
        user=None
    console.log(f'[blue] {user}')
    context = {"user": user, 'request':request}    
    return templates.TemplateResponse('index.html', context)
            

### Private page
@router.get('/private', response_class=HTMLResponse)
def index(request:Request, user: User=Depends(get_current_user_from_token)):
    context = {'user':user, 'request':request}
    return templates.TemplateResponse('private.html', context)

@router.get('/data')
def dummy_data(request:Request, user: User=Depends(get_current_user_from_token)):
    return {'check out': 'all the data'}


### Login - GET
@router.get('/auth/login', response_class=HTMLResponse)
def login_get(request:Request):
    context = {'request': request}
    return templates.TemplateResponse('login.html', context)


### Login - POST
class LoginForm:
    def __init__(self, request:Request):
        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None
        self.oassword: Optional[str] = None
    
    async def load_data(self):
        form = await self.request.form()
        self.username = form.get('username')
        self.password = form.get('password')
        
    async def is_valid(self):
        if not self.username or not (self.username.__contains__("@")):
            self.errors.append('Email is required')
        if not self.password or not len(self.password) >= 4:
            self.errors.append('A valid password is required')
        if not self.errors:
            return True
        return False
    
@router.post('/auth/login', response_class=HTMLResponse)
async def login_post(request:Request):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            response = RedirectResponse('/secure', status.HTTP_302_FOUND)
            login_for_access_token(response=response, form_data=form)
            form.__dict__.update(msg='Login Successful')
            console.log('[green]Login successfull')
            return response
        except HTTPException:
            form.__dict__.update(msg='')
            form.__dict__.get('errors').append('Incorrect Email or Password')
            return templates.TemplateResponse('login.html', form.__dict__)
    return templates.TemplateResponse('login.html', form.__dict__)


### Sign-up get
@router.get('/auth/signup', response_class=HTMLResponse)
async def signup_get(request:Request):
    return templates.TemplateResponse('signup.HTML', {'request':request})

### Signup post
@router.post('/auth/signup', response_class=HTMLResponse)
async def signup_post(request:Request):
    form = await request.form()
    username = form.get('username')
    password =  form.get('password')
    
    set_new_user(username=username, password=crypto.hash(password))
    
    return RedirectResponse('/secure', status.HTTP_302_FOUND)
 

### Logout
@router.get('/auth/logout', response_class=HTMLResponse)
def logout_get():
    response = RedirectResponse(url='/secure')
    response.delete_cookie(COOKIE_NAME)
    return response



