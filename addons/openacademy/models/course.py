from odoo import api, fields, models


class Course(models.Model):
    _name = 'course'
    _description = 'Courses'
    name = fields.Text(string='Name')
    description = fields.Html(string='Description')
    responsible_id = fields.Many2one(string='Responsible', comodel_name='res.users')
    sessions = fields.One2many(comodel_name='session', inverse_name='course_id')
    full_course = fields.Boolean(string='Course is Full', compute='_compute_full_course', store=True)

    #
    @api.depends('sessions', 'sessions.seats_taken')
    def _compute_full_course(self):
        for record in self:
            if record.sessions:
                is_full = True
                for session in record.sessions:
                    if session.seats_taken < 100:
                        is_full &= False
                        if not is_full:
                            break
                record.full_course = is_full
