from odoo import models, fields

class Course(models.Model):
    _name = 'openacademy.course'
    _rec_name = 'title'
    _sql_constraints = [
        ('title_description_check', 'CHECK(title != description)', "Title and description can not be equal"),
        ('title_unique_check', 'UNIQUE(title)', "Title must be unique"),
    ]

    title = fields.Char(string="Title")
    description = fields.Char(string="Description")
    responsible = fields.Many2one("res.users", string="Responsible")
    sessions = fields.One2many("openacademy.session", "course", string="Sessions")
