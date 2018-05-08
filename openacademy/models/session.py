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
    num_seats = fields.Integer(string = 'Number of seats')
    taken_seats_percent = fields.Float(string="Percentage of taken seats:", compute="_get_percent")

    course_id = fields.Many2one(comodel_name='course', ondelete="set null", string="Related course:", required="True")
    instructor_id = fields.Many2one(comodel_name='res.partner', ondelete="set null", string="Instructor:")
    responsible_id = fields.Many2one(comodel_name='res.users', ondelete="set null", string="Responsible:")
    attendees = fields.Many2many(comodel_name="res.partner", relation="session_attendees", column1="session_id", column2="attendee_id")

    @api.depends('num_seats', 'attendees', 'start_date', 'duration', 'end_date')
    def _get_percent(self):
        for r in self:
            if not (r.num_seats):
                continue
            num_attendees = len(r.attendees)
            r.taken_seats_percent = num_attendees / r.num_seats * 100

    def _get_end_date(self):
        for r in self:
            s_date = datetime.strptime(r.start_date, DATE_FORMAT)
            e_date = s_date + timedelta(days=int(r.duration))
            r.end_date = e_date.strftime(DATE_FORMAT)

    def _set_end_date(self):
        for r in self:
            if not (r.end_date):
                continue
            s_date = datetime.strptime(r.start_date, DATE_FORMAT)
            e_date = datetime.strptime(r.end_date, DATE_FORMAT)

            res = e_date - s_date
            r.duration = res.days
