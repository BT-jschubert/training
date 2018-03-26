from odoo import models,fields,api,_

class Curso(models.Model):
    _name = 'openacademy.curso'
    _rec_name = "nombre"
    _sql_constraints = [('check_different_title_description', 'CHECK(nombre != descripcion)', 'Name and description cant be the same!'),
                        ('check_unique_title', 'UNIQUE(nombre)','Name should be unique')]

    nombre = fields.Text(required=True,translate=True)
    descripcion = fields.Text(default='Descripcion generica')
    responsible_id=fields.Many2one('res.users')
    session_ids = fields.One2many('openacademy.session','related_Course_id')
    #search field which shows which sessions are full
    has_full_sessions =fields.Boolean('Full Sessions?', compute='_compute_full_sessions',
                                        search='_full_session_search')

    @api.multi
    @api.depends('session_ids')
    def _compute_full_sessions(self):
        for course in self:
            for session in course.session_ids:
                full_sessions = session.search([('related_Course_id','=',course.id),
                                ('percentage_of_seats_taken','=',100)])
                result = full_sessions == session
                course.has_full_sessions = result
                full_session_ids = [x.id for x in full_sessions]
                session_ids = [x.id for x in course.session_ids]
                result = list(set(full_session_ids).intersection(set(session_ids)))

                # course.has_full_sessions = result == session_ids
                ## New API implementation not working properlly
                # full_sessions &= course.session_ids
                # if full_sessions &= course.session_ids is None:
                #     course.has_full_sessions = False
                # else:
                #     course.has_full_sessions = True

    def _full_session_search(self, operator, value):
        course_ids = []
        for course in self.search([]):
            for session in course.session_ids:
                full_sessions = session.search([('related_Course_id', '=', course.id),
                                                ('percentage_of_seats_taken', '=', 100)])
                full_session_ids = [x.id for x in full_sessions]
                session_ids = [x.id for x in course.session_ids]
                result = list(set(full_session_ids).intersection(set(session_ids)))
                if result == session_ids:
                    course_ids.append(course.id)
                    ## New API implementation not working properlly
                # full_sessions |= course.session_ids
        return [('id', 'in', list(set(course_ids)))]
        # return [('id', 'in', full_sessions )]

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {}, nombre=_('%s (copy)') % self.nombre)
        return super(Curso, self).copy(default)