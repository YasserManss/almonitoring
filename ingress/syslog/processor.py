#!/opt/platform/python/python
import sys, json, os, redis
sys.path.append(os.path.dirname(__file__)+'/../../')
from common.config import get_redis_config, get_rest_api_config

#redis setup
redis_port = get_redis_config('port')
redis_pass = get_redis_config('requirepass')
redis_host='127.0.0.1'
redis_pool = redis.ConnectionPool(host=redis_host,port=redis_port,db=0,password=redis_pass)
###
SAFE_TYPES = (int, str, bool, bytes, float)
while True:
    for line in sys.stdin:
        r = redis.Redis(connection_pool=redis_pool)
        msg = line.strip().split('::')
        if len(msg) >2:
            del line
            try:
                alert = json.loads(msg[2])
                if isinstance(alert, dict):
                    alert = [alert]
                for a in alert:
                    log = a['alert']
                    log['timestamp']=msg[0]
                    log['source']=msg[1]
                    key = 'nokey'
                    if 'key' in a:
                        key = a['key']
                    r.incr(key, 1)
                    serial = r.get(key)
                    new_log = {
                            k: v if isinstance(v, SAFE_TYPES) else json.dumps(v)
                            for k, v in log.items()
                    }
                    r.hmset(key+':'+serial.decode(), new_log)
            except ValueError as e:
                r.incr('nokey', 1)
                serial = r.get('nokey')
                r.set('nokey:'+serial.decode(), 'xx'.join(msg))
                #pass as no key        

