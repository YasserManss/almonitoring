import os
base = os.path.dirname(__file__)


def get_redis_config(key: str):
    content = ''
    with open(base+'/../conf/redis.conf','r') as f:
        content = f.read()
    import re
    parameter = re.findall(key+'(.*)', content)
    if parameter:
        return parameter[0].strip()
    else:
        return False



def get_rest_api_config(key: str):
    content = ''
    import yaml
    with open(base+'/../conf/rest_api.yaml','r') as f:
        content = yaml.safe_load(f.read())
    if key in content:
        return content[key]
    else:
        return False

