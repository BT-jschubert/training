import json
import random
import urllib.request


def json_rpc(url, method, params):
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": random.randint(0, 1000000000),
    }
    req = urllib.request.Request(url=url, data=json.dumps(data).encode(), headers={
        "Content-type":"application/json",
    })
    r = urllib.request.urlopen(req).read()
    reply = json.loads(r.decode('utf-8'))
    if reply.get('error'):
        raise Exception(reply["error"])
    return reply["result"]


def call(url, service, method, *args):
    return json_rpc(url, "call", {"service": service, "method": method, "args": args})

#log in

# Indicate your HOST, PORT, DB, USER, PASS


HOST = 'localhost'
PORT = 8069
DB = 'training_curso'
USER = 'admin'
PASS = 'admin'

url = "http://%s:%s/jsonrpc" % (HOST, PORT)
uid = call(url, "common", "login", DB, USER, PASS)
print("Logged in as %s (uid: %d)" % (USER, uid))

args = []
sessions = call(url, "object", "execute", DB, uid, PASS, 'openacademy.session',
                'search_read', args)
for session in sessions:
    print('Name: %s - Number of seats: %s \n' % (session['display_name'], session['number_of_seats']))