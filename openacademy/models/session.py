from odoo import models,fields,_

class Session(models.Model):
    _name = 'openacademy.session'
    name = fields.Text(required=True)
    start_date = fields.Date(default=fields.Date.today())
    duration=fields.Datetime()
    number_of_seats=fields.Integer()
    related_Course_id=fields.Many2one('openacademy.curso')
    instructor_id=fields.Many2one('res.partner')
    attendees_ids = fields.Many2many('res.partner')
