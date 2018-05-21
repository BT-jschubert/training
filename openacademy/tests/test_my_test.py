from odoo.tests import common

class TestMy_test(common.TransactionCase):
    def setUp(self):
        super(TestMy_test, self).setUp()

        #Get environments used by tests
        self.session = self.env['session']
        self.course = self.env['course']


        #Create 2 new courses for the tests
        self.test_course_1 = self.course.create({'title': 'Test Course 1'})
        self.test_course_2 = self.course.create({'title': 'Test Course 2'})


        #Create 2 new sessions for the tests and add the two new courses
        self.test_session_1 = self.session.create({'name': 'Test Session 1',
                                         'course_id': self.test_course_1.id,
                                         'num_seats': 2})
        self.test_session_2 = self.session.create({'name': 'Test Session 2',
                                         'course_id': self.test_course_2.id,
                                         'num_seats': 2})



    def tearDown(self):
        super(TestMy_test, self).tearDown()


    def test_1_seats_updated(self):
        # A 'search' is necessary if we want to get the records
        # (empty if we want ALL of them)
        # sessions = session_env.search([])
        # print(len(sessions))

        # Get initial percentage of occupied seats -> It should be 0
        initial_seats = self.test_session_1.taken_seats_percent
        print('Initial percentage of occupied seats: %f' %(initial_seats))

        #Old method to find a user to add to session
        #Changed since since it's more recommendable to search by xml_id
        #partner_table = self.env['res.partner'].search([('name', 'ilike', 'Demo User')])

        # Add an attendee to session 1 (Demo data from res_partner - Search by xml ID)
        partner = self.env.ref("base.res_partner_1")
        self.test_session_1.attendees |= partner

        # Get percentage of occupied seats
        current_seats = self.test_session_1.taken_seats_percent
        print('Current percentage of occupied seats: %f' % (current_seats))


        #Check if current percentage is 50%, since we defined 2 seats for this course
        #and now one should be occupied.
        self.assertEqual(current_seats - initial_seats, 50.0,
                            'Percentage of taken is not well updated after adding a new attendee.')


    def test_2_end_date_change(self):
        # Set end date of the test session
        self.test_session_1.write({'end_date': '2018-07-01'})

        #Get initial duration
        initial_duration = self.test_session_1.duration
        print('Initial duration in days: %f' % (initial_duration))

        #Change end date of the test session
        self.test_session_1.write({'end_date': '2018-07-08'})
        current_duration = self.test_session_1.duration
        print('Current duration in days: %f' % (current_duration))

        self.assertEqual(current_duration-initial_duration, 7.0,
                            'Duration does not change properly after modifying the end date')


    def test_3_wizard_addAttendees(self):
        # Get initial attendees for the two test sessions -> Should be 0
        initial_attendees_session_1 = self.test_session_1.num_attendees
        initial_attendees_session_2 = self.test_session_2.num_attendees
        print('Initial attendees session 1: %d' %(initial_attendees_session_1))
        print('Initial attendees session 2: %d' % (initial_attendees_session_2))

        #Get two partners (Demo data from res_partner - Search by xml ID)
        attendee_1 = self.env.ref("base.res_partner_1")
        attendee_2 = self.env.ref("base.res_partner_2")

        print('Attendee 1 to add: %s' % (attendee_1.name))
        print('Attendee 2 to add: %s' % (attendee_2.name))


        # Add both attendees to both sessions using wizard
        wizard = self.env['wizard'].create({'attendees': [(6, 0, [attendee_1.id, attendee_2.id])],
                                            'sessions':  [(6, 0, [self.test_session_1.id, self.test_session_2.id])]
                                           })

        #Another equivalent possibility to add the attendees to sessions
        # wizard = self.env['wizard'].create({'attendees': [(4, partner_1.id), (4, partner_2.id)],
        #                                     'sessions':  [(4, self.test_session_1.id), (4, self.test_session_2.id)]})

        #Call the wizard action
        wizard.add_attendees()

        #Get final attendees for the two sessions
        current_attendees_session_1 = self.test_session_1.num_attendees
        current_attendees_session_2 = self.test_session_2.num_attendees

        print('Current attendees session 1:')
        for att in self.test_session_1.attendees:
            print(att.name)

        print('Current attendees session 2:')
        for att in self.test_session_2.attendees:
            print(att.name)

        self.assertIn(attendee_1, self.test_session_1.attendees,
                      'Wizard has not added the first attendee to session 1 properly')
        self.assertIn(attendee_2, self.test_session_1.attendees,
                      'Wizard has not added the second attendee to session 1 properly')
        self.assertIn(attendee_1, self.test_session_2.attendees,
                      'Wizard has not added the first attendee to session 2 properly')
        self.assertIn(attendee_2, self.test_session_2.attendees,
                      'Wizard has not added the second attendee to session 2 properly')

        self.assertEqual(current_attendees_session_1-initial_attendees_session_1, 2,
                            'Wizard has not added all attendees to session 1')
        self.assertEqual(current_attendees_session_2-initial_attendees_session_2, 2,
                            'Wizard has not added all attendees to session 2')