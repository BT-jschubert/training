import xmlrpc.client
import random

HOST = 'localhost'
PORT = 8069
DB = 'training'
USER = 'admin'
PASS = 'admin'

root = 'http://%s:%d/xmlrpc/' % (HOST, PORT)
uid = xmlrpc.client.ServerProxy(root + 'common').login(DB, USER, PASS)
print("Logged in as %s (uid: %d)" % (USER, uid))

sock = xmlrpc.client.ServerProxy(root + 'object')

# This program should display all the Sessions, and their corresponding number of seats.
args = []
sessions = sock.execute(DB, uid, PASS, 'openacademy.session', 'search_read', args)
for s in sessions:
    print(s['seats'])

# This program should also create a new session for one of the courses.
args = [('title', '=', 'foo')]
session_name = 'foo_session' + str(random.randint(1,10000))
print(session_name)
course_id = sock.execute(DB, uid, PASS, 'openacademy.course', 'search', args)[0]
args = {
    'name': session_name,
    'course': course_id,
    'start_date': '2019-01-01',
    'duration': random.randint(1,10),
    'seats': random.randint(1,20),
}
session = sock.execute(DB, uid, PASS, 'openacademy.session', 'create', args)
print(session)