from pydantic import BaseModel


class TaskDTO(BaseModel):
    taskId: str
    serverPath: str
    storagePath: str
    host: str
    port: int
    user: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str
