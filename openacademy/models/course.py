from odoo import models, fields

class Course(models.Model):
    _name = 'openacademy.course'
    _rec_name = 'title'
    title = fields.Char()
    description = fields.Char()
    responsible = fields.Many2one("res.users")
    sessions = fields.One2many("openacademy.session", "course")
