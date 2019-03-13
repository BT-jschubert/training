from odoo import api, fields, models


class Course(models.Model):
    _name = "openacademy.course"
    _description = "Course"
    _rec_name = "title"

    title = fields.Char(required=True, string="Title")
    description = fields.Text(required=True, string="Description")
    responsible_id = fields.Many2one('res.partner', 'Responsible')
    session_ids = fields.One2many('openacademy.session', 'course_id', 'Sessions')

    _sql_constraints = [
        ('name_uniq', 'unique (title)', "A course with this name already exists !"),
        ('name_diff_desc', 'CHECK( title <> description )', 'Name a description from the course must be different'),
    ]

    def copy(self, default=None):
        """ copy(default=None)

        Duplicate record ``self`` updating it with default values

        :param dict default: dictionary of field values to override in the
               original values of the copied record, e.g: ``{'field_name': overridden_value, ...}``
        :returns: new record

        """
        self.ensure_one()
        vals = self.copy_data(default)[0]
        vals['title'] = "Copy of [{0}]".format(self.title)
        # To avoid to create a translation in the lang of the user, copy_translation will do it
        new = self.with_context(lang=None).create(vals)
        self.with_context(from_copy_translation=True).copy_translations(new)


        return new