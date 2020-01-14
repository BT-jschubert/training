
from odoo import api,fields,models

class Session(models.Model):
    _name='session'
    _description = 'Sessions'

    name = fields.Text(string='Name')
    start_date = fields.Date(string='StartDate',default=fields.Date.today)
    duration = fields.Integer(string='Duration in Minutes')
    seats = fields.Integer(string='No of Seats')
    course_id = fields.Many2one(comodel_name='course', ondelete='cascade')
    instructor_id = fields.Many2one(comodel_name='res.partner',ondelete='set null')
    attendees = fields.Many2many(comodel_name='res.partner',relation='session_attendees')
