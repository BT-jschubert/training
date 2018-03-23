import xmlrpc.client

# Indicate your HOST, PORT, DB, USER, PASS
HOST = 'localhost'
PORT = 8069
DB = 'training_curso'
USER = 'admin'
PASS = 'admin'

root = 'http://%s:%d/xmlrpc/' % (HOST, PORT)
uid = xmlrpc.client.ServerProxy(root + 'common').login(DB, USER, PASS)
print("Logged in as %s (uid: %d)" % (USER, uid))

#
sock = xmlrpc.client.ServerProxy(root + 'object')
# args = []
# sessions = sock.execute(DB, uid, PASS, 'openacademy.session', 'search', args)
# args = sessions
# sessions_name = sock.execute(DB, uid, PASS, 'openacademy.session', 'read', args)
sessions = sock.execute(DB, uid, PASS, 'openacademy.session', 'search_read', [])
for session in sessions:
    print('Name: %s - Number of seats: %s \n' % (session['display_name'], session['number_of_seats']))

