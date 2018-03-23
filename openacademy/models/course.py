from odoo import fields, models, _, api


class OpenacademyCourse(models.Model):
    _name = 'openacademy.course'
    _sql_constraints = [('desc_dif_name', 'CHECK(name != description)',
                         'Description and name must be different'),
                        ('unique_name', 'UNIQUE(name)', 'Course name already exists')]

    name = fields.Char(string="Course title", required=True, help="Name of the course", translate=True)
    description = fields.Text(string="Description", help="Description of the course")
    sessions = fields.One2many("openacademy.session", "related_course")
    full_sessions = fields.Boolean(string="Fulfilled sessions", compute="_get_full_sessions",
                                   search='_search_full_sessions')
    responsible_id = fields.Many2one("res.users", string="Course's Responsible")

    def _search_full_sessions(self, operator, value):
        course_ids = []
        for r in self.search([]):
            r.full_sessions = True
            for session in r.sessions:
                remain_seats = session._get_remain_seats()
                if remain_seats == 0.0:
                    continue
                else:
                    r.full_sessions = False
                    break

            if r.full_sessions:
                course_ids.append(r.id)

        return [('id', 'in', list(set(course_ids)))]

    @api.depends('sessions')
    def _get_full_sessions(self):
        for r in self.search([]):
            r.full_sessions = True
            for session in r.sessions:
                remain_seats = session._get_remain_seats()
                if remain_seats == 0.0:
                    continue
                else:
                    r.full_sessions = False
                    break

    @api.multi
    def copy(self, default):
        default = dict()
        default['name'] = "Copy of " + self.name
        return super(OpenacademyCourse, self).copy(default)
