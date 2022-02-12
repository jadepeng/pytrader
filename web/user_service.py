from datetime import datetime, timedelta
from typing import Optional, List

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from web.db_service import DbService

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

route_data = [
    {
        "id": 2,
        "parentId": 0,
        "name": 'Project',
        "path": '/Project',
        "component": 'Layout',
        "redirect": '/Project/ProjectList',
        "meta": {"title": '项目管理', "icon": 'el-icon-phone'}
    },
    {
        "id": 20,
        "parentId": 2,
        "name": 'ProjectList',
        "path": '/Project/ProjectList',
        "component": 'ProjectList',
        "meta": {"title": '项目列表', "icon": 'el-icon-goods'}
    },
    {
        "id": 21,
        "parentId": 2,
        "name": 'ProjectDetail',
        "path": '/Project/ProjectDetail/:projName',
        "component": 'ProjectDetail',
        "meta": {"title": '项目详情', "icon": 'el-icon-question', "activeMenu": '/Project/ProjectList', "hidden": True}
    },
    {
        "id": 22,
        "parentId": 2,
        "name": 'ProjectImport',
        "path": '/Project/ProjectImport',
        "component": 'ProjectImport',
        "meta": {"title": '项目导入', "icon": 'el-icon-help'}
    },
    {
        "id": 3,
        "parentId": 0,
        "name": 'Nav',
        "path": '/Nav',
        "component": 'Layout',
        "redirect": '/Nav/SecondNav/ThirdNav',
        "meta": {"title": '多级导航', "icon": 'el-icon-picture'}
    },
    {
        "id": 30,
        "parentId": 3,
        "name": 'SecondNav',
        "path": '/Nav/SecondNav',
        "redirect": '/Nav/SecondNav/ThirdNav',
        "component": 'SecondNav',
        "meta": {"title": '二级导航', "icon": 'el-icon-camera', "alwaysShow": True}
    },
    {
        "id": 300,
        "parentId": 30,
        "name": 'ThirdNav',
        "path": '/Nav/SecondNav/ThirdNav',
        "component": 'ThirdNav',
        "meta": {"title": '三级导航', "icon": 'el-icon-s-platform'}
    },
    {
        "id": 31,
        "parentId": 3,
        "name": 'SecondText',
        "path": '/Nav/SecondText',
        "redirect": '/Nav/SecondText/ThirdText',
        "component": 'SecondText',
        "meta": {"title": '二级文本', "icon": 'el-icon-s-opportunity', "alwaysShow": True}
    },
    {
        "id": 310,
        "parentId": 31,
        "name": 'ThirdText',
        "path": '/Nav/SecondText/ThirdText',
        "component": 'ThirdText',
        "meta": {"title": '三级文本', "icon": 'el-icon-menu'}
    },
    {
        "id": 4,
        "parentId": 0,
        "name": 'Components',
        "path": '/Components',
        "component": 'Layout',
        "redirect": '/Components/OpenWindowTest',
        "meta": {"title": '组件测试', "icon": 'el-icon-phone'}
    },
    {
        "id": 40,
        "parentId": 4,
        "name": 'OpenWindowTest',
        "path": '/Components/OpenWindowTest',
        "component": 'OpenWindowTest',
        "meta": {"title": '选择页', "icon": 'el-icon-goods'}
    },
    {
        "id": 41,
        "parentId": 4,
        "name": 'CardListTest',
        "path": '/Components/CardListTest',
        "component": 'CardListTest',
        "meta": {"title": '卡片列表', "icon": 'el-icon-question'}
    },
    {
        "id": 42,
        "parentId": 4,
        "name": 'TableSearchTest',
        "path": '/Components/TableSearchTest',
        "component": 'TableSearchTest',
        "meta": {"title": '表格搜索', "icon": 'el-icon-question'}
    },
    {
        "id": 43,
        "parentId": 4,
        "name": 'ListTest',
        "path": '/Components/ListTest',
        "component": 'ListTest',
        "meta": {"title": '标签页列表', "icon": 'el-icon-question'}
    },
    {
        "id": 5,
        "parentId": 0,
        "name": 'Permission',
        "path": '/Permission',
        "component": 'Layout',
        "redirect": '/Permission/Directive',
        "meta": {"title": '权限管理', "icon": 'el-icon-phone', "alwaysShow": True}
    },
    {
        "id": 50,
        "parentId": 5,
        "name": 'Directive',
        "path": '/Permission/Directive',
        "component": 'Directive',
        "meta": {"title": '指令管理', "icon": 'el-icon-goods'}
    }
]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    roles: List[str] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


class UserService:
    def __init__(self, db_service: DbService):
        self.db_service = db_service

    def get_user(self, username: str):
        return self.db_service.get_user(username)

    def authenticate_user(self, username: str, password: str):
        user = self.get_user(username)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def get_current_user(self, token: str = Depends(oauth2_scheme)):
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
        user = self.get_user(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

    async def get_current_active_user(self, current_user: User = Depends(get_current_user)):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
