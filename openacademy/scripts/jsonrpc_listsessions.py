import json
import random
import urllib.request

def json_rpc(url, method, params):
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": random.randint(0,1000000000),
    }
    req = urllib.request.Request(url=url, data=json.dumps(data).encode(),
                                 headers={ "Content-Type":"application/json" })

    r = urllib.request.urlopen(req).read()
    reply = json.loads(r.decode('utf-8'))
    if reply.get("error"):
        raise Exception(reply["error"])
    return reply["result"]

def call(url, service, method, *args):
    return json_rpc(url, "call", {"service": service, "method": method, "args":args})

url = "http://%s:%d/jsonrpc" % ("localhost",8069)
uid = call(url, "common", "login", "training", "admin", "admin")
print("Logged in as %s (uid: %d)" % ("admin",uid))

args=[]
sessions = call(url, "object", "execute", "training", uid, "admin", 'openacademy.session', 'search_read', args)
for el in sessions:
    print("Nombre de la sesión: %s, Curso relacionado: %s, Numero de asientos: %d" % (
    el['name'], el['related_course'][1], el['number_of_seats']))