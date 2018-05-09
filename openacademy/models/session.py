from odoo import fields, models, api
from datetime import datetime, timedelta

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT

class Session(models.Model):
    _name = 'session'
    _rec_name = 'name'


    name = fields.Char(string='Session name:')
    start_date = fields.Date(string="Start date:", default=fields.Date.today())
    duration = fields.Float(string='Duration in days:')
    end_date = fields.Date(string="End date:", compute = "_get_end_date", inverse="_set_end_date")
    num_seats = fields.Integer(string = 'Number of seats', default=1)
    taken_seats_percent = fields.Float(string="Percentage of taken seats:", compute="_get_percent")

    course_id = fields.Many2one(comodel_name='course', ondelete="set null", string="Related course:", required=True)
    course_description = fields.Text(related='course_id.description', string="Course description:")
    instructor_id = fields.Many2one(comodel_name='res.partner', ondelete="set null", domain=['|', ('instructor', '=', True),('category_id', '=', "Teacher/Level 1")], string="Instructor:")
    responsible_id = fields.Many2one(comodel_name='res.users', ondelete="set null", string="Responsible:")
    attendees = fields.Many2many(comodel_name="res.partner", relation="session_attendees", column1="session_id", column2="attendee_id")


    #Methods for computed fields
    @api.depends('num_seats', 'attendees')
    def _get_percent(self):
        for r in self:
            if not (r.num_seats):
                continue
            num_attendees = len(r.attendees)
            r.taken_seats_percent = num_attendees / r.num_seats * 100

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            s_date = datetime.strptime(r.start_date, DATE_FORMAT)
            e_date = s_date + timedelta(days=int(r.duration))
            r.end_date = e_date.strftime(DATE_FORMAT)


    # Methods for inverse fields
    def _set_end_date(self):
        for r in self:
            if not (r.end_date):
                continue
            s_date = datetime.strptime(r.start_date, DATE_FORMAT)
            e_date = datetime.strptime(r.end_date, DATE_FORMAT)

            res = e_date - s_date
            r.duration = res.days

    # Methods for "onchange"
    @api.onchange('num_seats')
    def _onchange_seats(self):
        if self.num_seats <= 0:
            return {
                'warning': {
                    'title': "Incorrect number of seats",
                    'message': "Number of seats must be a positive number",
                }
            }
        elif self.num_seats < len(self.attendees):
            return {
                'warning': {
                    'title': "Incorrect number of seats",
                    'message': "There are more participants than seats! Number of seats must be higher than number of attendees",
                }
            }

    #Methods for Python constraints
    @api.constrains('instructor_id', 'attendees')
    def _instructor_not_attendee(self):
        for r in self:
            if r.instructor_id in r.attendees:
                raise Exception("An instructor you have chosen is an attendee. Would you like to continue?")
