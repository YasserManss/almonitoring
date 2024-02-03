from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, ValidationError, Json
import redis
app = FastAPI()
security = HTTPBasic()

#rest api setup
allowed_api_users = [('admin','0')]
class Alert(BaseModel):
    key: str | None = None
    alert: dict | Json
###

# redis setup
redis_port = 6379
redis_pass = 'redis'
redis_host='127.0.0.1'
redis_pool = redis.ConnectionPool(host=redis_host,port=redis_port,db=0,password=redis_pass)
###



@app.get("/")
async def root(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    if (str(credentials.username), str(credentials.password)) not in allowed_api_users:
        raise HTTPException(status_code=401, detail='Not Allowed')
    else:
        return {"message": "Hello World!"}

@app.post("/alert")
async def create_item(credentials: Annotated[HTTPBasicCredentials, Depends(security)], alert: Alert):
    if (str(credentials.username), str(credentials.password)) not in allowed_api_users:
        raise HTTPException(status_code=401, detail='Not Allowed')
    else:
        print('here')
        r = redis.Redis(connection_pool=redis_pool)
        print(r.ping())
        default_key = 'nokey'
        if 'key' not in alert:
            key = default_key
        r.incr(key, 1)
        serial = r.get(key)
        r.hmset(key+':'+serial.decode(), alert.alert)
        return alert
