import sys
import time
from datetime import datetime,timedelta
import requests
import psutil
import socket
import multiprocessing as mp
from aiohttp import web
from eddies_tools.db_info import *
from eddies_tools.mysql_query_builder import *
from eddies_tools.read_creds import read
CREDS=read()
HUBDBI=getDbInstance(user=CREDS['localhost']['user'],
                     password=CREDS['localhost']['password'])
def get_idlest():
    t1=HUBDBI.web_ms.routers
    t2=HUBDBI.web_ms.user_router_binding
    t3=HUBDBI.network_traffic.t
    now=datetime.now()
    ym=(now.year,now.month)
    sq=Select(t1.port).str()
    routerCount={}
    crs=HUBDBI.query(sq)
    for (port,) in crs:
        routerCount[port]=0
    sq=Select(t3.port,t3.upload,t3.download)\
        .where(t3.time.ge(now-timedelta(minutes=5))).str(ym)
    crs=HUBDBI.query(sq)
    for port,upload,download in crs:
        routerCount[port]=routerCount.get(port) or 0
        routerCount[port]+=upload+download
    mn=10e10
    mnPort=None
    for port in routerCount:
        if routerCount[port]<mn:
            mn=routerCount[port]
            mnPort=port
    return mnPort
def handle_client(client_socket,addr):
    t1=HUBDBI.web_ms.routers
    t2=HUBDBI.web_ms.user_router_binding
    ip=addr[0]
    now=datetime.now()
    sq=Select(t2.port).where(t2.ip.eq(ip)\
        .And(t2.time.ge(now-timedelta(minutes=60)))).str()
    crs=HUBDBI.query(sq)
    port=None
    for (port,) in crs: pass
    if not port:
        port=get_idlest()
    sq=Insert(t2.ip,t2.port,t2.time).values([
        ip,
        port,
        SQL.now()
    ]).on_duplicate_update(t2.port,t2.time).str()
    HUBDBI.query(sq)
    message = client_socket.recv(1024).decode()
    print(f"[+] Received: {message[:100]}...")
    fullUrl=message.split("HTTP")[0]
    if 'GET' in fullUrl:
        fullUrl=fullUrl.split('GET')[1].strip()
    elif 'POST' in fullUrl:
        fullUrl=fullUrl.split('POST')[1].strip()
    url=f'http://127.0.0.1:{port}{fullUrl}'
    print(url)
    client_socket.sendall(f"HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n"
       f"<script>window.location='{url}'</script>\r\n\r\n".encode())
    client_socket.close()
if __name__=='__main__':
    print(f'[+]',CREDS)
    if len(sys.argv)>1:
        bind_port=int(sys.argv[1])
    else:
        bind_port=5000
    bind_ip="0.0.0.0"
    print(f"[+] Listening on port {bind_ip} : {bind_port}")
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
        client_handler = mp.Process(target=handle_client,args=(client,addr))
        client_handler.start()
