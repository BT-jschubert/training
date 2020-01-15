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
    course_id = fields.Many2one('course', ondelete='cascade')
    instructor_id = fields.Many2one('res.partner', ondelete='set null')
    attendees = fields.Many2many('res.partner', 'session_attendees')

    description = fields.Html(string='Description', related="course_id.description")

    seats_taken = fields.Integer(string="Seats taken", compute='_compute_seats_taken')
    is_full = fields.Boolean(string="Course is Full", compute='_compute_is_full', store=True)

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

    @api.onchange("seats")
    def _check_seats(self):  # self is not a collection
        if self.seats < 0:
            return {
                'warning': {
                    'title': "Negative Seats",
                    'message': "You can't have negativ Seats",
                }
            }

    @api.onchange('attendees', 'seats')
    def _check_available_seats(self):  # self is not a collection
        if self.seats_taken > 100:
            return {
                'warning': {
                    'title': "Session Full",
                    'message': "The Session is full",
                }
            }

    @api.constrains('instructor_id', 'attendees')
    def _check_instructor_is_not_an_attendee(self):
        for record in self:
            for attendee in record.attendees:
                if attendee.id == record.instructor_id.id:
                    return {
                        'warning': {
                            'title': "Instructor",
                            'message': "The Instructor cannot be an Attendee",
                        }
                    }
