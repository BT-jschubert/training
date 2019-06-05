from odoo import models
from odoo import fields


class resPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    is_instructor = fields.Boolean()
    sessions = fields.Many2many("openacademy.session", relation="session_attendee_rel", column1="partner", column2="session")