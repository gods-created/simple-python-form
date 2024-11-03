from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

from modules import User
from validators import UserData

form_app = APIRouter(
    tags=['Templates']
)

templates = Jinja2Templates(directory='templates')

@form_app.get('/form', name='Form page', status_code=200)
def form_page(r: Request):
    return templates.TemplateResponse(
        request=r, name='form.html', context={}
    )

@form_app.post('/form', name='Send form', status_code=200)
def send_form(user: UserData):
    user = user.to_json()
    
    with User() as module:
        response = module._save_user(user)

    return JSONResponse(
        content=response
    )
