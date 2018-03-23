import xmlrpc.client

root = 'http://%s:%d/xmlrpc/' % ('localhost',8069)

uid = xmlrpc.client.ServerProxy(root + 'common').login('training','admin','admin')
print("Logged in as %s (uid: %d)" % ('admin', uid))

sock = xmlrpc.client.ServerProxy(root + 'object')

session = sock.execute('training',uid,'admin','openacademy.session','search_read',[])
for el in session:  
    print("Nombre de la sesión: %s, Curso relacionado: %s, Numero de asientos: %d" % (el['name'], el['related_course'][1], el['number_of_seats']))