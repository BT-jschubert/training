from datetime import datetime, timedelta

from odoo.tests import common
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT


class TestOpenacademy(common.TransactionCase):

    def setUp(self):
        super(TestOpenacademy, self).setUp()

        partner = self.env['res.partner']
        partner.create({
            'name': 'New Partner 1',
            'email': 'newpartnerm@example.com',
        })

        partner.create({
            'name': 'New Partner 2',
            'email': 'newpartnerm@example.com',
        })

        courses = self.env['course']
        course = courses.create({
            'title': "Driving",
            'description': 'Learn to drive different vehicles'
        })

        session = self.env['session']
        session.create({
            'name': 'Driving a motorbike',
            'start_date': '2018-05-24',
            'duration': 12,
            'number_of_seats': 60,
            'related_course': course.id
        })

    def tearDown(self):
        super(TestOpenacademy, self).tearDown()

    def test_numer_of_seats(self):
        session_model = self.env['session']
        my_session = session_model.search(
            [('name', '=', 'Driving a motorbike')])

        partner_model = self.env['res.partner']
        partner = partner_model.search([('name', '=', 'New Partner 1')])

        attendees_num_before = len(my_session.attendees)

        my_session.write({'attendees': [(4, partner.id)]})
        # first_session.attendees |= partner #V11

        self.assertTrue(partner.id in my_session.attendees.ids,
                        "Added partner not found in first session attendees list")

        attendees_num_after = len(my_session.attendees)

        self.assertEqual(attendees_num_before, attendees_num_after - 1,
                         "Attendees have not incremented correctly")

    def test_duration_update(self):
        session_model = self.env['session']
        my_session = session_model.search(
            [('name', '=', 'Driving a motorbike')])

        duration_before_change = my_session.duration
        end_date_before_change = my_session.end_date

        end_date_object = datetime.strptime(end_date_before_change,
                                            DATE_FORMAT)
        update_days = timedelta(days=2)

        end_date_object = end_date_object + update_days

        end_date_string = end_date_object.strftime(DATE_FORMAT)

        my_session.write({'end_date': end_date_string})

        duration_after_change = my_session.duration

        self.assertNotEqual(duration_before_change, duration_after_change,
                            "Duration has not changed after increasing the end date by 2 days")

    def test_adding_attendes_wizard(self):
        session_model = self.env['session']
        wizard_model = self.env['add_sessions_wizard']
        partner_model = self.env['res.partner']

        my_session = session_model.search(
            [('name', '=', 'Driving a motorbike')])

        partner1 = partner_model.search([('name', '=', 'New Partner 1')])
        partner2 = partner_model.search([('name', '=', 'New Partner 2')])

        # first_session.write({'attendees': [(4, partner.id)]})

        my_wizard = wizard_model.create({
            'wizard_session': my_session.id,
            'wizard_session_attendees': [(4, partner1.id), (4, partner2.id)]
        })

        my_wizard.save_results()

        my_session = session_model.search(
            [('name', '=', 'Driving a motorbike')])

        self.assertIn(partner1, my_session.attendees,
                      'Parter1 not in session')
        self.assertIn(partner2, my_session.attendees,
                      'Parter2 not in session')
