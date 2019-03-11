from odoo import api, fields, models


class Course(models.Model):
    _name = "openacademy.course"
    _description = "Course"
    _rec_name = "title"

    title = fields.Char(required=True, string="Title")
    description = fields.Text(required=True, string="Description")
