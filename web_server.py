import datetime
import json
from datetime import datetime, timedelta

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from jose import jwt, JWTError
from starlette.responses import RedirectResponse

import easyquotation.api
from easyquant.quotation import use_quotation
from t import get_t_price
from web.database import Database
from web.db_service import DbService
from web.dto import LoginRequest
from web.models import User
from web.settings import APISettings
from web.user_service import Token, route_data, UserService, oauth2_scheme, TokenData, UserModel

# fix mimetypes error, default .js is text/plain
import mimetypes
mimetypes.add_type("application/javascript; charset=utf-8", ".js")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000

app = FastAPI()
settings = APISettings()
database = Database()
db_service = DbService(settings, database)
user_service = UserService(db_service)
quotation = use_quotation('jqdata')
online_quotation = easyquotation.api.use('qq')

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = user_service.get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/")
async def root():
    return RedirectResponse("/static/index.html")


@app.post("/api/watch_stocks/{code}")
def watch_stock(code: str = Path(..., title="The stock code to watch")):
    security = quotation.get_stock_info(code)
    price = quotation.get_price(code, date=datetime.now())
    dbitem = db_service.watch_stock(code, security.name, price)
    return {
        'error': 0,
        'data': dbitem
    }


@app.delete("/api/watch_stocks/{code}")
def watch_stock(code: str = Path(..., title="The stock code to remove")):
    db_item = db_service.remove_stock(code)
    return {
        'error': 0,
        'data': db_item
    }


@app.get("/api/stocks")
async def get_stocks(current_user: User = Depends(get_current_active_user)):
    stocks = db_service.get_watch_stocks(current_user.username)
    codes = [stock.code for stock in stocks]
    data = online_quotation.real(codes)
    data = list(data.values())
    for stock in data:
        stock['t_price'] = get_t_price(stock['code'])
    return data


@app.post("/api/login", response_model=Token)
async def login_for_access_token(login: LoginRequest):
    user = user_service.authenticate_user(login.username, login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = user_service.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/api/me/", response_model=UserModel)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    user = UserModel(
        email=current_user.email,
        full_name=current_user.full_name,
        roles=json.loads(current_user.roles),
        username=current_user.username,
        disabled=False)
    return user


@app.get("/api/route")
async def read_user_routes(current_user: User = Depends(get_current_active_user)):
    assert current_user is not None
    return route_data


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
