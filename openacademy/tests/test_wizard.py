from odoo.tests import common
# from unittest2 import SkipIf

class TestWizard(common.TransactionCase):

    def setUp(self):
        super(TestWizard, self).setUp()
        # check sessions initial attendees
        self.initial_session_1 = self.env['openacademy.session'].search([('name', '=', 'Session_test1')])
        self.initial_session_2 = self.env['openacademy.session'].search([('name', '=', 'Session_test2')])
        # add attendess through wizard
        self.agrolait_id = self.env['res.partner'].search([('name', '=', 'Agrolait')])['id']
        self.wizard_obj = self.env['openacademy.wizard']

        self.wizard = self.wizard_obj.create({'partner_relation': [(4, self.agrolait_id)],
                            'session_relations': [(4, self.initial_session_1.id),
                                                  (4, self.initial_session_2.id)]})
        pass

    def tearDown(self):
        super(TestWizard, self).tearDown()

    def test_attendees_adding(self):
        self.wizard.add2sessions()
        #check sessions final attendess
        attendee_list_ses1 = self.initial_session_1.attendees_ids
        attendee_list_ses2 = self.initial_session_2.attendees_ids
        self.assertEqual(attendee_list_ses1.id, self.agrolait_id, 'Not in session 1')
        self.assertEqual(self.agrolait_id, attendee_list_ses1.id, 'Not in session 2')

