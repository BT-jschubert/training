
from odoo import api,fields,models

class Course(models.Model):
    _name='course'
    _description = 'Courses'
    name = fields.Text(string='Name')
    description = fields.Html(string='Description')
    responsible_id = fields.Many2one(string='Responsible',comodel_name='res.users')
    sessions = fields.One2many(comodel_name='session',inverse_name='course_id')