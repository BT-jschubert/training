{
    'name': "openacademy",
    'version': '1.0',
    'depends': ['base'],
    'author': "Nadal",
    'category': 'Category',
    'description': """
    Module for human resource management. You can manage:\n
    * Employees and hierarchies : You can define your employee with User and display hierarchies\n
    * HR Departments\n
    * HR Jobs\n
    \n
    Required git:\n
    - git@github.com:brain-tec/BT-Developer.git#10.0
    - git@github.com:brain-tec/BT-Webkit.git#10.0
    - git@github.com:brain-tec/l10n-switzerland.git#10.0
    - git@github.com:brain-tec/partner-contact.git#10.0
    - git@github.com:brain-tec/BT-Utils.git#10.0
    - git@github.com:brain-tec/bank-payment.git
    Required patches are in BT-Swissdec/patches/ folder.\n
      \n
    If you have any problems with "no module named pip.commands" execute following commands:\n
    - sudo apt-get install python-setuptools \n
    - sudo easy_install pip \n
    - sudo easy_install logilab-common \n
    \n
    For the new 'viewgen-java-2017.05' you need to install this package: \n
    - sudo apt install pdftk \n
    \n
    In order to run the viewgen after version 'viewgen-java-2017.05' we need to have java8 installed. Therefore we have a new ir.config.parameter 'swissdec_java_key_path_viewgen' which has to be set \n
    """,
    # data files always loaded at installation
    'data': [
        "data/to_done_cronjob.xml",
        "views/courses_menu.xml",
        "views/course_views.xml",
        "views/sessions_menu.xml",
        "views/session_views.xml",
        "views/partner_menu.xml",
        "views/partner_views.xml",
        "views/wizard_view.xml",
        "security/security.xml",
        "security/ir.model.access.csv",
        "reports/session_reports.xml"
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        "demo/courses_demo_data.xml",
        "demo/sessions_demo_data.xml"
    ],
    'auto_install': False
    # If module and all its dependencies have to be installed automatically
}
