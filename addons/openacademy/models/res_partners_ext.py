from odoo import api, fields, models


class PartnerExt(models.Model):
    _inherit ='res.partner'

    is_instructor = fields.Boolean(string='Instructor')
    sessions = fields.One2many(string='Sessions', comodel_name="session",inverse_name='instructor_id')

