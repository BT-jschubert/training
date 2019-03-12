import logging

from odoo.tests import common

from datetime import  datetime

_logger = logging.getLogger(__name__)


class TestSessionCase(common.TransactionCase):
    def setUp(self):
        super(TestSessionCase, self).setUp()
    
    def tearDown(self):
        super(TestSessionCase, self).tearDown()

    def test_seats(self):
        session_obj = self.env['openacademy.session'].search([("name", "=", "Session 1")])
        init_seats = session_obj['remain_seats']

        attendee_obj = self.env['res.partner'].search([("name", "=", "Agrolait")])

        session_obj.write({'attendees': [(4, attendee_obj['id'])]})
        self.assertNotEqual(init_seats, session_obj['remain_seats'])

    def test_duration(self):
        session_obj = self.env['openacademy.session'].search([("name", "=", "Session 1")])
        init_duration = session_obj['duration']

        session_obj.write({'end_date': datetime.today()})
        self.assertNotEqual(init_duration, session_obj['duration'])
