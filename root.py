from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from utils.exception import NotAuthenticatedException

#from samedw_mod import secure
#from samedw_mod import data
import routers.secure as secure
import routers.data as data


app = FastAPI()

app.include_router(secure.router)
app.include_router(data.router)



@app.get("/")
async def root():
    return {"message": "Trying Routers"}

@app.exception_handler(NotAuthenticatedException)
def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
    """
    Redirect the user to the login page if not logged in
    """
    return RedirectResponse(url='auth/login')