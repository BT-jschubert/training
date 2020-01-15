from odoo import api, fields, models
from datetime import timedelta


class Session(models.Model):
    _name = 'session'
    _description = 'Sessions'

    name = fields.Text(string='Name')
    start_date = fields.Datetime(string='StartDate', default=fields.Date.today)
    end_date = fields.Datetime(string='EndDate', compute='_compute_end_date')
    duration = fields.Integer(string='Duration in Minutes')
    seats = fields.Integer(string='No of Seats')
    course_id = fields.Many2one(comodel_name='course', ondelete='cascade')
    instructor_id = fields.Many2one(comodel_name='res.partner', ondelete='set null')
    attendees = fields.Many2many(comodel_name='res.partner', relation='session_attendees')

    description = fields.Html(string='Description',related="course_id.description")

    seats_taken = fields.Integer(string="Seats taken", compute='_compute_seats_taken', store=True)
    is_full = fields.Boolean(string="Course is Full", compute='_compute_is_full',store=True)


    @api.depends('start_date')
    def _compute_end_date(self):
        for record in self:
            record.end_date = record.start_date + timedelta(minutes=record.duration)

    @api.depends('attendees')
    def _compute_seats_taken(self):
        for record in self:
            if record.attendees:
                record.seats_taken = len(record.attendees) / record.seats * 100
            else:
                record.seats_taken = 0

    @api.depends('attendees')
    def _compute_is_full(self):
        for record in self:
            record.is_full = len(record.attendees) == record.seats
