import xmlrpc.client

HOST = 'localhost'
PORT = 8069
DB = 'Training'
USER = 'admin'
PASS = 'admin'
ROOT = 'http://%s:%d/xmlrpc/' % (HOST, PORT)

#Log in the database
uid = xmlrpc.client.ServerProxy(ROOT + 'common').login(DB, USER, PASS)
print("Logged in as %s (uid:%d)" % (USER, uid))


# Read Demo User db id
# sock = xmlrpc.client.ServerProxy(ROOT + 'object')
# args = [('name', '=', 'Demo User')]
# demo_user_id = sock.execute(DB, uid, PASS, 'res.partner', 'search', args)
# print("Demo user ID: %d" %(demo_user_id[0]))


#Look for all sessions and display the number of seats
sock = xmlrpc.client.ServerProxy(ROOT + 'object')
args = ['name', 'num_seats']
# session_ids = sock.execute(DB, uid, PASS, 'session', 'search', [])
sessions = sock.execute(DB, uid, PASS, 'session', 'search_read', [], args)

for s in sessions:
    print('Session: %s -> %d seats' %(s['name'], s['num_seats']))


#Create new session for the first course in the list
course_id =  sock.execute(DB, uid, PASS, 'course', 'search', [])[0]
sock.execute(DB, uid, PASS, 'session', 'create', {'name': 'New session xmlrpc', 'course_id': course_id})
