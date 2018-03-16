from odoo import fields, models, _

class OpenacademySession(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(string="Session title", required=True)
    start_date = fields.Date(string="Session date", default=fields.Date.today())
    duration = fields.Float(string="Duration time", required=True)
    number_of_seats = fields.Integer(string="Number of seats")
    related_course = fields.Many2one(comodel_name="openacademy.course")
    instructor = fields.Many2one("openacademy.partner")
    responsible = fields.Many2one(comodel_name="openacademy.responsible")