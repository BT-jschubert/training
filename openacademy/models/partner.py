from odoo import fields, models


class Partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    is_instructor = fields.Boolean(string="Instructor")
    sessions_ids = fields.Many2many('openacademy.session',
                                    'attend_session_rel')
