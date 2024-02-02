from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()

allowed_users = [('admin','0')]


@app.get("/")
async def root(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    if (str(credentials.username), str(credentials.password)) not in allowed_users:
        raise HTTPException(status_code=401, detail='Not Allowed')
    else:
        return {"message": "Hello World!"}
