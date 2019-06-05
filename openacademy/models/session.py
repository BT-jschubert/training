from odoo import models, fields, api
import datetime


class Session(models.Model):
    _name = 'openacademy.session'
    name = fields.Char()
    start_date = fields.Date(default=fields.Date.today)
    end_date = fields.Date(store=True, compute='_compute_end_date', inverse='_inverse_end_date')
    duration = fields.Integer(help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    course = fields.Many2one("openacademy.course", requred=True)
    instructor = fields.Many2one("res.partner")
    attendees = fields.Many2many("res.partner", relation="session_attendee_rel", column1="partner", column2="attendee")
    taken_seats = fields.Float(compute='_compute_taken_seats')

    @api.depends('seats')
    def _compute_taken_seats(self):
        for r in self:
            r.taken_seats = (len(r.attendees)/r.seats)*100 if r.seats > 0 else 0

    @api.depends('duration', 'start_date')
    def _compute_end_date(self):
        for r in self:
            r.end_date = fields.Date.from_string(r.start_date) + datetime.timedelta(days=r.duration)

    def _inverse_end_date(self):
        for r in self:
            if not (r.duration and r.start_date):
                continue
            r.duration = (fields.Date.from_string(r.end_date) - fields.Date.from_string(r.start_date)).days