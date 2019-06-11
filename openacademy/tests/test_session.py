from odoo.tests import common

class TestSession(common.TransactionCase):

    def test_number_of_seats_is_updated_properly_when_adding_new_attendees(self):
        session = self.env["openacademy.session"].create({
            "name": "foo",
            "start_date": "01/01/2019",
            "seats": 4,
            "duration": 4,
        })
        attendee1 = self.env['res.partner'].create({
            "name": "attendee1",
        })
        attendee2 = self.env['res.partner'].create({
            "name": "attendee2",
        })
        session.attendees = attendee1 + attendee2

        self.assertEquals(session.taken_seats, 50.0)

    def test_duration_is_computed_properly_when_changing_end_date(self):
        session = self.env["openacademy.session"].create({
            "name": "foo",
            "start_date": "01/01/2019",
            "seats": 4,
            "duration": 4,
        })

        session.end_date = "2019-01-07"

        self.assertEquals(session.duration, 6)

    def test_all_sessions_have_the_attendees_given_from_the_wizard(self):
        wizard = self.env["openacademy.wizard"].create([])
        session1 = self.env["openacademy.session"].create({
            "name": "session1",
        })
        session2 = self.env["openacademy.session"].create({
            "name": "session2",
        })
        attendee1 = self.env['res.partner'].create({
            "name": "attendee1",
        })
        attendee2 = self.env['res.partner'].create({
            "name": "attendee2",
        })

        wizard.attendees = attendee1 + attendee2
        wizard.sessions = session1 + session2
        wizard.save_attendees()

        self.assertEquals(len(session1.attendees), 2)
        self.assertEquals(len(session2.attendees), 2)
        self.assertEquals(session1.attendees[0].name, "attendee1")
        self.assertEquals(session1.attendees[1].name, "attendee2")
        self.assertEquals(session2.attendees[0].name, "attendee1")
        self.assertEquals(session2.attendees[1].name, "attendee2")
