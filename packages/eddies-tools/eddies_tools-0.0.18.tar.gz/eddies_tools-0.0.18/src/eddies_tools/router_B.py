import sys
import time
from datetime import datetime
import requests
import psutil
import socket
HOSTNAME=socket.gethostname()
HOST=socket.gethostbyname(HOSTNAME)
import os
PID=os.getpid()
PPID=os.getppid()
print(HOSTNAME,HOST,PPID,PID)
from eddies_tools.db_info import *
from eddies_tools.mysql_query_builder import *
from eddies_tools.read_creds import read
CREDS=read()
HUBDBI=getDbInstance(user=CREDS['localhost']['user'],
                     password=CREDS['localhost']['password'])
# if len(sys.argv)<2:
#     raise Exception('enter port')
# bind_port=int(sys.argv[1])
import socket
import threading
import traceback
import multiprocessing as mp
def get_user_info(USER_INFO):
    t1=HUBDBI.hub.users
    t2=HUBDBI.hub.user_perms
    sq1=Select(t1.uid,t1.name,t1.ip,t1.expiry).str()
    sq2=Select(t2.uid,t2.perm).str()
    while True:
        user_perms={}
        try:
            crs=HUBDBI.query(sq2,cursor='dict')
        except Exception:
            traceback.print_exc()
            time.sleep(2)
            continue
        for d in crs:
            uid=d['uid']
            user_perms[uid]=user_perms.get(uid) or set()
            user_perms[uid].add(d['perm'])
        try:
            crs=HUBDBI.query(sq1,cursor='dict')
        except Exception:
            traceback.print_exc()
            time.sleep(2)
            continue
        for d in crs:
            d['perms']=user_perms.get(d['uid']) or set()
            USER_INFO[d['ip']]=d
            USER_INFO[d['uid']]=d
        time.sleep(2)
def get_routing_info(ROUTING_INFO,ROUTING_COUNTS,USER_ROUTING_INFO):
    t1=HUBDBI.web_ms.ms
    t2=HUBDBI.web_ms.routing
    t3=HUBDBI.web_ms.user_routing
    sq2=Select(t2.ms,t2.host,t2.port,t1.requiredPerm).str()
    sq3=Select(t3.uid,t3.ms,t3.host,t3.port,t3.time)\
        .where(t3.time.ge(datetime.now()-timedelta(minutes=60))).str()
    while True:
        try:
            crs=HUBDBI.query(sq2,cursor='dict')
        except Exception:
            traceback.print_exc()
            time.sleep(2)
            continue
        routing={}
        for d in crs:
            url=d['ms']
            routing[url]=routing.get(url) or {'requiredPerm':d['requiredPerm'],'addresses':[]}
            hp=(d['host'],d['port'])
            routing[url]['addresses'].append(hp)
            ROUTING_COUNTS[hp]=0
        for url in routing:
            ROUTING_INFO[url]=routing[url]
        try:
            crs=HUBDBI.query(sq3,cursor='dict')
        except Exception:
            traceback.print_exc()
            time.sleep(2)
            continue
        for d in crs:
            hp=(d['host'],d['port'])
            ROUTING_COUNTS[hp]+=1
            USER_ROUTING_INFO[(d['uid'],d['ms'])]=d
        time.sleep(2)
def get_idlest(ROUTING_INFO,ROUTING_COUNTS,url):
    mn=10e10
    mnHp=None
    for hp in ROUTING_INFO[url]['addresses']:
        if hp=='meta':continue
        if ROUTING_COUNTS[hp]<mn:
            mn=ROUTING_COUNTS[hp]
            mnHp=hp
    return {'host':mnHp[0],'port':mnHp[1]}
def logger(qu):
    t1=HUBDBI.usage_log.t
    t2=HUBDBI.web_ms.user_routing
    while True:
        kwa=qu.get()
        now=datetime.now()
        ym=(now.year,now.month)
        if kwa['type']=='usage_log':
            sq=Insert(t1.uid,t1.url,t1.fullUrl,t1.time,t1.
                      responseSize,t1.responseTime,
                      t1.error,t1.body).values([
                kwa['uid'],
                kwa['url'],
                kwa['fullUrl'],
                SQL.now(),
                kwa['responseSize'],
                kwa['responseTime'],
                kwa['error'],
                kwa['body']
            ]).str(ym)
        elif kwa['type']=='user_routing':
            sq=Insert(t2.uid,t2.ms,t2.host,t2.port,t2.time).values([
                kwa['uid'],
                kwa['url'],
                kwa['host'],
                kwa['port'],
                SQL.now(),
            ]).on_duplicate_update(t2.host,t2.port,t2.time).str()
        else:
            print(f"unknown logger type {kwa['type']}")
            continue
        try:
            HUBDBI.query(sq)
        except Exception as e:
            print(e)
def get_network_usage(PORT):
    UPDATE_DELAY=2
    io=psutil.net_io_counters()
    bytes_sent,bytes_recv=io.bytes_sent,io.bytes_recv
    t1=HUBDBI.network_traffic.t
    while True:
        now=datetime.now()
        ym=(now.year,now.month)
        time.sleep(UPDATE_DELAY)
        io_2=psutil.net_io_counters()
        sent=io_2.bytes_sent-bytes_sent
        recv=io_2.bytes_recv-bytes_recv
        print(f"Upload: {sent}, Download: {recv}")
        bytes_sent,bytes_recv=io_2.bytes_sent,io_2.bytes_recv
        sq=Insert(t1.hostname,t1.host,t1.port,t1.time,t1.pid,t1.upload,t1.download).values([
            HOSTNAME,
            HOST,
            PORT,
            SQL.now(),
            PPID,
            sent,
            recv
        ]).str(ym)
        HUBDBI.query(sq)
def handle_client(client_socket,addr,USER_INFO,ROUTING_INFO,ROUTING_COUNTS,
                  USER_ROUTING_INFO,LOGGING_QU):
    timer=time.time()
    message = client_socket.recv(1024).decode()
    body=None
    if 'POST' in message:
        body=[]
        while True:
            chunk=client_socket.recv(1024).decode()
            body.apppend(chunk)
            if chunk[-4:]=='\r\n\r\n':
                break
        body=''.join(body)
    print(f"[+] Received: {message[:100]}...")
    fullUrl=message.split("HTTP")[0]
    respCode=None
    resp=None
    get=False
    post=False
    if 'GET' in fullUrl:
        get=True
        fullUrl=fullUrl.split('GET')[1].strip()
    elif 'POST' in fullUrl:
        post=True
        fullUrl=fullUrl.split('POST')[1].strip()
    else:
        respCode=400
        resp='unregistered HTTP method'
    print(fullUrl)
    url='/'.join(fullUrl.split('/')[:2])
    user_info=USER_INFO.get(addr[0])
    print(addr[0])
    uid=user_info['uid']
    print(uid,datetime.now(),user_info['expiry'])
    if respCode is None:
        if fullUrl=='/favicon.ico':
            respCode=400
            resp='no favicon'
        elif user_info is None:
            respCode=401
            resp='no users found'
        elif datetime.now()>user_info['expiry']:
            respCode=401
            resp='user authorization expired'
        elif url not in ROUTING_INFO:
            respCode=400
            resp=f'no routing info for {fullUrl}'
        elif ROUTING_INFO[url]['requiredPerm'] \
            and ROUTING_INFO[url]['requiredPerm'] not in user_info['perms']:
            respCode=401
            resp='user does not have required permissions'
        else:
            ri=USER_ROUTING_INFO.get((uid,url))
            if not ri: ri=get_idlest(ROUTING_INFO,ROUTING_COUNTS,url)
            USER_ROUTING_INFO[(uid,url)]=ri
            LOGGING_QU.put({
                'type':'user_routing',
                'uid':uid,
                'url':url,
                'host':ri['host'],
                'port':ri['port'],
            })
            rl=f"http://{ri['host']}:{ri['port']}{fullUrl}"
            print(rl,'HERE')
            if get:
                resp=requests.get(rl).text
            elif post:
                resp=requests.post(rl,data=body).text
            respCode=200
    #sending back the packet
    resp=(f"HTTP/1.1 {respCode} OK\r\nContent-type: text/html\r\n\r\n"
       f"{resp}\r\n\r\n")
    client_socket.sendall(resp.encode())
    client_socket.close()
    timeTaken=time.time()-timer
    print('time taken',round(timeTaken,4),'s')
    LOGGING_QU.put({
        'type':'usage_log',
        'uid':uid,
        'url':url,
        'fullUrl':fullUrl,
        'responseSize':len(resp),
        'responseTime':timeTaken,
        'error':resp if respCode!=200 else None,
        'body':message,
    })
if __name__=='__main__':
    print(f'[+]',CREDS)
    if len(sys.argv)>1:
        bind_port=int(sys.argv[1])
    else:
        bind_port=5001
    bind_ip="0.0.0.0"
    print(f"[+] Listening on port {bind_ip} : {bind_port}")
    manager=mp.Manager()
    USER_INFO=manager.dict()
    ROUTING_INFO=manager.dict()
    ROUTING_COUNTS=manager.dict()
    USER_ROUTING_INFO=manager.dict()
    LOGGING_QU=mp.Queue()
    # user_info_thread=threading.Thread(target=get_user_info)
    user_info_thread=mp.Process(target=get_user_info,args=(USER_INFO,))
    user_info_thread.start()
    logger_thread=mp.Process(target=logger,args=(LOGGING_QU,))
    logger_thread.start()
    network_usage_thread=mp.Process(target=get_network_usage,args=(bind_port,))
    network_usage_thread.start()
    routing_info_thread=mp.Process(target=get_routing_info,
                                   args=(ROUTING_INFO,ROUTING_COUNTS,USER_ROUTING_INFO))
    routing_info_thread.start()
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((bind_ip,bind_port))
    # we tell the server to start listening with
    # a maximum backlog of connections set to 5
    server.listen(1000)
    while True:
        # When a client connects we receive the
        # client socket into the client variable, and
        # the remote connection details into the addr variable
        client, addr = server.accept()
        print(f"[+] Accepted connection from: {addr[0]}:{addr[1]}")
        #spin up our client thread to handle the incoming data
        # client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler = mp.Process(target=handle_client,
            args=(client,addr,USER_INFO,ROUTING_INFO,ROUTING_COUNTS,
                  USER_ROUTING_INFO,LOGGING_QU))
        client_handler.start()
