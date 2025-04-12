import os
import json
def read():
    dbUser=os.getenv('DBUSER')
    dbPw=os.getenv('DBPW')
    creds={
        'localhost':{
            "user":dbUser,
            "password":dbPw,
        }
    }
    return creds