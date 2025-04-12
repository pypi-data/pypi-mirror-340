import os
import json
def read():
    dbUser=os.getenv('DBUSER')
    dbPw=os.getenv('DBPW')
    cwd=os.getcwd()
    print(cwd)
    fp=os.path.join(cwd,'creds.json')
    if os.path.isfile(fp):
        fl=open(fp,'r')
        creds=fl.read()
        fl.close()
        creds=json.loads(creds)
        return creds
    else:
        creds={
            "user":dbUser,
            "password":dbPw,
        }
        return creds