import pyTigerGraph as tg
#print(tg.__file__)
#from config import host, un, graph, pw

hostname = "https://frws-victornet.i.tgcloud.io"
username = "tigergraph"
password = "Burro123"
graphname =  "FINNET"
conn = None


def getConnection():
    try:
        conn = tg.TigerGraphConnection(host=hostname,
                                    graphname=graphname,
                                    username=username,
                                    password=password,
                                    version="3.1.0",
                                    useCert = True,
                                    restppPort= 9000,
                                    gsPort=14240
                                    ) #usercert=false
        secret = 'evs11qk7nqg3c7r34rd2fh63685hut58'
        conn.apiToken = conn.getToken(secret)
#        token = None
        return conn            
    except Exception as e:
        print(e)
        print('There was an error. Make sure to start your box and try again')

#conn = getConnection()
#print(conn.gsql('''LS''', options=[]))
