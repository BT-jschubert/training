import xmlrpc.client

#CONFIGURATION PARAMETERS
HOST = 'localhost'
PORT = 8069
DB = 'training_test'
USER = 'admin'
PASS = 'admin'

#CONNECTION TO ODOO INSTANCE
root = 'http://%s:%d/xmlrpc/' % (HOST,PORT)
uid = xmlrpc.client.ServerProxy(root + 'common').login(DB, USER, PASS)
sock = xmlrpc.client.ServerProxy(root + 'object')


#*************************** UTILITY FUNCTIONS ***************************
def _print_sessions(sessions):
    i=0
    for session in sessions:
        print("[", i ,"]")
        i += 1
        print("\tname: \t",session['name'])
        print("\tseats: \t",session['number_of_seats'])
    print("\n\n")

def _get_sessions():
    session_ids = sock.execute(DB, uid, PASS, 'sessions', 'search', [])
    sessions = sock.execute_kw(DB, uid, PASS, 'sessions', 'read', [session_ids])
    return sessions

def _get_sessions_with_fields():
    return sock.execute_kw(DB, uid, PASS, 'sessions', 'search_read', [], {'fields': ['name', 'number_of_seats']})


#*************************** PROGRAM EXECUTION ***************************
print("**************** INITIAL SESSIONS ****************")
_print_sessions(_get_sessions())


print("************* INSERTING NEW SEASSON **************\n...\n...\n")
id = sock.execute_kw(DB, uid, PASS, 'sessions', 'create', [{
    'name': "New Session",
    'number_of_seats': "5"
}])
print("Inserted new Seasson.\n\n")


print("**************** CURRENT SESSIONS ****************")
_print_sessions(_get_sessions_with_fields())


print("*************** DELETE NEW SESSION ***************\n...\n...\n")
session_ids = sock.execute(DB, uid, PASS, 'sessions', 'search', [('name', '=', 'New Session')])
sock.execute_kw(DB, uid, PASS, 'sessions', 'unlink', [session_ids])
print("Deleted new Seasson.\n\n")


print("************ FINAL STATE OF SESSIONS *************")
_print_sessions(_get_sessions_with_fields())

