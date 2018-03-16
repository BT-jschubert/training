from odoo import fields, models, _

class OpenacademyCourse(models.Model):
    _name = 'openacademy.course'

    name = fields.Char(string="Course title", required=True, help="Name of the course")
    description = fields.Text(string="Description", help="Description of the course")
    sessions = fields.One2many(comodel_name="openacademy.session", inverse_name="related_course")