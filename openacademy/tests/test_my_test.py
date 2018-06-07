from odoo.tests import common
from odoo import fields
from datetime import datetime,timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT


class My_tests(common.TransactionCase):

    def setUp(self):
        super(My_tests, self).setUp()

        self.env['res.partner'].create({
            'name': 'My Test User',
            'email': 'mytestuser@example.com',
        })

        self.env['sessions'].create({
            'name': 'My Test Session',
            'duration': 5,
            'number_of_seats': 10,
            #start_date by default value is today.
        })


    def test_taken_seats_updated(self):

        #Get initial number of seats from a session
        session = self.env['sessions'].search([('name', '=', 'My Test Session')])
        initial_seats_taken = session.taken_seats_percent

        #Get a partner to add as a new Attendee to the session
        # new_attendee = self.env['res.partner'].search([('id','=',34)])
        new_attendee = self.env['res.partner'].search([('name', '=', 'My Test User')])

        #Add the new attendee to the session
        session.browse(session.id).attendees |= new_attendee

        #Retrieve the value for the number of seats availabe. It should have been changed.
        # actual_seats_taken = session.browse(session.id).taken_seats_percent  <-- if it does NOT detect the changes...
        actual_seats_taken = session.taken_seats_percent

        #Check that the value have changed for the number of seats taken.
        self.assertNotEqual(initial_seats_taken, actual_seats_taken)


    #This test will check if the end_date field changes when the duration is modified. So it is re-calculated.
    def test_duration_is_changed(self):
        session = self.env['sessions'].search([('name', '=', 'My Test Session')])
        initial_end_date = datetime.strptime(session.end_date, DATE_FORMAT)

        #Asign a new value for duration, and check that the computed field "end_date" have changed.
        session.duration = 10
        final_end_date = datetime.strptime(session.end_date, DATE_FORMAT)

        #Asserts.
        self.assertNotEquals(initial_end_date, final_end_date)

        update_days = timedelta(days=session.duration)
        datetime_object = datetime.strptime(session.start_date, DATE_FORMAT)
        calculated_end_date = datetime_object + update_days
        self.assertEquals(final_end_date, calculated_end_date)


    #This test will call a method to link some models from a wizard.
    def test_wizard_attendees(self):
        session = self.env['sessions'].search([('name', '=', 'My Test Session')])
        number_of_attendees = len(session.attendees)

        #TWO WAYS to retrieve the information from a model:
        #   1-. GET A INDIVIDUAL:
        #       new_attendee = self.env['res.partner'].search([('name', '=', 'My Test User')])
        #
        #   2-. GET ALL THE OCCURRENCES, AND LATER ON, RETRIEVE BY INDEX.
        #
        partners = self.env['res.partner'].search([])

        #add references to the wizard model.
        my_new_wizard = self.env['wizard'].create({
            'sessions': [(4, session.id)],
            'attendees': [(4, partners[0].id)]
        })

        #Call the function from the wizard.
        my_new_wizard.add_attendees()

        #Asserts.
        self.assertNotEquals(number_of_attendees,len(session.attendees))
        self.assertIn(session.attendees, partners[0])
