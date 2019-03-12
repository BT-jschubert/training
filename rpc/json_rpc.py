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
    req = urllib.request.Request(url=url, data=json.dumps(data).encode(),
                                 headers={
                                     "Content-Type": "application/json",
                                 })
    r = urllib.request.urlopen(req).read()
    reply = json.loads(r.decode('utf-8'))
    if reply.get("error"):
        raise Exception(reply["error"])
    return reply["result"]


def call(url, service, method, *args):
    return json_rpc(url, "call",
                    {"service": service, "method": method, "args": args})


# log in the given database
url = "http://%s:%s/jsonrpc" % ('localhost', 8069)
uid = call(url, "common", "login", 'training', 'admin', 'admin')
print("Logged in as %s (uid: %d)" % ('admin', uid))

# Search for Demo User
args = [('name', '=', 'Demo User')]
demo_user_id = call(url, "object", "execute", 'training', uid, 'admin',
                    'res.partner',
                    'search', args)
print(demo_user_id)

sessions = call(url, "object", "execute", 'training', uid, 'admin', 'session',
                'search_read', [], ['name', 'number_of_seats'])

for session in sessions:
    print('\t- Session: ' + session['name'] + ' - Number of seats: ' + str(
        session['number_of_seats']))

print("\nCreating new record")

course_ids = call(url, "object", "execute", 'training', uid, 'admin', 'course',
                  'search', [])
first_course = course_ids[0]

session_name = "JSON Flying with your brain"

id = call(url, "object", "execute", 'training', uid, 'admin', 'session',
          'create', {
              'name': 'JSON Flying with your brain',
              'related_course': first_course}
          )

print("Added course " + session_name + " with id " + str(id))
print("Added course {} with id {}".format(session_name, id))
