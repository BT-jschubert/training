from odoo import fields, models

class Course(models.Model):
    _name = 'course'
    _rec_name = 'title'

    title = fields.Char(string='Subject:')
    description = fields.Text(string = 'Description of the subject')
    sessions = fields.One2many(comodel_name='session', inverse_name="course_id", ondelete="set null", string="Sessions:")

    #SQL constraints
    _sql_constraints=[('unique_title', 'unique(title)', 'The name of the course already exists'),
                      ('diff_title_desc', 'CHECK(title != description)', 'The name of the course must differ from description')]