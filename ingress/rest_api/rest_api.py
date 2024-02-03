from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, ValidationError, Json
app = FastAPI()
security = HTTPBasic()

allowed_users = [('admin','0')]

class Alert(BaseModel):
    key: str | None = None
    alert: dict | Json




@app.get("/")
async def root(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    if (str(credentials.username), str(credentials.password)) not in allowed_users:
        raise HTTPException(status_code=401, detail='Not Allowed')
    else:
        return {"message": "Hello World!"}

@app.post("/alert")
async def create_item(credentials: Annotated[HTTPBasicCredentials, Depends(security)], alert: Alert):
    if (str(credentials.username), str(credentials.password)) not in allowed_users:
        raise HTTPException(status_code=401, detail='Not Allowed')
    else:
        return alert
