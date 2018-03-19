{
    'name' : 'OpenAcademy',
    'version'  : '0.01',
    'depends' : ['base'],
    'author' :  'Daniel Herreros',
    'category' : 'Category',
    'description' : """
                        Open Academy module for practical training exercises
                    """,
    #data files to be loaded ALWAYS
    'data' : [
        'views/vistas.xml',
        'views/menu.xml',
        'views/session_views.xml',
        'views/partner_ext.xml'
    ],
    #data files to be loaded ONLY while in demo
    'demo' : [
        'demo/mydemodata.xml',
        'demo/session_demo_data.xml',
        'demo/teachers.xml'
    ],
    #should we autoinstall the module
    'autoinstall' : False,

}