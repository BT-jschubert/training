from odoo import models, fields


class resPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    is_instructor = fields.Boolean(string="Instructor")
    sessions = fields.Many2many("openacademy.session", relation="session_attendKee_rel", column1="partner", column2="session", string="Sessions")