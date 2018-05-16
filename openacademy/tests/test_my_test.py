from odoo.tests import common

class TestMy_test(common.TransactionCase):
    def setUp(self):
        super(TestMy_test, self).setUp()

    def tearDown(self):
        super(TestMy_test, self).tearDown()

    def test_1_seats_updated(self):
        # Get initial percentage of occupied seats
        sessions_table = self.env['session'].search([])  #A 'search' is necessary if we want to get the records
                                                         # (empty if we want ALL of them)
        initial_seats = sessions_table[0].taken_seats_percent
        print('Initial percentage of occupied seats: %f' %(initial_seats))

        # Add a new attendee (partner - Demo User)
        partner_table = self.env['res.partner'].search([('name', 'ilike', 'Demo User')])
        sessions_table[0].attendees |= partner_table[0]

        # Get new percentage of occupied seats
        current_seats = sessions_table[0].taken_seats_percent
        print('Current percentage of occupied seats: %f' % (current_seats))

        self.assertNotEqual(initial_seats, current_seats,
                            'Percentage of taken seats does not change after adding a new attendee.')


    def test_2_end_date_change(self):
        #Get initial duration
        sessions_table = self.env['session'].search([])
        initial_duration = sessions_table[0].duration
        print('Initial duration in days: %f' % (initial_duration))

        #Change end date
        sessions_table[0].write({'end_date': '2018-07-01 00:00:00'})
        current_duration = sessions_table[0].duration
        print('Current duration in days: %f' % (current_duration))

        self.assertNotEqual(initial_duration, current_duration, 'Duration does not change after modifying the end date')


    def test_3_wizard_addAttendees(self):
        # Get initial attendees for two sessions
        sessions = self.env['session'].search([])
        session_1 = sessions[0]
        session_2 = sessions[1]

        initial_attendees_session_1 = len(session_1.attendees)
        initial_attendees_session_2 = len(session_2.attendees)
        print('Attendees session 1: %d' %(initial_attendees_session_1))
        print('Attendees session 2: %d' % (initial_attendees_session_2))

        #Get two partners (new attendees for the sessions - Demo Users)
        partners = self.env['res.partner']
        partner_1 = partners.search([('name', 'ilike', 'Demo User')])[0]
        partner_2 = partners.search([('name', 'ilike', 'Demo Portal User')])[0]

        # Add both attendees to both sessions using wizard
        wizard = self.env['wizard'].create({'attendees': [(4, partner_1.id), (4, partner_2.id)],
                                            'sessions':  [(4, session_1.id), (4, session_2.id)]})
        wizard.add_attendees()

        #Get final attendees for the two sessions
        current_attendees_session_1 = len(session_1.attendees)
        current_attendees_session_2 = len(session_2.attendees)
        print('Attendees session 1: %d' % (current_attendees_session_1))
        print('Attendees session 2: %d' % (current_attendees_session_2))

        self.assertNotEqual(initial_attendees_session_1, current_attendees_session_1,
                            'Wizard does not add attendees to session 1')
        self.assertNotEqual(initial_attendees_session_2, current_attendees_session_2,
                            'Wizard does not add attendees to session 2')