from typing import Annotated, List
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, ValidationError, Json, RootModel
import redis, sys, os
sys.path.append(os.path.dirname(__file__)+'/../../')
from common.config import get_redis_config, get_rest_api_config
app = FastAPI()
security = HTTPBasic()

#rest api setup
allowed_api_users = get_rest_api_config("allowed_users")
class Alert(BaseModel):
    key: str | None = None
    alert: dict | Json

class Alerts(RootModel):
    root : List[Alert]
    def __iter__(self):
        return iter(self.root)
    def __getitem__(self, item):
        return self.root[item]

###


#redis setup
redis_port = get_redis_config('port')
redis_pass = get_redis_config('requirepass')
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
async def create_item(credentials: Annotated[HTTPBasicCredentials, Depends(security)], alert: Alert | Alerts):
    if {str(credentials.username): str(credentials.password)} not in allowed_api_users:
        raise HTTPException(status_code=401, detail='Not Allowed')
    else:
        r = redis.Redis(connection_pool=redis_pool)
        if isinstance(alert, Alert):
            alert = [alert]
        for a in alert:
            default_key = 'nokey'
            if 'key' not in a:
                key = default_key
            r.incr(a.key, 1)
            serial = r.get(a.key)
            r.hmset(a.key+':'+serial.decode(), a.alert)
        return {"message": "Success"}
