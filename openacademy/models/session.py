from odoo import models, fields


class Session(models.Model):
    _name = 'openacademy.session'
    name = fields.Char()
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Integer(help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    course = fields.Many2one("openacademy.course", requred=True)
    instructor = fields.Many2one("res.partner")
    attendees = fields.Many2many("res.partner", "session_attendee_rel", "partner", "attendee")