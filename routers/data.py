from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from utils.util import get_current_user_from_token
from utils.schemas import User

router = APIRouter(
    prefix="/data",
    tags=["data"],
    responses={404: {"description": "Not found"}},
)
templates = Jinja2Templates(directory='templates')

@router.get('/')
def dummy_data():
    return {'check out': 'all the data'}


### Private page
@router.get('/private', response_class=HTMLResponse)
def index(request:Request, user: User=Depends(get_current_user_from_token)):
    context = {'user':user, 'request':request}
    return templates.TemplateResponse('private.html', context)
