from odoo import fields, models, _


class ResPartnerExt(models.Model):
    _inherit = 'res.partner'

    is_instructor = fields.Boolean(string="Is or not is instructor")
    session_ids = fields.Many2many("openacademy.session", "session_partner_rel")
    session_wizard_ids = fields.Many2many("openacademy.session_wizard", "session_wizard_partner_rel")


