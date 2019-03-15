from odoo import api
from odoo import fields
from odoo import models

class Course(models.Model):
    _name = "openacademy.course"
    _description = "Course"
    _rec_name = "title"

    title = fields.Char(required=True, string="Title")
    description = fields.Text(required=True, string="Description")
    responsible_id = fields.Many2one('res.users', 'Responsible')
    session_ids = fields.One2many('openacademy.session', 'course_id', 'Sessions')

    _sql_constraints = [
        ('name_uniq', 'unique (title)', "A course with this name already exists !"),
        ('name_diff_desc', 'CHECK( title <> description )', 'Name a description from the course must be different'),
    ]

    @api.multi
    def copy(self):

        default = {'title': "Copy of [{0}]".format(self.title)}
        new = super(Course,self).copy(default)
        self.with_context(from_copy_translation=True).copy_translations(new)

        return new