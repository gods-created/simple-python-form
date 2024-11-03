from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles
import uvicorn

from middlewares import Error404Middleware

from routers import form_app

app = FastAPI(
    title='Application',
    version='0.0.1',
    redoc_url=None
)

app.mount('/static', StaticFiles(directory='static'), name='static')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

app.add_middleware(
    Error404Middleware
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(r: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=404,
        content=jsonable_encoder(
            {
                'detail': exc.errors()
            }
        )
    )
    
@app.exception_handler(HTTPException)
async def http_exception_handler(r: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(
            {
                'detail': exc.detail
            }
        )
    )

@app.get('/', tags=['No API'], name='Disable root router', status_code=302)
def root():
    return RedirectResponse('/form')
    
@app.get('/error404', tags=['No API', 'Errors'], name='Error 404', status_code=404)
def error404():
    return HTMLResponse(
        content='''
            <div style="display:flex;align-items:center;justify-content:center;height:100%;width:100%">
                <h2>ERROR 404. Page not found!</h2>
            </div>
        '''
    )
    
app.include_router(
    form_app
)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8001, reload=True)
