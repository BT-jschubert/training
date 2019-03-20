from datetime import timedelta, datetime

from odoo.tests import common


class TestSession(common.TransactionCase):

    def setUp(self):

        """*****setUp*****"""
        super(TestSession, self).setUp()

        self.demo_session_fr1 = self.env.ref('openacademy.demo_session_fr1')
        self.demo_session_fr2 = self.env.ref('openacademy.demo_session_fr2')

        self.attendee1 = self.env['res.partner'].create({'name': 'Name1'})
        self.attendee2 = self.env['res.partner'].create({'name': 'Name2'})

    def test_taken_seat(self):
        self.demo_session_fr1.attend_ids = [(5, 0, 0)]
        self.demo_session_fr1.seats = 4
        self.assertEqual(self.demo_session_fr1.taken_seat_per,0)

        self.demo_session_fr1.attend_ids |= self.attendee1
        self.assertEqual(self.demo_session_fr1.taken_seat_per, 25)

        self.demo_session_fr1.attend_ids |= self.attendee2
        self.assertEqual(self.demo_session_fr1.taken_seat_per, 50)

    def test_end_date_computation(self):
        self.demo_session_fr1.duration = 2
        self.demo_session_fr1.start_date = datetime.now().date()
        self.assertEqual(self.demo_session_fr1.duration, 2)

        self.demo_session_fr1.end_date = (datetime.strptime(self.demo_session_fr1.start_date, '%Y-%m-%d') + timedelta(days=3)).date()
        self.assertEqual(self.demo_session_fr1.duration, 4)

    def test_wizard(self):

        self.demo_session_fr1.attend_ids = [(5, 0, 0)]
        self.demo_session_fr2.attend_ids = [(5, 0, 0)]

        self.wizard = self.env['openacademy.wizard'].create({})
        self.wizard.session_ids |= self.demo_session_fr1
        self.wizard.session_ids |= self.demo_session_fr2

        self.wizard.partner_ids |= self.attendee1
        self.wizard.partner_ids |= self.attendee2

        self.assertNotIn(self.attendee1, self.demo_session_fr1.attend_ids)
        self.assertNotIn(self.attendee2, self.demo_session_fr1.attend_ids)
        self.assertNotIn(self.attendee1, self.demo_session_fr2.attend_ids)
        self.assertNotIn(self.attendee2, self.demo_session_fr2.attend_ids)

        self.wizard.save_attendees()

        self.assertIn(self.attendee1, self.demo_session_fr1.attend_ids)
        self.assertIn(self.attendee2, self.demo_session_fr1.attend_ids)
        self.assertIn(self.attendee1, self.demo_session_fr2.attend_ids)
        self.assertIn(self.attendee2, self.demo_session_fr2.attend_ids)
