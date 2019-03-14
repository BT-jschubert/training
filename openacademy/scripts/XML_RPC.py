import xmlrpc.client


class XML_RPC:

    if __name__ == '__main__':
        # Indicate your HOST, PORT, DB, USER, PASS
        PORT = 8069
        DB = 'training'
        USER = 'admin'
        PASS = '123456'

        root = 'http://%s:%d/xmlrpc/' % ('localhost', PORT)
        uid = xmlrpc.client.ServerProxy(root + 'common').login(DB, USER, PASS)

        # Read Demo User db id
        sock = xmlrpc.client.ServerProxy(root + 'object')

        sessions_ids = sock.execute(DB, uid, PASS, 'openacademy.session', 'search', [])
        sessions = sock.execute(DB, uid, PASS, 'openacademy.session', 'read', sessions_ids)

        for session in sessions:
            print(session['name'] +" | Seats: "+str(session['seats']))

        course_ids = sock.execute(DB, uid, PASS, 'openacademy.course', 'search', [])
