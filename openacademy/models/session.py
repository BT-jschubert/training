from odoo import models
from odoo import fields
from odoo import api
from odoo import exceptions
import datetime


class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(string="Name")
    start_date = fields.Date(default=fields.Date.today, string="Start date")
    end_date = fields.Date(store=True, compute='_compute_end_date', inverse='_inverse_end_date', string="End date")
    duration = fields.Integer(help="Duration in days", string="Duration")
    seats = fields.Integer(string="Number of seats")
    course = fields.Many2one("openacademy.course", requred=True, string="Course")
    instructor = fields.Many2one("res.partner", domain=lambda self: self._instructor_domain(), string="Instructor")
    attendees = fields.Many2many("res.partner", relation="session_attendee_rel", column1="session", column2="partner", string="Attendees")
    taken_seats = fields.Float(compute='_compute_taken_seats', string="Taken seats")
    color = fields.Integer(string="Color");

    @api.depends('seats')
    def _compute_taken_seats(self):
        for r in self:
            r.taken_seats = (len(r.attendees)/r.seats)*100.0 if r.seats > 0 else 0.0

    @api.depends('duration', 'start_date')
    def _compute_end_date(self):
        for r in self:
            r.end_date = fields.Date.from_string(r.start_date) + datetime.timedelta(days=r.duration)

    def _inverse_end_date(self):
        for r in self:
            if not (r.end_date and r.start_date):
                continue
            r.duration = (fields.Date.from_string(r.end_date) - fields.Date.from_string(r.start_date)).days

    def _instructor_domain(self):
        return ['|', ('is_instructor', '=', True), ('category_id', 'in', (self.env.ref('openacademy.child_tag1').id, self.env.ref('openacademy.child_tag2').id))]

    @api.onchange('seats')
    def _onchange_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': "Wrong number of seats",
                    'message': "Seats must be greater than zero",
                }
            }

    @api.onchange('attendees')
    def _onchange_seats(self):
        if len(self.attendees) > self.seats:
            return {
                'warning': {
                    'title': "Wrong number of attendees",
                    'message': "Attendees can not be grater than seats",
                }
            }

    @api.constrains('instructor', 'attendees')
    def _check_instructor_not_in_attendees(self):
        for record in self:
            if record.instructor in record.attendees:
                raise exceptions.ValidationError("Instructor %s present in Atendees list" % record.instructor.name)