from odoo import models, fields, api

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
    has_all_sessions_full = fields.Boolean(string="Has all sessions full", compute=lambda self: None, search='_search_has_all_sessions_full')


    def _search_has_all_sessions_full(self, operator, value):
        records = self.env['openacademy.course'].search([('sessions', '!=', False)])
        ids = []
        for r in records:
            sessions_full = True
            for s in r.sessions:
                if s.seats > len(s.attendees):
                    sessions_full = False
                    break
            if sessions_full:
                ids.append(r.id)

        return[('id', 'in', ids)]